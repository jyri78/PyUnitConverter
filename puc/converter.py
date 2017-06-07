#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

from __future__ import division

import puc


class Converter(puc.Frame):
    def __init__(self, parent: puc.Frame, controller: puc.Tk):
        puc.Frame.__init__(self, parent)

        self.controller = controller

        # Some variables used in methods
        self.unit_lists = []
        self.unit_tos = []
        self.unit_froms = []

        # Variables for remembering selection; list is used for it's mutability
        self.selected_list = [None]
        self.selected_to = [None]
        self.selected_from = [None]


        # ----------------------------------------------------------------------
        # Units List (label, combobox, entry/textbox, button)
        # ----------------------------------------------------------------------

        lblTitle = puc.Label(
            self,
            text = puc.messages["program.title"] + "  –  "
                    + puc.messages["main.button.convert"].lower(),
            style = "LMT.TLabel")

        lblUnitsList = puc.Label(self, text=puc.messages["units.label.units_list"])
        self.cmbUnitsList = puc.Combobox(self, state="readonly")
        self.cmbUnitsList.bind("<<ComboboxSelected>>", self.units_list_selected)


        # ----------------------------------------------------------------------
        # Conversion (label, combobox, entry/textbox, button)
        # ----------------------------------------------------------------------

        lblConverter = puc.Label(self,
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

        btnCancel = puc.Button(self, text = puc.messages["button.cancel"],
                               command= lambda: controller.show_frame(puc.Main))


        # ----------------------------------------------------------------------
        # Put labels, coboboxes and entry/textbox to the frame
        # ----------------------------------------------------------------------

        lblTitle.grid(row=0, column=0, columnspan=6, sticky="nw", padx=10, pady=15)
        lblUnitsList.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        self.cmbUnitsList.grid(row=1, column=2, columnspan=2, padx=10)

        lblConverter.grid(row=2, column=0, columnspan=3, sticky="w", pady=10)

        self.txtMultiplier.grid(row=3, column=0)
        self.cmbTo.grid(row=3, column=1, columnspan=2, padx=10)
        puc.Label(self, text="=").grid(row=3, column=3)
        self.lblResult.grid(row=3, column=4, pady=5)
        self.cmbFrom.grid(row=3, column=5, padx=10, pady=5)


        # ---------------------------------------------------------------------
        # Put buttons to the frame
        # ---------------------------------------------------------------------

        self.btnCalc.grid(row=4, column=3, columnspan=2, pady=10)
        btnCancel.grid(row=5, column=5, padx=5, pady=20, sticky="se")

        # Reset units list combobox
        self.reset_units_list()
        if controller.df_exists:
            self.cmbUnitsList.current(0)  # select first element
            self.units_list_selected("")


    # -------------------------------------------------------------------------
    # Method for calculation
    # -------------------------------------------------------------------------

    def calc(self):
        """Make calculation based on selected unit and multiplier."""
        # Make calculation only then, if both (from and to) units selected
        if self.selected_to[0] and self.selected_from[0]:
            mult = puc.text2float(self.txtMultiplier.get().strip())
            if mult == 0:
                mult = 1
                self.txtMultiplier.delete(0, puc.END)
                self.txtMultiplier.insert(0, puc.float2text(mult))

            to = self.controller.data[self.selected_list[0]][self.selected_to[0]]
            frm = self.controller.data[self.selected_list[0]][self.selected_from[0]]
            self.lblResult["text"] = puc.float2text(round(mult*to/frm, 5))


    # -------------------------------------------------------------------------
    # Methods for comboboxes
    # -------------------------------------------------------------------------

    def reset_units_list(self):
        """Resets units list combobox."""
        self.controller.set_selections(self.unit_lists, self.cmbUnitsList, self.controller.data)

    def units_list_selected(self, evt):
        """Unit list selection (resets units combobox)."""
        self.controller.make_selection(self.selected_list, self.cmbUnitsList, "status.selected_list", evt=="")
        self.reset_units()


    def reset_units(self):
        """Resets units combobox based on selected list."""
        self.cmbTo.set("")
        self.cmbTo.current(None)
        self.selected_to[0] = None
        self.cmbFrom.set("")
        self.cmbFrom.current(None)
        self.selected_from[0] = None

        self.controller.set_selections(self.unit_tos, self.cmbTo,
                                       self.controller.data[self.selected_list[0]])

        self.controller.set_selections(self.unit_froms, self.cmbFrom,
                                       self.controller.data[self.selected_list[0]])

    def to_selected(self, evt):
        """To unit selection (make calculation automatically)."""
        self.controller.make_selection(self.selected_to, self.cmbTo,
                                       "status.selected_to", evt=="")
        self.calc()

    def from_selected(self, evt):
        """From unit selection (make calculation automatically)."""
        self.controller.make_selection(self.selected_from, self.cmbFrom,
                                       "status.selected_from", evt=="")
        self.calc()
