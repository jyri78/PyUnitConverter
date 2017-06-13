#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

from __future__ import absolute_import


# Deny direct access
if __name__ == "__main__":
    #from os import _exit; _exit(1)
    raise SystemExit(1)


__version__ = 'x.x' # will be reset

__author__ = 'Jüri Kormik'

__all__ = ["messages", "read_data", "save_data", "text2float", "float2text", "run"]


try:
    from tkinter import Tk, TkVersion, Frame, X, END
except ImportError:
    from Tkinter import Tk, TkVersion, Frame, X, END
try:
    import tkinter.messagebox as msgBox
except ImportError:
    import tkMessageBox as msgBox

if TkVersion < 8.5:
    root = Tk()  # otherwise create root in main
    root.withdraw()
    msgBox.showerror("PyUnitConverter Cannot Start",
            "PyUnitConverter requires tcl/tk 8.5+, not %s." % TkVersion,
            parent=root)
    raise SystemExit(1)


try:
    from tkinter.ttk import Style, Label, Button, Combobox, Entry
except ImportError:
    from ttk import Style, Label, Button, Combobox, Entry

try:
    import json
except: pass

try:
    import pickle
except: pass


from glob import glob

# Python 2 and 3
from io import open
from os.path import exists

# Import program parts into module `puc`
from puc.main import *
from puc.converter import *
from puc.units import *
from puc.statusbar import *
from puc.program import *


SM_NONE, SM_JSON, SM_PICKLE = -1, 0, 1
lang = {}
messages = {}
settings = {}
saving_modes = [False, False]
settings_file = "PyUnitConverter.json"
puc_icon = "./puc/puc.ico"
db_filename = "units"
db_file_ver = ""
datafile = ""


# Detects available saving modes
try:
    pickle.DEFAULT_PROTOCOL
    saving_modes[SM_PICKLE] = True
except: pass

try:
    json.dumps('\u0020')
    saving_modes[SM_JSON] = True
except: pass


# ==============================================================================
# Functions for loading language file
# ==============================================================================

def load_lang():
    global lang, messages

    # Import language file
    lng = getattr(__import__("lang." + puc.settings["lang"]), puc.settings["lang"])
    lang = lng.lang
    messages = lng.messages


# ==============================================================================
# Functions for reading/writing data from/to file
# (supported two savingmodes: JSON ja PICKLE)
# ==============================================================================

def read_data(file: str, mode = 0) -> dict:
    """Reads data from file."""
    data = None
    if not mode:
        with open(file, "r", encoding="UTF-8") as f:
            data = json.load(f)
    else:
        # PICKLE saves data in binary form
        with open(file, "rb") as f:
            data = pickle.load(f)
    return data

def save_data(file: str, data: dict, mode = 0):
    """Saves data to the file."""
    if not mode:
        with open(file, "w", encoding="UTF-8") as f:
            json.dump(data, f)
    else:
        with open(file, "wb") as f:
            pickle.dump(data, f)


# ==============================================================================
# Functions for text to float conversion and vice versa
# ==============================================================================

def text2float(txt: str) -> float:
    """Converts text to float.
    If text is not number, then returns `0.0`
    """
    try:
       return float(txt.replace(",", "."))
    except:
        return 0.0

def float2text(number: float):
    """Converts float to text and replaces point width comma when necessary."""
    if lang["flPoint_comma"]:
        return str(number).replace(".", ",")
    else:
        return str(number)


# ==============================================================================
# Function to run a program (user GUI)
# ==============================================================================

def run():
    global datafile, db_filename

    # Get database filename
    db_filename = settings["db_filename"]

    # Set datafile full name
    if saving_modes[settings["saving_mode"]] :
        datafile = db_filename + db_file_ver \
                + messages["program.ext"][settings["saving_mode"]]

    Program().mainloop()
