from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input, Label
from textual.validation import Function, Number, ValidationResult, Validator
from textual.containers import ScrollableContainer
from textual.screen import Screen
import sys
from sim_dependencies import *

json_file = None
ADMIN = False

for arg in sys.argv: 
    if arg == "--admin": ADMIN = True

def read_json():
    with open('qc_sim_settings.json','r') as openfile:
        json_file = json.load(openfile)
    return json_file


class SettingsNameDisplay(Static):
    """Widget to display the QC system settings' name from qc_sim_DIP_settings.json"""

class SpecialSettingsNameDisplay(Static):
    """Widget to display the QC system special stettings' name from qc_sim_DIP_settings.json"""

class TextAYS(Static):
    """Widget to display text for the Are you sure screen"""

class Config(Static):
    """Widget of the config system"""

    def compose(self) -> ComposeResult:
        """Create widget"""
        yield SettingsNameDisplay(f"{self.item[0]}: {self.item[1]}")
        yield Button("On",id="ON",variant="success")
        yield Button("Off",id="OFF",variant="error")

    def on_button_pressed(self,event: Button.Pressed) -> None:
        global json_file
        if event.button.id == "ON":
            self.add_class("toggle_on")
            json_file[self.item[0]] = "On"
            self.item[1] = "On"
            sndisplay = self.query_one(SettingsNameDisplay)
            sndisplay.update(f"{self.item[0]}: {self.item[1]}")
        elif event.button.id == "OFF":
            self.add_class("toggle_off")
            json_file[self.item[0]] = "Off"
            self.item[1] = "Off"
            sndisplay = self.query_one(SettingsNameDisplay)
            sndisplay.update(f"{self.item[0]}: {self.item[1]}")

class Config_Special(Static):
    """Widget of the config system"""

    def compose(self) -> ComposeResult:
        """Create widget"""
        yield SpecialSettingsNameDisplay(f"{self.item[0]}: {self.item[1]}")
        yield Input(placeholder="Enter an integer...",
                    validators=[Function(is_integer,"Value is not an integer"),
                                Number(minimum=1,maximum=1000)])

    @on(Input.Changed)
    def show_invalid_reasons(self,event: Input.Changed) -> None:
        inputv = self.query_one(Input)
        if is_integer(inputv.value): json_file[self.item[0]] = int(inputv.value); self.item[1] = inputv.value
        sndisplay = self.query_one(SpecialSettingsNameDisplay)
        sndisplay.update(f"{self.item[0]}: {self.item[1]}")

def is_integer(value: str) -> bool:
    try: returnv = float(value) == float(int(value))
    except: returnv = False
    return returnv

class AreYouSureScreen(Screen):
    BINDINGS = [("y","pop_screen_y","Yes"),("n","app.pop_screen","No")]

    def compose(self) -> ComposeResult:
        yield TextAYS("- Are you sure? -",id="title")
        yield TextAYS("Are you sure you want to save?")
        yield TextAYS("Press (y) for yes and (n) for no",id="choice")

    def action_pop_screen_y(self) -> None:
        json_object = json.dumps(json_file,indent=4)
        with open("qc_sim_settings.json","w") as outfile:
            outfile.write(json_object)
        app.pop_screen()


class Config_App(App):
    """The config app used to config the QC simulator"""

    BINDINGS = [("d","toggle_dark","Toggle dark mode"),("h","home_button","Revert to home page"),("q","quit_button","Quit"),
                ("s","save_button","Save config")]

    CSS_PATH = "qcconfig.tcss"

    def compose(self) -> ComposeResult:
        global json_file
        """Child widgets"""
        self.title = '- Quantum simulation settings config -'
        if ADMIN: self.title = '- Admin mode. -'; yield Label("WARNING: Any setting that is followed by the suffix -dev is an admin setting! Development only!")
        yield Header(icon='⚙')
        yield Footer()
        json_file = read_json()
        configs = []
        special_configs = []
        for itemv in json_file.items():
            if "-dev" in itemv[0] and not ADMIN: continue
            if type(itemv[1]) != int:
                new_config = Config()
                new_config.scroll_visible()
                new_config.item = list(itemv)
                configs.append(new_config)
                continue
            new_config = Config_Special()
            new_config.scroll_visible()
            new_config.item = list(itemv)
            special_configs.append(new_config)
        configs += special_configs
        yield ScrollableContainer(*configs)

    def action_toggle_dark(self) -> None:
        """Action to toggle dark mode"""
        self.dark = not self.dark

    def action_home_button(self) -> None:
        """Action to revert to home page"""
        self.dark = not self.dark
    
    def action_quit_button(self) -> None:
        """Action to quit"""
        exit()
    
    def on_mount(self) -> None:
        self.install_screen(AreYouSureScreen(),name="areyousure")

    def action_save_button(self) -> None:
        """Action to save the new settings"""
        self.push_screen('areyousure')

if __name__  == "__main__":
    app = Config_App()
    app.run()