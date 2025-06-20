"""

    Software Updater
    @gl36

    20/06/2025
"""

## Imports
import tkinter as tk
from tkinter import ttk, filedialog

import requests
import sys
import os

import zipfile
import tempfile
import shutil

## Class
def format_error(exception: Exception, message: str = None) -> str:
    name: str = type(exception).__name__

    if message:
        message = f'{message} '
    else:
        message = ""
    return f'{message}[{name}]: {str(exception)}'

class _UpdaterUI:
    def __init__(self, title: str, ui_master: tk.Tk | None = None) -> None:
        self.ui_master = ui_master
        self.title = title

        if not self.ui_master:
            self.root = tk.Tk()
        else:
            self.root = tk.Toplevel(self.ui_master)
        
        # Create UI
        self.container = ttk.Frame(self.root, padding=10)
        self.container.grid()

        self.label_title = ttk.Label(self.container, text=self.title, anchor="w")
        self.label_title.pack(expand=True, fill="x")

        self.label_status = ttk.Label(self.container, text="waiting to update...", anchor="w")
        self.label_status.pack(expand=True, fill="x")

        self.progress_bar = ttk.Progressbar(self.container, length=300)
        self.progress_bar.pack(fill="x", expand=True, pady=(20, 0))
    
    def set_status(self, text: str = ""):
        self.label_status.config(text=text)
        self.root.update()
    
    def set_progress(self, current: float | int = None, max: float| int = None):
        if current != None:
            self.progress_bar["value"] = current
        
        if max != None:
            self.progress_bar.config(maximum=max)
        
        self.root.update()

class Updater:
    def __init__(self, url: str, directory: str, branch: str = "main", update_name: str = "performing software update...", ui_master: tk.Tk = None) -> None:
        self.url = url
        self.dir = directory
        self.branch = branch
        self.ui_master = ui_master
        self.title = update_name
    
    def update(self) -> tuple[bool, str | None]:
        # Create UI
        interface = _UpdaterUI(self.title)
        interface.set_progress(0, 5)
       

        # Download new archive
        interface.set_status("downloading archive")
        try:
            download_response = requests.get(f'{self.url}/{self.branch}')
            download_response.raise_for_status()
        except Exception as e:
            interface.root.destroy()
            return False, format_error(e, "Download failed!")
        
        interface.set_progress(1)
        
        # Install the downloaded archive in a temporary file
        try:
            installed_archive = tempfile.TemporaryFile(mode="w")
            installed_archive.write(download_response.content)
        except Exception as e:
            interface.root.destroy()
            return False, format_error(e, "Failed to install temporary archive!")
        
        # Extract the downloaded archive
        interface.set_status("extracting downloaded archive")
        try:
            # Create a temporary directory to extract to
            archive_dump = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
            
            # Extract the file
            with zipfile.ZipFile(installed_archive.name, "r") as file:
                file.extractall(archive_dump.name)
            
            # The downloaded archive is no longer required, so remove it.
            installed_archive.close()
            del installed_archive
        except Exception as e:
            interface.root.destroy()
            return False, format_error(e, "Failed to extract the downloaded archive!")
        
        interface.set_progress(2)
        
        # Remove the current files
        interface.set_status("removing current installation")
        try:
            shutil.rmtree(self.dir)
            os.makedirs(self.dir)
        except Exception as e:
            interface.root.destroy()
            return False, format_error(e, "Failed to remove the current installation!")
        
        interface.set_progress(3)

        # Install the extracted data
        interface.set_status("installing update")
        try:
            shutil.copytree(archive_dump.name, self.dir, dirs_exist_ok=True)
        except Exception as e:
            interface.root.destroy()
            return False, format_error(e, "Failed to install new files!")
        
        interface.set_progress(4)
        
        # Finish the update
        interface.set_status("finishing software update")
        archive_dump.cleanup()

        interface.root.destroy()

        return True, None

# Add testing functionality
if __name__ == "__main__":
    print("(Library testing)")
    s, r = Updater(input("url> "), filedialog.askdirectory(initialdir=os.path.dirname(__file__))).update()

    input(s,r)