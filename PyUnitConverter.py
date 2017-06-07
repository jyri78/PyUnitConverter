#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

__version__ = '1.0.0'

__author__ = 'Jüri Kormik'


from locale import getdefaultlocale

import puc


# Load settings if exists or set default
if puc.exists(puc.settings_file):
    puc.settings = puc.read_data(puc.settings_file, puc.SM_JSON)
else:
    puc.settings = {
        "lang": getdefaultlocale()[0][:2],
        "saving_mode": puc.SM_JSON,
        "db_filename": "units" # without extension
        }

    # If language does not exist, then reset to default
    if not puc.exists("./lang/"+ puc.settings["lang"] +".py"):
        puc.settings["lang"] = "en"


# Import language file
lng = getattr(__import__("lang." + puc.settings["lang"]), puc.settings["lang"])


if __name__ == "__main__":
    # Set some global variables
    puc.__version__ = __version__
    puc.lang = lng.lang
    puc.messages = lng.messages

    # Run the program
    puc.run()
