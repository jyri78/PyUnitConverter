#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

import puc


class Main(puc.Frame):
    """Main frame object class."""
    def __init__(self, parent: puc.Frame, controller: puc.Tk):
        puc.Frame.__init__(self, parent)

        self.lblTitle = puc.Label(self, text = puc.messages["program.title"],
                                  style="PUCT.TLabel")

        self.cmbLang = puc.Combobox(self, state="readonly", width=2)
        self.cmbLang.bind("<<ComboboxSelected>>", controller.change_lang)
        self.cmbLang["values"] = puc.langs
        self.cmbLang.set(puc.settings["lang"])

        self.lblLang = puc.Label(self, text = puc.lang["lang"], style="PUCL.TLabel")

        self.btnConvert = puc.Button(
            self,
            text = puc.messages["main.button.convert"],
            command = lambda: controller.show_frame(puc.Converter))

        self.btnTranslation = puc.Button(
            self,
            text = puc.messages["main.button.translate"],
            command = lambda: controller.show_frame(puc.Translation))

        if puc.db_file_ver == 1 or not controller.df_exists:
            self.btnTranslation.state(["disabled"])

        self.btnUnits = puc.Button(self, text = puc.messages["main.button.units"],
                                   command = lambda: controller.show_frame(puc.Units))

        self.btnSave = puc.Button(self, text = puc.messages["main.button.save"],
                                  command = controller.save_data)

        self.btnSave.state(["disabled"])

        self.btnAbout = puc.Button(
            self,
            text = puc.messages["main.button.about"],
            command = lambda: puc.msgBox.showinfo(
                title = puc.messages["main.button.about"],
                message = puc.messages["program.title"] + "\n\n"
                        + "{:>11}".format(puc.messages["program.version"] +":  ")
                        + puc.__version__
                        + "\n" + "{:>13}".format(puc.messages["program.author"] +":  ")
                        + puc.__author__))

        self.btnClose = puc.Button(self, text = puc.messages["button.close"],
                                   command = controller.close)

        # If no datafaile found, then disable converting button (no data!)
        self.btnConvert.state(["!disabled" if controller.df_exists else "disabled"])

        # Finally show labels and buttons (adds to the grid)
        self.lblTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nw")
        self.cmbLang.grid(row=0, column=3, padx=20, sticky="es")
        self.lblLang.grid(row=1, column=3, padx=20, sticky="ne")
        self.btnConvert.grid(row=2, column=0, padx=10, sticky="ew")
        self.btnUnits.grid(row=3, column=0, padx=10, pady=15, sticky="ew")
        self.btnTranslation.grid(row=3, column=1, padx=10, pady=15, sticky="ew")
        self.btnSave.grid(row=3, column=3, padx=20, pady=15, sticky="ew")
        self.btnAbout.grid(row=4, column=1, padx=10, pady=35, sticky="esw")
        self.btnClose.grid(row=4, column=3, padx=20, pady=35, sticky="es")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)


    def change_lang(self):
        '''Changes frames language.'''
        self.lblTitle.config(text = puc.messages["program.title"])
        self.lblLang.config(text = puc.lang["lang"])
        self.btnConvert.config(text = puc.messages["main.button.convert"])
        self.btnUnits.config(text = puc.messages["main.button.units"])
        self.btnTranslation.config(text = puc.messages["main.button.translate"])
        self.btnSave.config(text = puc.messages["main.button.save"])
        self.btnAbout.config(text = puc.messages["main.button.about"])
        self.btnClose.config(text = puc.messages["button.close"])
