# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause

from pathlib import Path
from customtkinter import *
import yaml
import json


class Client:
    def __init__(self):
        self.KeySense = Path(__file__).parents[1]

        # Configuration files
        with open("cfg.json", "r") as cfg:
            self.language = json.load(cfg)["DefaultLanguage"]

        # Scripts
        with open(self.KeySense / "script.yml", "r") as scripts:
            self.scripts = yaml.full_load(scripts)["scripts"]
            self.script_triggers = [script["trigger"] for script in self.scripts]
            self.script_replacers = [script["replace"] for script in self.scripts]

        # Client settings
        self.app = CTk()
        self.RESOLUTION = "1280x720"
        self.app.geometry(self.RESOLUTION)

    def application(self):
        CTkButton(master=self.app, text="KeySense", corner_radius=32).place(
            relx=0.5, rely=0.5, anchor="center"
        )

    def display_app(self):
        # Refresh application
        self.application()

        # Display application
        self.app.mainloop()


if __name__ == "__main__":
    Client().display_app()
