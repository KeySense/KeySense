# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause
from pathlib import Path
from pynput import keyboard
import yaml
import json


class OSSense:
    def __init__(self):
        self.KeySense = Path(__file__).parents[1]

        # Scripts
        with open(self.KeySense / "Script.yml", "r") as scripts:
            self.scripts = yaml.full_load(scripts)["scripts"]
            self.script_triggers = [script["trigger"] for script in self.scripts]
            self.script_replacers = [script["replace"] for script in self.scripts]

        # Listener
        self.key_pressed = list()

    def trigger_script(self, trigger):
        # max_trigger_len = max([len(trigger) for trigger in self.script_triggers])
        print(trigger)

    def capture_trigger(self, key):
        self.key_pressed.append(str(key).replace("'", ""))
        trigger_lens = [len(trigger) for trigger in self.script_triggers]
        for len_trigger in trigger_lens:
            print(self.key_pressed[-len_trigger:])
            print("".join(self.key_pressed[-len_trigger:]))

            try:
                if "".join(self.key_pressed[-len_trigger:]) in self.script_triggers:
                    self.trigger_script(
                        trigger="".join(self.key_pressed[-len_trigger:])
                    )
            except Exception as OutOfIndex:
                continue

    def listener(self):
        with keyboard.Listener(on_press=self.capture_trigger) as listener:
            listener.join()


if __name__ == "__main__":
    OSSense().listener()
