#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

lang = {
    "lang": "estonian",  # should be in english
    "flPoint_comma": True,  # floating point symbol is `,` instead `.`
    "translator": "Jüri Kormik"
    }

messages = {
    "program.ext":      [".json", ".pickle"],
    "program.title":    "Lihtne mõõtühikute teisendaja",
    "program.author":   "Autor",
    "program.version":  "Versioon",

    "program.err.title":  "Andmefail salvestamata",
    "program.err.text":   "Andmefail on salvestamata.\nKas oled kindel, et soovid programmi sulgeda?",

    # Statusbar messages
    "status.saving_mode":  ["<POLE>", " JSON ", "PICKLE"],
    "status.no_datafile":  "Andmefaili ei leitud.",
    "status.data_saved":   "Andmefail salvestatud.",

    "status.selected_list":  "Valitud mõõtühikute loend:  ",
    "status.added_list":     "Lisatud mõõtühikute loend:  ",
    "status.list_exists":    "Lisatav mõõtühikute loend on juba olemas.",

    "status.selected_unit":  "Valitud mõõtühik:  ",
    "status.added_unit":     "Lisatud mõõtühik:  ",
    "status.unit_exists":    "Lisatav mõõtühik on juba olemas.",

    "status.added_multiplier":  "Lisatud/Muudetud kordaja:  ",

    "status.selected_from":  "Valitud mõõtühik millele:  ",
    "status.selected_to":    "Valitud mõõtühik millelt:  ",

    # Universal button texts
    "button.close":   "Sulge",
    "button.add":     "Lisa",
    "button.change":  "Lisa/Muuda",
    "button.cancel":  "Lõpeta",

    # Frame texts
    "main.button.convert":  "Mõõtühikute teisendaja",
    "main.button.units":    "Lisa/Muuda mõõtühikuid",
    "main.button.save":     "Salvesta andmed",
    "main.button.about":    "Programmist",

    "converter.button.calc":  "Arvuta",

    "units.label.units_list":  "Ühikute loend",
    "units.label.base":        "Baasühik (infoks)",
    "units.label.converter":   "Mõõtühiku teisendus",
    "units.label.unit":        "Mõõtühik",
    "units.label.multiplier":  "Kordaja",
    "units.button.save":       "Salvesta",
    }
