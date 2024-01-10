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
            self.script_map = {
                item["trigger"]: item["replace"] for item in self.scripts
            }

        # Listener
        self.keys_pressed = list()

    def clear_cache(self):
        self.keys_pressed.clear()

    def trigger_script(self, trigger):
        # max_trigger_len = max([len(trigger) for trigger in self.script_triggers])
        print(trigger)
        print(self.script_map[trigger])
        self.clear_cache()

    def capture_trigger(self, key):
        if key == keyboard.Key.space:
            self.clear_cache()
            print(self.keys_pressed)

        else:
            print(self.keys_pressed)
            self.keys_pressed.append(str(key).replace("'", ""))

            if "".join(self.keys_pressed) in [
                trigger for trigger in self.script_triggers
            ]:
                self.trigger_script(trigger="".join(self.keys_pressed))

    def listener(self):
        self.clear_cache()
        with keyboard.Listener(on_press=self.capture_trigger) as listener:
            listener.join()


if __name__ == "__main__":
    OSSense().listener()
