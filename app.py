"""

    Application Root
    @gl36

    20/06/2025

"""

# Imports
from internal.lib import file_system
from internal.runtime import ui, updater

import json
import sys

from tkinter import messagebox, filedialog

import ttkbootstrap as ttk
import ttkbootstrap.dialogs.dialogs as dialogs
from ttkbootstrap.constants import *

# Project
class App:
    def __init__(self):
        # Project Properties

        ## Project Data
        self.FileSystem = file_system.FileSystem(__file__)
        self.file_config = self.FileSystem.get_resource()

        self.settings = file_system.SettingsHelper()