# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause

from pathlib import Path
import customtkinter as ctk
import yaml
import json


class Client:
    def __init__(self, appearance="System", theme="blue"):
        self.KeySense = Path(__file__).parents[1]

        # Configuration files
        with open("cfg.json", "r") as cfg:
            self.language = json.load(cfg)["DefaultLanguage"]

        # Scripts
        with open(self.KeySense / "Script.yml", "r") as scripts:
            self.scripts = yaml.full_load(scripts)["scripts"]
            self.script_triggers = [script["trigger"] for script in self.scripts]
            self.script_replacers = [script["replace"] for script in self.scripts]

        # Client
        self.app = ctk.CTk()

        # Client settings
        self.appearance_theme = ctk.set_appearance_mode(appearance)
        self.color_theme = ctk.set_default_color_theme(theme)
        self.RESOLUTION = "1280x720"
        self.app.geometry(self.RESOLUTION)

    def menu_selection(self, option):
        print(f"User selection: {option}")

    def elements(self):
        # Option menu
        option_menu = ctk.CTkOptionMenu(
            master=self.app, values=["Scripts", "Options"], command=self.menu_selection
        )
        option_menu.set("Option 1")
        option_menu.place()

    def create(self):
        # Render Client Elements
        self.elements()

        # Display Client
        self.app.mainloop()


if __name__ == "__main__":
    Client().create()
