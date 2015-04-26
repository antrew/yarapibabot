from kivy.lang import Builder
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsPanel

from settingsjson import settings_json

Builder.load_string('''
<Interface>:
    orientation: 'vertical'
    Button:
        text: 'Open Settings'
        font_size: 50
        on_release: app.open_settings()    
''')

class Interface(BoxLayout):
    pass

class SettingsApp(App):
    def build(self):
        self.settings_cls = SettingsPanel
        self.use_kivy_settings = False
        return Interface()
    
    def build_config(self, config):
        config.setdefaults('configuration', {
                                       'set_point': 0.0,
                                       'Kp': 10,
                                       'Ki': 2,
                                       'Kd': 1,
                                       'disable_motors': False})
    
    def build_settings(self, settings):
        settings.add_json_panel('Settings',
                                self.config,
                                data=settings_json)
    
    def on_config_change(self, config, section, key, value):
        print config, section, key, value
    
SettingsApp().run()