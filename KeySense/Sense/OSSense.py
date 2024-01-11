# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause

from pathlib import Path
from pynput.keyboard import Listener, Key, Controller
import yaml
import string


class OSSense:
    def __init__(self):
        self.KeySense = Path(__file__).parents[1]

        # Scripts
        with open(self.KeySense / "Script.yml", "r") as scripts:
            self.scripts = yaml.full_load(scripts)["scripts"]
            self.script_triggers = [script["trigger"] for script in self.scripts]
            self.script_replacers = [script["replace"] for script in self.scripts]
            self.script_map = {
                item["trigger"]: item["replace"] for item in self.scripts
            }
            self.script_triggers_len = [
                len(trigger) for trigger in self.script_triggers
            ]

        # Listener
        self.keys_pressed = list()
        self.hotkey_trigger = [Key.alt, Key.ctrl, Key.shift]
        self.replacer_trigger = string.printable

        # Keyboard actions
        self.keyboard = Controller()

    def clear_cache(self):
        self.keys_pressed.clear()

    @staticmethod
    def key_to_str(key):
        return str(key).replace("'", "")

    def is_trigger(self, key):
        if (key in self.hotkey_trigger) or (key in self.replacer_trigger):
            return True
        return False

    def trigger_hotkey_script(self):
        self.clear_cache()
        # TODO

    def delete_text(self, text):
        for _ in range(len(text)):
            self.keyboard.press(Key.backspace)
            self.keyboard.release(Key.backspace)

    def write_text(self, text):
        print(text)
        for letter in text:
            self.keyboard.press(letter)
            self.keyboard.release(letter)

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
