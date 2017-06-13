#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

lang = {
    "lang": "english",  # should be in english
    "flPoint_comma": False,  # floating point symbol is `,` instead `.`
    "translator": "Jüri Kormik"
    }

messages = {
    "program.ext":      [".json", ".pickle"],
    "program.title":    "Simple Unit Converter",
    "program.author":   "Author",
    "program.version":  "Version",

    "program.err.title":  "Datafile unsaved",
    "program.err.text":   "Datafile is not saved.\nAre you sure you want to exit the program?",

    # Statusbar messages
    "status.saving_mode":  ["<NONE>", " JSON ", "PICKLE"],
    "status.no_datafile":  "Datafile not found.",
    "status.data_saved":   "Datafile saved.",

    "status.selected_list":  "Selected unit list:  ",
    "status.added_list":     "Added units list:  ",
    "status.list_exists":    "Appendable units list already exists.",

    "status.selected_unit":  "Selected unit:  ",
    "status.added_unit":     "Added unit:  ",
    "status.unit_exists":    "Appendable unit already exists.",

    "status.added_multiplier":  "Added/Changed multiplier:  ",

    "status.selected_from":  "Selected unit to:  ",
    "status.selected_to":    "Selected unit from:  ",

    # Universal button texts
    "button.close":   "Close",
    "button.add":     "Add",
    "button.change":  "Add/Change",
    "button.cancel":  "Cancel",

    # Frame texts
    "main.button.convert":  "Unit Converter",
    "main.button.units":    "Add/Change Units",
    "main.button.save":     "Save data",
    "main.button.about":    "About",

    "converter.button.calc":  "Calc",

    "units.label.units_list":  "Units list",
    "units.label.base":        "Base unit (for info)",
    "units.label.converter":   "Unit converter",
    "units.label.unit":        "Unit",
    "units.label.multiplier":  "Multiplier",
    "units.button.save":       "Save",
    }
