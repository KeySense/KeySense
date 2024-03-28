# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause

from pynput.keyboard import Listener, Key, Controller
from Languages import sense_es_la1, sense_pt_br, sense_lan
from pathlib import Path

import yaml
import string


class OSSense:
    def __init__(self, scripts_path=None):
        self.KeySense = Path(__file__).parents[1]

        # Scripts
        if scripts_path is None:
            scripts_path = self.KeySense / "Script.yml"

        with open(scripts_path, "r", encoding="utf-8") as scripts:
            self.scripts = yaml.full_load(scripts)["scripts"]

        self.script_triggers = [script["trigger"] for script in self.scripts]
        self.script_replacers = [script["replacer"] for script in self.scripts]
        self.script_map = {item["trigger"]: item["replacer"] for item in self.scripts}
        self.script_triggers_len = [len(trigger) for trigger in self.script_triggers]

        # Listener
        self.keys_pressed = list()
        self.hotkey_trigger = [Key.alt, Key.ctrl, Key.shift]
        self.replacer_trigger = string.printable

        # Keyboard actions
        self.keyboard = Controller()
        (
            self.NEWLINE_MAP,
            self.TAB_MAP,
        ) = sense_lan()  # If in 'replacer', generates 4 spaces line

        # Language specific
        self.special_letters_es_la1 = sense_es_la1()
        self.special_letters_pt = sense_pt_br()

    @staticmethod
    def key_to_str(key):
        return str(key).replace("'", "")

    def clear_cache(self):
        self.keys_pressed.clear()

    def simulate_key(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    def is_trigger(self, key):
        if (key in self.hotkey_trigger) or (key in self.replacer_trigger):
            return True
        return False

    def is_special_action(self, letter):
        return letter in [self.NEWLINE_MAP, self.TAB_MAP]

    def is_lan_specific_letter(self, letter):
        if letter in self.special_letters_pt or letter in self.special_letters_es_la1:
            return True
        return False

    def type_with_tilde_enye_cedilla(self, letter):
        # Executes tilde, enye (ñ) and C cedilla (ç)

        self.keyboard.press(Key.alt_gr)
        self.simulate_key(letter)
        self.keyboard.release(Key.alt_gr)

    def execute_special_action(self, letter):
        if letter == self.NEWLINE_MAP:
            self.simulate_key(Key.enter)
        if letter == self.TAB_MAP:
            for _ in range(4):
                self.simulate_key(Key.tab)

    def execute_lan_specific_letter(self, letter):
        # TODO
        self.type_with_tilde_enye_cedilla(letter)
        self.type_with_tilde_enye_cedilla(letter)

    def trigger_hotkey_script(self):
        self.clear_cache()
        # TODO

    def delete_text(self, text):
        for _ in range(len(text)):
            self.simulate_key(Key.backspace)

    def write_text(self, text):
        for letter in text:
            if self.is_special_action(letter):
                self.execute_special_action(letter)
                break

            if self.is_lan_specific_letter(letter):
                self.execute_lan_specific_letter(letter)
                break

            else:
                self.simulate_key(letter)

    def trigger_replacer_script(self, trigger):
        self.delete_text(text=trigger)
        self.write_text(text=self.script_map[trigger])
        self.clear_cache()

    def capture_trigger(self, key):
        key = self.key_to_str(key)
        if not self.is_trigger(key):
            self.clear_cache()

        if key in [self.key_to_str(_key) for _key in self.hotkey_trigger]:
            self.trigger_hotkey_script()

        if key in self.replacer_trigger:
            self.keys_pressed.append(key)

            if len(self.keys_pressed) > max(self.script_triggers_len):
                self.clear_cache()

            if "".join(self.keys_pressed) in [
                trigger for trigger in self.script_triggers
            ]:
                self.trigger_replacer_script(trigger="".join(self.keys_pressed))

    def listener(self):
        self.clear_cache()
        with Listener(on_press=self.capture_trigger) as listener:
            listener.join()


if __name__ == "__main__":
    OSSense().listener()