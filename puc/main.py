#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

import puc


class Main(puc.Frame):
    """Main frame object class."""
    def __init__(self, parent: puc.Frame, controller: puc.Tk):
        puc.Frame.__init__(self, parent)

        lblTitle = puc.Label(self, text = puc.messages["program.title"],
                             style="LMT.TLabel")

        self.btnConvert = puc.Button(
            self,
            text = puc.messages["main.button.convert"],
            command = lambda: controller.show_frame(puc.Converter))

        btnUnits = puc.Button(self, text = puc.messages["main.button.units"],
                              command = lambda: controller.show_frame(puc.Units))

        self.btnSave = puc.Button(self, text = puc.messages["main.button.save"],
                                  command = controller.save_data)

        self.btnSave.state(["disabled"])

        btnAbout = puc.Button(
            self,
            text = puc.messages["main.button.about"],
            command = lambda: puc.msgBox.showinfo(
                title = puc.messages["main.button.about"],
                message = puc.messages["program.title"] + "\n\n"
                        + "{:>11}".format(puc.messages["program.version"] +":  ")
                        + puc.__version__
                        + "\n" + "{:>13}".format(puc.messages["program.author"] +":  ")
                        + puc.__author__))

        btnClose = puc.Button(self, text = puc.messages["button.close"],
                              command = controller.close)

        # If no datafaile found, then disable converting button (no data!)
        self.btnConvert.state(["!disabled" if controller.df_exists else "disabled"])

        # Finally show labels and buttons (adds to the grid)
        lblTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=15, sticky="nw")
        self.btnConvert.grid(row=1, column=0, padx=10, pady=5)
        btnUnits.grid(row=1, column=1, padx=10, pady=5)
        self.btnSave.grid(row=1, column=3, padx=20, pady=5)
        btnAbout.grid(row=3, column=1, padx=10, pady=35, sticky="se")
        btnClose.grid(row=3, column=3, padx=20, pady=35, sticky="se")
