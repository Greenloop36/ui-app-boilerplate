"""

    Project File System
    @gl36

    20/06/2025

"""

# Imports
import os
import sys

import usersettings
import json

# Classes
class SettingsHelper:
    def __init__(self, app_id: str, default_settings: dict[str, any]):
        self.settings = usersettings.Settings(app_id)

        for key, value in default_settings.items():
            self.settings.add_setting(key, type(value), default=value)
        
        self.settings.load_settings()
    
    def get_setting(self, key: str) -> any:
        return self.settings[key]
    
    def set_setting(self, key: str, value: any, auto_save: bool = True):
        self.settings[key] = value

        if auto_save:
            self.save()
    
    def save(self):
        self.settings.save_settings()