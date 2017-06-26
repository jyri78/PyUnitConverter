#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

import puc


class Program(puc.Tk):
    """Main program class for dealing user GUI.
    """
    def __init__(self, *args, **kwargs):
        puc.Tk.__init__(self, *args, **kwargs)

        # Create style for titles in frames
        puc.Style().configure("PUCT.TLabel", foreground="darkgreen",
                              font = (None, 13, "bold"))

        # Create style for language name in main frame
        puc.Style().configure("PUCL.TLabel", foreground="blue",
                              font = (None, 9, "italic"))

        # Set program titlebar title and icon
        # (ignore icon load error, not mandatory)
        puc.Tk.wm_title(self, "PyUnitConverter  –  v" + puc.__version__)
        try:
            puc.Tk.wm_iconbitmap(self, bitmap = puc.puc_icon)
        except: pass

        #self.geometry("600x400+200+100")
        self.resizable(False, False)

        # Take control over program closing
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Set some variables needed in program
        self.df_exists = puc.exists(puc.datafile)
        self.data = {}
        self.u_langs = {}
        self.frames = {}
        self.unsaved = False

        # Container for other frames
        container = puc.Frame(self, padx=10, pady=10)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.statusbar = puc.Statusbar(self)
        self.statusbar.pack(side = "bottom", fill = puc.X)

        # If there is datafile, then read it, otherwise set statusbar no
        # datafile message
        if self.df_exists:
            self.data = puc.read_data(puc.datafile)

            # If database file version >1, then make some conversions
            if puc.db_file_ver[-1:] != "":
                self.u_langs["lang"] = self.data["units_lang"]
                self.u_langs["translations"] = self.data["translations"]
                self.data = self.data["units"]
        else:
            if puc.db_file_ver[-1:] != "":
                self.u_langs = {
                    "units_lang": puc.settings["lang"],
                    "translations": {}}

            self.statusbar.set_status(puc.messages["status.no_datafile"])

        # Load all frames in to variable
        for F in (puc.Main, puc.Converter, puc.Units):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Finally show main frame
        self.show_frame(puc.Main)


    def show_frame(self, contr: puc.Frame):
        """Shows user GUI frame (raises it)

        Parameter:
            contr: controller name to raise
        """
        self.frames[contr].tkraise()

    def get_frame(self, contr: puc.Frame) -> puc.Frame:
        """Returns frame corresponding to the controller

        Parameter:
            contr: controller name
        """
        return self.frames[contr]


    def change_lang(self, evt):
        puc.settings["lang"] = self.frames[puc.Main].cmbLang.get()
        puc.load_lang()

        for F in self.frames:
            self.frames[F].change_lang()


    def save_data(self):
        """Saves data to the file."""
        if puc.db_file_ver[-1:] != "":
            data = {
                "units_lang": self.u_langs["lang"],
                "units": self.data,
                "translations": self.u_langs[""]}
        else:
            data = self.data

        puc.save_data(puc.datafile, data)
        self.unsaved = False  # datafile saved
        self.frames[puc.Main].btnSave.state(["disabled"])
        self.frames[puc.Units].btnSave.state(["disabled"])
        self.statusbar.set_status(puc.messages["status.data_saved"])

    def close(self):
        """Manages program closing.

        If there should be unsaved data, then informs about this user.
        """
        if self.unsaved:
            if puc.msgBox.askyesno(
                    title = puc.messages["program.err.title"], icon = "question",
                    message = puc.messages["program.err.text"]):
                puc.save_data(puc.settings_file, puc.settings, puc.SM_JSON)
                self.destroy()
        else:
            # If no unsaved data, then don't bother user
            puc.save_data(puc.settings_file, puc.settings, puc.SM_JSON)
            self.destroy()


    # -------------------------------------------------------------------------
    # Methods for different frames of GUI (repeated actions)
    # -------------------------------------------------------------------------

    def set_selections(self, selections: list, combo: puc.Combobox, data: dict):
        """Adds selections to the combobox.

        Parameters:
            selections: list for selections
            combo: combobox where to add selections
            data: dictionary from where to get selections
        """
        selections = []
        if data:
            # For selections we use dictionary keys
            for d in data:
                if d != "base_unit":
                    selections += [d]

        # Finally adds sorted list to the combobox
        combo["values"] = sorted(selections)

    def make_selection(self, selection: dict, sel: str, combo: puc.Combobox,
                       status_text: str, no_status = False):
        """Saves user selection and informs in statusbar if allowed.

        Parameters:
            selection: variable to remember selection
            combo: combobox where selection was made
            status_text: text to show in statusbar
            no_status: don't add text to the statusbar
        """
        selection[sel] = combo.get()
        if not no_status:
            self.statusbar.set_status(puc.messages[status_text] + selection[sel].lower())
