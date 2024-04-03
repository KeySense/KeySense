# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause

from pathlib import Path
from pynput.keyboard import Listener, Key, Controller
import yaml
import string

from .utils.langs import sense_es_la1, sense_pt_br, sense_lan, hotkey_lan


class KeyboardSense:

    def __init__(self, scripts_path=None):
        self.KeySense = Path(__file__).parents[1]

        # Scripts
        if scripts_path is None:
            scripts_path = self.KeySense / "Script.yml"

        with open(scripts_path, "r", encoding="utf-8") as scripts:
            self.scripts = yaml.full_load(scripts)["scripts"]

        # Listener
        self.keys_pressed = list()
        self.supported_hotkeys = [Key.alt_l, Key.ctrl_l, Key.shift]
        self.hotkey_translation_map = {
            key: hotkey_lan()[hotkey]
            for hotkey, key in enumerate(self.supported_hotkeys)
        }
        self.replacer_trigger = string.printable
        self.listening_for_hotkey = False

        # Keyboard actions
        self.keyboard = Controller()
        (
            self.ENTER_MAP,
            self.TAB_MAP,
        ) = sense_lan()  # If in 'replacer', generates 4 spaces line

        # Language specific
        self.special_letters_es_la1 = sense_es_la1()
        self.special_letters_pt = sense_pt_br()

        # Load files
        self.load_scripts()

    @staticmethod
    def key_to_str(key):
        return str(key).replace("'", "")

    def has_triggers(self):
        if "trigger" in [list(script.keys())[0] for script in self.scripts]:
            return True
        return False

    def has_hotkeys(self):
        if "hotkey" in [list(script.keys())[0] for script in self.scripts]:
            return True
        return False

    def load_scripts(self):

        if self.has_triggers():

            self.script_triggers = [
                script["trigger"]
                for script in self.scripts
                if list(script.keys())[0] == "trigger"
            ]

            self.script_replacers = [
                script["replacer"]
                for script in self.scripts
                if list(script.keys())[0] == "trigger"
            ]
            self.script_map = {
                self.script_triggers[item]: self.script_replacers[item]
                for item in range(len(self.script_replacers))
            }
            self.script_triggers_len = [
                len(trigger) for trigger in self.script_triggers
            ]

        if self.has_hotkeys():
            self.hotkey_triggers = [
                script["hotkey"]
                for script in self.scripts
                if list(script.keys())[0] == "hotkey"
            ]
            self.hotkey_dos = [
                script["do"]
                for script in self.scripts
                if list(script.keys())[0] == "hotkey"
            ]
            self.hotkey_map = {
                self.hotkey_triggers[item]: self.hotkey_dos[item]
                for item in range(len(self.hotkey_dos))
            }

            self.hotkey_triggers_len = [
                len(trigger[1:]) for trigger in self.hotkey_triggers
            ]

    def clear_cache(self):
        self.listening_for_hotkey = False
        self.keys_pressed.clear()

    def simulate_key(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    def is_trigger(self, key):
        if (key in self.supported_hotkeys) or (key in self.replacer_trigger):
            return True
        return False

    def is_special_action(self, letter):
        return letter in [self.ENTER_MAP, self.TAB_MAP]

    def is_lan_specific_letter(self, letter):
        if letter in self.special_letters_pt or letter in self.special_letters_es_la1:
            return True
        return False

    def type_with_tilde_enye_cedilla(self, letter):

        # Executes tilde, enye (ñ) and C cedilla (ç)

        # For some reason ç lowercase doesn't execute with the normal code... :l
        # Implementing this .type hardcoded for this particular case

        if letter == self.special_letters_pt[-2]:
            self.keyboard.type(self.special_letters_pt[-2])

        else:
            self.keyboard.press(Key.alt_gr)
            self.simulate_key(letter)
            self.keyboard.release(Key.alt_gr)

    def execute_special_action(self, letter):

        if letter == self.ENTER_MAP:
            self.simulate_key(Key.enter)

        if letter == self.TAB_MAP:

            self.simulate_key(Key.tab)

    def execute_lan_specific_letter(self, letter):

        self.type_with_tilde_enye_cedilla(letter)

    def delete_text(self, text):
        for _ in range(len(text)):
            self.simulate_key(Key.backspace)

    def write_text(self, text):
        for letter in text:
            if self.is_special_action(letter):
                self.execute_special_action(letter)

            if self.is_lan_specific_letter(letter):
                self.execute_lan_specific_letter(letter)

            if not self.is_lan_specific_letter(letter) and not self.is_special_action(
                letter
            ):
                self.simulate_key(letter)

    def trigger_replacer_script(self, trigger):
        self.delete_text(text=trigger)
        self.write_text(text=self.script_map[trigger])
        self.clear_cache()

    def is_present_hotkey(self, trigger):
        for hotkey_trigger in self.hotkey_triggers:
            if trigger in hotkey_trigger:
                return True
        return False

    def trigger_hotkey_script(self, trigger):
        # TO BE IMPLEMENTED IN 2.0.0
        self.clear_cache()

    def capture_trigger(self, key):

        if self.listening_for_hotkey or (
            key in [_key for _key in self.supported_hotkeys]
            and self.is_present_hotkey(self.hotkey_translation_map[key])
        ):
            print("hotkey detected")
            if not self.listening_for_hotkey:

                self.hotkey = self.hotkey_translation_map[key]
                self.listening_for_hotkey = True

            else:
                if key in [_key for _key in self.supported_hotkeys]:
                    key = self.hotkey_translation_map[key]

                key = self.key_to_str(key)
                self.keys_pressed.append(key)
                print(self.keys_pressed)

                if len(self.keys_pressed) > max(self.hotkey_triggers_len):
                    self.clear_cache()

                if self.hotkey + "".join(self.keys_pressed) in [
                    trigger for trigger in self.hotkey_triggers
                ]:

                    print(self.hotkey + "".join(self.keys_pressed))
                    self.trigger_hotkey_script(
                        trigger=self.hotkey + "".join(self.keys_pressed)
                    )

        if not self.listening_for_hotkey:

            key = self.key_to_str(key)

            if not self.is_trigger(key):

                self.clear_cache()

            if key in self.replacer_trigger:
                self.keys_pressed.append(key)

                if len(self.keys_pressed) > max(self.script_triggers_len):
                    self.clear_cache()

                if "".join(self.keys_pressed) in [
                    trigger for trigger in self.script_triggers
                ]:
                    self.trigger_replacer_script(trigger="".join(self.keys_pressed))

    def listener(self, on_press=None):
        self.clear_cache()
        if on_press is None:
            on_press = self.capture_trigger

        with Listener(on_press=on_press) as listener:
            listener.join()
