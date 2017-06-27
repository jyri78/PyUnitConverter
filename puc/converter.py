#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

from __future__ import division

import puc


class Converter(puc.Frame):
    """Converter frame object class."""
    def __init__(self, parent: puc.Frame, controller: puc.Tk):
        puc.Frame.__init__(self, parent)

        self.controller = controller

        # Variable used in methods (values of comboboxes)
        self.uCombos = {"lists": [], "tos": [], "froms": []}

        # Variable for remembering selections
        self.selected = {"list": None, "to": None, "from": None}


        # ----------------------------------------------------------------------
        # Units List (label, combobox, entry/textbox, button)
        # ----------------------------------------------------------------------

        self.lblTitle = puc.Label(
            self,
            text = puc.messages["program.title"] + "  –  "
                    + puc.messages["main.button.convert"].lower(),
            style = "PUCT.TLabel")

        self.lblUnitsList = puc.Label(self, text=puc.messages["units.label.units_list"])
        self.cmbUnitsList = puc.Combobox(self, state="readonly", width=15)
        self.cmbUnitsList.bind("<<ComboboxSelected>>", self.units_list_selected)


        # ----------------------------------------------------------------------
        # Conversion (label, combobox, entry/textbox, button)
        # ----------------------------------------------------------------------

        self.lblConverter = puc.Label(self,
                                      text = puc.messages["units.label.converter"],
                                      font = (None, 10, "bold"))

        self.txtMultiplier = puc.Entry(self, width=5)
        self.txtMultiplier.insert(0, "1")

        # Allow `Enter`-key in entry/textbox
        self.txtMultiplier.bind("<Return>", lambda evt: self.btnCalc.invoke())

        self.cmbTo = puc.Combobox(self, state="readonly")
        self.cmbTo.bind("<<ComboboxSelected>>", self.to_selected)

        # Create frame around result label to see, where it is
        self.lblResult = puc.Label(self, width=15)
        self.lblResult['borderwidth'] = 1
        self.lblResult['relief'] = "solid"

        self.cmbFrom = puc.Combobox(self, state="readonly")
        self.cmbFrom.bind("<<ComboboxSelected>>", self.from_selected)


        # ----------------------------------------------------------------------
        # Buttons
        # ----------------------------------------------------------------------

        self.btnCalc = puc.Button(self,
                                  text = puc.messages["converter.button.calc"],
                                  command = self.calc)

        self.btnCancel = puc.Button(self, text = puc.messages["button.cancel"],
                                    command= lambda: controller.show_frame(puc.Main))


        # ----------------------------------------------------------------------
        # Put labels, coboboxes and entry/textbox to the frame
        # ----------------------------------------------------------------------

        self.lblTitle.grid(row=0, column=0, columnspan=6, sticky="nw", padx=10, pady=15)
        self.lblUnitsList.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        self.cmbUnitsList.grid(row=1, column=2, columnspan=2, padx=10)

        self.lblConverter.grid(row=2, column=0, columnspan=3, sticky="w", pady=10)

        self.txtMultiplier.grid(row=3, column=0)
        self.cmbTo.grid(row=3, column=1, columnspan=2, padx=10)
        puc.Label(self, text="=").grid(row=3, column=3, padx=3)
        self.lblResult.grid(row=3, column=4, pady=5)
        self.cmbFrom.grid(row=3, column=5, padx=10, pady=5)


        # ----------------------------------------------------------------------
        # Put buttons to the frame
        # ----------------------------------------------------------------------

        self.btnCalc.grid(row=4, column=3, columnspan=2, pady=10, sticky="ew")
        self.btnCancel.grid(row=5, column=5, padx=10, pady=20, sticky="se")

        # Reset units list combobox
        self.reset_units_list()
        if controller.df_exists:
            self.cmbUnitsList.current(0)  # select first element
            self.units_list_selected("")


    # --------------------------------------------------------------------------
    # Method for changing frame language
    # --------------------------------------------------------------------------

    def change_lang(self):
        '''Changes frames language.'''
        self.lblTitle.config(text = puc.messages["program.title"] + "  –  "
                    + puc.messages["main.button.convert"].lower())

        self.lblUnitsList.config(text = puc.messages["units.label.units_list"])
        self.lblConverter.config(text = puc.messages["units.label.converter"])
        self.btnCalc.config(text = puc.messages["converter.button.calc"])
        self.btnCancel.config(text = puc.messages["button.cancel"])


    # --------------------------------------------------------------------------
    # Method for calculation
    # --------------------------------------------------------------------------

    def calc(self):
        """Make calculation based on selected unit and multiplier."""
        # Make calculation only then, if both (from and to) units selected
        if self.selected["to"] and self.selected["from"]:
            mult = puc.text2float(self.txtMultiplier.get().strip())
            if mult == 0:
                mult = 1
                self.txtMultiplier.delete(0, puc.END)
                self.txtMultiplier.insert(0, puc.float2text(mult))

            to = self.controller.data[self.selected["list"]][self.selected["to"]]
            frm = self.controller.data[self.selected["list"]][self.selected["from"]]
            self.lblResult["text"] = puc.float2text(round(mult*to/frm, 5))


    # --------------------------------------------------------------------------
    # Methods for comboboxes
    # --------------------------------------------------------------------------

    def reset_units_list(self):
        """Resets units list combobox."""
        self.controller.set_selections(self.uCombos["lists"], self.cmbUnitsList,
                                       self.controller.data, True)

    def units_list_selected(self, evt):
        """Unit list selection (resets units combobox)."""
        self.controller.make_selection(self.selected, "list", self.cmbUnitsList,
                                       "status.selected_list", evt=="", True)
        self.reset_units()


    def reset_units(self):
        """Resets units combobox based on selected list."""
        self.cmbTo.set("")
        self.cmbTo.current(None)
        self.selected["to"] = None
        self.cmbFrom.set("")
        self.cmbFrom.current(None)
        self.selected["from"] = None

        self.controller.set_selections(self.uCombos["tos"], self.cmbTo,
                                       self.controller.data[self.selected["list"]], True)

        self.controller.set_selections(self.uCombos["froms"], self.cmbFrom,
                                       self.controller.data[self.selected["list"]], True)

    def to_selected(self, evt):
        """To unit selection (make calculation automatically)."""
        self.controller.make_selection(self.selected, "to", self.cmbTo,
                                       "status.selected_to", evt=="", True)
        self.calc()

    def from_selected(self, evt):
        """From unit selection (make calculation automatically)."""
        self.controller.make_selection(self.selected, "from", self.cmbFrom,
                                       "status.selected_from", evt=="", True)
        self.calc()
