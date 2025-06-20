"""

    Software Updater
    @gl36

    20/06/2025
"""

## Imports
import tkinter as tk
from tkinter import ttk, messagebox

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

class Updater:
    def __init__(self, url: str, directory: str, branch: str = "main") -> None:
        self.url = url
        self.dir = directory
        self.branch = branch
    
    def update(self) -> tuple[bool, str | None]:
        # Download the archive of
        try:
            download_response = requests.get(f'{self.url}/{self.branch}')
            download_response.raise_for_status()
        except Exception as e:
            return False, format_error(e, "Download failed!")
        
        # Install the downloaded archive in a temporary file
        try:
            installed_archive = tempfile.TemporaryFile(mode="w")
            installed_archive.write(download_response.content)
        except Exception as e:
            return False, format_error(e, "Failed to install temporary archive!")
        
        # Extract the downloaded archive
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
            return False, format_error(e, "Failed to extract the downloaded archive!")
        
        # Remove the current files
        try:
            shutil.rmtree(self.dir)
            os.makedirs(self.dir)
        except Exception as e:
            return False, format_error(e, "Failed to remove the current installation!")

        # Install the extracted data
        try:
            shutil.copytree(archive_dump.name, self.dir, dirs_exist_ok=True)
        except Exception as e:
            return False, format_error(e, "Failed to install new files!")
        
        # Finish the update
        archive_dump.cleanup()

        return True, None