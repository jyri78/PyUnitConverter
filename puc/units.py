#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

from __future__ import division

import puc


class Units(puc.Frame):
    def __init__(self, parent: puc.Frame, controller: puc.Tk):
        puc.Frame.__init__(self, parent)

        self.controller = controller
        self.data_change = False  # if there has been made change in data

        # Some variables used in methods
        self.unit_lists = []
        self.units = []

        # Variables for remembering selection; list is used for it's mutability
        self.selected_list = [None]
        self.selected_unit = [None]


        # ----------------------------------------------------------------------
        # Units list (label, combobox, entry/textbox, button)
        # ----------------------------------------------------------------------

        self.lblTitle = puc.Label(
            self,
            text = puc.messages["program.title"] + "  –  "
                    + puc.messages["main.button.units"].lower(),
            style = "PUCT.TLabel")

        self.lblUnitsList = puc.Label(self, text=puc.messages["units.label.units_list"])
        self.cmbUnitsList = puc.Combobox(self, state="readonly")
        self.cmbUnitsList.bind("<<ComboboxSelected>>", self.units_list_selected)
        self.txtUnitsList = puc.Entry(self)

        self.lblBaseUnit = puc.Label(self, text=puc.messages["units.label.base"])
        self.txtBaseUnit = puc.Entry(self)

        # Enables/Disables adding button based on length of inputboxes
        self.txtUnitsList.bind(
            "<KeyRelease>",
            lambda evt: self.btnAddUnitsList.state([
                "!disabled" if len(self.txtUnitsList.get().strip()) > 1
                and len(self.txtBaseUnit.get().strip()) > 1 else "disabled"
            ]))
        self.txtBaseUnit.bind(
            "<KeyRelease>",
            lambda evt: self.btnAddUnitsList.state([
                "!disabled" if len(self.txtUnitsList.get().strip()) > 1
                and len(self.txtBaseUnit.get().strip()) > 1 else "disabled"
            ]))

        self.btnAddUnitsList = puc.Button(self, text = puc.messages["button.add"],
                                          command = self.add_units_list)

        self.btnAddUnitsList.state(["disabled"])

        # Allow `Enter`-key in entry/textbox
        self.txtUnitsList.bind("<Return>", lambda evt: self.btnAddUnitsList.invoke())
        self.txtBaseUnit.bind("<Return>", lambda evt: self.btnAddUnitsList.invoke())


        # ----------------------------------------------------------------------
        # Units and multiplier
        # ----------------------------------------------------------------------

        self.lblConverter = puc.Label(self,
                                      text = puc.messages["units.label.converter"],
                                      font = (None, 10, "bold"))

        self.lblUnit = puc.Label(self, text=puc.messages["units.label.unit"])
        self.cmbUnits = puc.Combobox(self, state="readonly")
        self.cmbUnits.bind("<<ComboboxSelected>>", self.unit_selected)

        self.txtUnit = puc.Entry(self)
        self.txtUnit.state(["disabled"])

        # Enables/Disables button based on length of inputbox
        self.txtUnit.bind(
            "<KeyRelease>",
            lambda evt: self.btnAddUnit.state([
                "!disabled" if len(self.txtUnit.get().strip()) > 1 else "disabled"
            ]))

        self.btnAddUnit = puc.Button(self, text = puc.messages["button.add"],
                                     command = self.add_unit)

        self.btnAddUnit.state(["disabled"])

        # Allow `Enter`-key in entry/textbox
        self.txtUnit.bind("<Return>", lambda evt: self.btnAddUnit.invoke())

        self.lblMultiplier = puc.Label(self, text=puc.messages["units.label.multiplier"])
        self.txtMultiplier = puc.Entry(self)
        self.txtMultiplier.state(["disabled"])

        # Enables/Disables button based on length of inputbox, but doesn't
        # allow to change base unit (which is equal to 1.0)
        self.txtMultiplier.bind(
            "<KeyRelease>",
            lambda evt: self.btnAddMultiplier.state([
                "!disabled" if len(self.txtMultiplier.get().strip()) > 0
                        and self.selected_unit[0].lower()
                        != self.controller.data[self.selected_list[0]]["base_unit"]
                    else "disabled"
            ]))

        self.btnAddMultiplier = puc.Button(self, text = puc.messages["button.change"],
                                           command = self.add_multiplier)

        self.btnAddMultiplier.state(["disabled"])

        # Allow `Enter`-key in entry/textbox
        self.txtMultiplier.bind("<Return>", lambda evt: self.btnAddMultiplier.invoke())


        # ----------------------------------------------------------------------
        # Buttons
        # ----------------------------------------------------------------------

        self.btnSave = puc.Button(self, text = puc.messages["units.button.save"],
                                  command = self.save_data)
        self.btnSave.state(["disabled"])

        self.btnCancel = puc.Button(self, text = puc.messages["button.cancel"],
                                    command = self.cancel)


        # ----------------------------------------------------------------------
        # Put units list elements to the frame
        # ----------------------------------------------------------------------

        self.lblTitle.grid(row=0, column=0, columnspan=5, sticky="nw", padx=10, pady=15)
        self.lblUnitsList.grid(row=1, column=0, sticky="w", pady=5)
        self.cmbUnitsList.grid(row=1, column=1, padx=10)
        self.txtUnitsList.grid(row=1, column=2)
        self.btnAddUnitsList.grid(row=1, column=3, padx=10, rowspan=2)

        self.lblBaseUnit.grid(row=2, column=1)
        self.txtBaseUnit.grid(row=2, column=2)


        # ----------------------------------------------------------------------
        # Put units elements to the frame
        # ----------------------------------------------------------------------

        self.lblConverter.grid(row=3, column=0, columnspan=2, sticky="w", pady=10)

        self.lblUnit.grid(row=4, column=0, sticky="w")
        self.cmbUnits.grid(row=4, column=1, padx=10)
        self.txtUnit.grid(row=4, column=2)
        self.btnAddUnit.grid(row=4, column=3, padx=10)

        self.lblMultiplier.grid(row=5, column=0, sticky="w")
        self.txtMultiplier.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        self.btnAddMultiplier.grid(row=5, column=2, pady=5)


        # ----------------------------------------------------------------------
        # Put buttons to the frame
        # ----------------------------------------------------------------------

        self.btnSave.grid(row=6, column=2, padx=20, pady=20)
        self.btnCancel.grid(row=6, column=3, padx=20, pady=20, sticky="se")

        # Reset units list combobox
        self.controller.set_selections(self.unit_lists, self.cmbUnitsList, self.controller.data)
        if controller.df_exists:
            self.cmbUnitsList.current(0) # select first element
            self.units_list_selected("")


    # --------------------------------------------------------------------------
    # Method for changing frame language
    # --------------------------------------------------------------------------

    def change_lang(self):
        self.lblTitle.config(text = puc.messages["program.title"] + "  –  "
                    + puc.messages["main.button.units"].lower())

        self.lblUnitsList.config(text = puc.messages["units.label.units_list"])
        self.lblBaseUnit.config(text = puc.messages["units.label.base"])
        self.btnAddUnitsList.config(text = puc.messages["button.add"])
        self.lblConverter.config(text = puc.messages["units.label.converter"])
        self.lblUnit.config(text = puc.messages["units.label.unit"])
        self.btnAddUnit.config(text = puc.messages["button.add"])
        self.lblMultiplier.config(text = puc.messages["units.label.multiplier"])
        self.btnAddMultiplier.config(text = puc.messages["button.change"])
        self.btnSave.config(text = puc.messages["units.button.save"])
        self.btnCancel.config(text = puc.messages["button.cancel"])


    # --------------------------------------------------------------------------
    # Helper mehtods for repeated actions
    # --------------------------------------------------------------------------

    def add_selection(self, input: puc.Entry, data: dict, selections: list,
                      combobox: puc.Combobox, add_button: puc.Button, s_text,
                      value = {}) -> str:
        """Adds new selection to the combobox and database.

        Parameters:
            input: inputbox from where to take new value
            data: database data (will be saved)
            selections: list to hold selections
            combobox: combobox where to add selection
            add_button: button, with what new value is added
            s_text: text to be added to the statusbar
            value = {}: value to add to the database
        """
        in_val = input.get().strip().capitalize()
        if len(in_val) > 1 and not in_val in data:
            input.delete(0, puc.END)
            data[in_val] = value

            # Selects just added selection
            combobox.set(in_val)
            self.controller.set_selections(selections, combobox, data)
            add_button.state(["disabled"])

            # There was data added and saving mode allows, then we expect saving
            if puc.settings["saving_mode"] > puc.SM_NONE:
                self.controller.unsaved = True

            self.controller.statusbar.set_status(
                puc.messages["status.added_"+s_text] + in_val.lower())
        else:
            self.controller.statusbar.set_status(
                puc.messages["status."+s_text+"_exists"])
        return in_val

    # Disable multiplier inputbox
    def disable_multiplier(self):
        """Clears and disables multiplier entry/textbox."""
        self.txtMultiplier.delete(0, puc.END)
        self.txtMultiplier.state(["disabled"])
        self.btnAddMultiplier.state(["disabled"])

    # Enables button `Save`
    def enable_btnSave(self):
        self.btnSave.state(["!disabled"])
        self.controller.get_frame(puc.Main).btnSave.state(["!disabled"])


    # --------------------------------------------------------------------------
    # Methods for comboboxes
    # --------------------------------------------------------------------------

    def units_list_selected(self, evt):
        """Takes some actions on units list selection."""
        self.controller.make_selection(self.selected_list, self.cmbUnitsList,
                                       "status.selected_list", evt=="")

        self.reset_units()
        self.txtBaseUnit.delete(0, puc.END)

        self.txtBaseUnit.insert(
            0,
            self.controller.data[self.selected_list[0]]["base_unit"])

        # Disable multiplier input since unit is now not selected
        self.disable_multiplier()

    def add_units_list(self):
        """Adds new unit to the combobox."""
        in_val = self.add_selection(self.txtUnitsList, self.controller.data,
                                    self.unit_lists, self.cmbUnitsList,
                                    self.btnAddUnitsList, "list")

        base = self.txtBaseUnit.get().strip().lower()
        self.controller.data[in_val]["base_unit"] = base
        self.txtBaseUnit.delete(0, puc.END)
        self.units_list_selected("")

        # Add automatically base unit also to the units
        self.txtUnit.delete(0, puc.END)
        self.txtUnit.insert(0, base)
        self.add_unit()
        self.controller.data[self.selected_list[0]][self.selected_unit[0]] = 1.0
        self.txtMultiplier.delete(0, puc.END)
        self.txtMultiplier.insert(0, "1,0" if puc.lang["flPoint_comma"] else "1.0")

        # Enables saving button if saving mode allows that
        if puc.settings["saving_mode"] > puc.SM_NONE:
            self.enable_btnSave()


    def reset_units(self):
        """Resets units in combobox."""
        self.cmbUnits.set("")
        self.cmbUnits.current(None)

        self.controller.set_selections(self.units, self.cmbUnits,
                                       self.controller.data[self.selected_list[0]])

        self.txtUnit.state(["!disabled"])

    def unit_selected(self, evt):
        """Takes some actions on unit selection."""
        self.controller.make_selection(self.selected_unit, self.cmbUnits,
                                       "status.selected_unit", evt=="")

        # Update multiplier input value
        self.txtMultiplier.state(["!disabled"])
        self.txtMultiplier.delete(0, puc.END)
        self.txtMultiplier.insert(
            0,
            puc.float2text(
                self.controller.data[self.selected_list[0]][self.selected_unit[0]]
            ))

    def add_unit(self):
        """Adds new unit to the combobox."""
        self.add_selection(self.txtUnit,
                           self.controller.data[self.selected_list[0]],
                           self.units, self.cmbUnits,
                           self.btnAddUnit, "unit", 0)

        self.unit_selected("")


    # --------------------------------------------------------------------------
    # Adding multiplier
    # --------------------------------------------------------------------------

    def add_multiplier(self):
        """Adds/Changes unit multiplier in database."""
        flt = puc.text2float(self.txtMultiplier.get())
        self.controller.data[self.selected_list[0]][self.selected_unit[0]] = flt

        # Adjusts inputs value
        s_number = puc.float2text(flt)
        self.txtMultiplier.delete(0, puc.END)
        self.txtMultiplier.insert(0, s_number)

        # Data was added and if saving mode allows, then we expect saving
        if puc.settings["saving_mode"] > puc.SM_NONE:
            self.controller.unsaved = True
            self.enable_btnSave()

        # If there are no datafile, then now conversion button in main frame
        # can be enabled
        self.controller.get_frame(puc.Main).btnConvert.state(["!disabled"])

        self.controller.statusbar.set_status(
            puc.messages["status.added_multiplier"] + s_number)


    # -------------------------------------------------------------------------
    # Saving database
    # -------------------------------------------------------------------------

    def save_data(self):
        """Saves datafile."""
        self.controller.save_data()
        self.controller.show_frame(puc.Main)


    # -------------------------------------------------------------------------
    # Closing frame
    # -------------------------------------------------------------------------

    def cancel(self):
        """Closes units adding/changing frame (raises main frame)."""
        self.controller.get_frame(puc.Converter).reset_units_list()
        self.controller.show_frame(puc.Main)
