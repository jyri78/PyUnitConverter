#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

import puc


class Main(puc.Frame):
    """Main frame object class."""
    def __init__(self, parent: puc.Frame, controller: puc.Tk):
        puc.Frame.__init__(self, parent)

        self.lblTitle = puc.Label(self, text = puc.messages["program.title"],
                                  style="LMT.TLabel")

        self.cmbLang = puc.Combobox(self, state="readonly", width=2)
        self.cmbLang.bind("<<ComboboxSelected>>", controller.change_lang)
        self.get_langs()

        self.btnConvert = puc.Button(
            self,
            text = puc.messages["main.button.convert"],
            command = lambda: controller.show_frame(puc.Converter))

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
        self.lblTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=15, sticky="nw")
        self.cmbLang.grid(row=0, column=3, padx=20, pady=15, sticky="ne")
        self.btnConvert.grid(row=1, column=0, padx=10, pady=5)
        self.btnUnits.grid(row=1, column=1, padx=10, pady=5)
        self.btnSave.grid(row=1, column=3, padx=20, pady=5)
        self.btnAbout.grid(row=3, column=1, padx=10, pady=35, sticky="se")
        self.btnClose.grid(row=3, column=3, padx=20, pady=35, sticky="se")

    def get_langs(self):
        out = []
        langs = puc.glob("./lang/*.py")
        for l in langs:
            # Accept only two letter languages
            out += [l[-5:-3]]
        self.cmbLang["values"] = sorted(out)
        self.cmbLang.set(puc.settings["lang"])

    def change_lang(self):
        self.lblTitle.config(text = puc.messages["program.title"])
        self.btnConvert.config(text = puc.messages["main.button.convert"])
        self.btnUnits.config(text = puc.messages["main.button.units"])
        self.btnSave.config(text = puc.messages["main.button.save"])
        self.btnAbout.config(text = puc.messages["main.button.about"])
        self.btnClose.config(text = puc.messages["button.close"])
