#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

import puc


class Translation(puc.Frame):
    """Translation frame object class."""
    def __init__(self, parent: puc.Frame, controller: puc.Tk):
        puc.Frame.__init__(self, parent)
        
        self.controller = controller
        
        # Variable for remembering selections
        self.selected = {"word": None, "lang": None}

        self.lblTitle = puc.Label(
            self,
            text = puc.messages["program.title"] + "  –  "
                    + puc.messages["main.button.translate"].lower(),
            style="PUCT.TLabel")


        # Listbox and scrollbar

        self.lstWords = puc.Listbox(self, height=12, width=25, selectmode=puc.SINGLE)
        scrWords = puc.Scrollbar(self, orient = puc.VERTICAL,
                                 command = self.lstWords.yview)

        self.lstWords["yscrollcommand"] = scrWords.set
        #self.get_words()
        self.lstWords.bind("<<ListboxSelect>>", self.word_selected)
        self.get_words()


        # Other elements (labels, combobox, textbox and buttons)

        self.lblLang = puc.Label(
            self,
            text = puc.messages["translation.label.to_lang"])

        self.cmbLang = puc.Combobox(self, state="readonly", width=2)
        lngs = []
        for l in puc.langs:
            if not l == self.controller.u_langs["lang"]:
                lngs += [l]

        self.cmbLang["values"] = lngs
        self.cmbLang.bind("<<ComboboxSelected>>", self.lang_selected)

        self.lblTranslation = puc.Label(
            self,
            text = puc.messages["translation.label.translation"])

        self.txtTranslation = puc.Entry(self)
        self.txtTranslation.bind(
            "<KeyRelease>",
            lambda evt: self.btnUpdate.state([
                "!disabled" if len(self.txtTranslation.get().strip()) > 1 else "disabled"
            ]))

        self.btnUpdate = puc.Button(self, text = puc.messages["button.change"],
                                    command = self.update_translation)
        self.btnUpdate.state(["disabled"])

        # Allow `Enter`-key in entry/textbox
        self.txtTranslation.bind("<Return>", lambda evt: self.btnUpdate.invoke())
        self.txtTranslation.bind("<Key-Down>", self.key_down)
        self.txtTranslation.bind("<Key-Up>", self.key_up)

        self.btnSave = puc.Button(self, text = puc.messages["button.save"],
                                  command = self.save_data)
        self.btnSave.state(["disabled"])

        self.btnCancel = puc.Button(self, text = puc.messages["button.cancel"],
                                    command = self.cancel)


        # ----------------------------------------------------------------------
        # Put elements to the frame
        # ----------------------------------------------------------------------

        self.lblTitle.grid(row=0, column=0, columnspan=6, sticky="nw", padx=10, pady=15)
        self.lstWords.grid(row=1, column=0, rowspan=5, pady=5, sticky="nesw")
        scrWords.grid(row=1, column=1, rowspan=5, pady=5, sticky="nsw")
        self.lblLang.grid(row=1, column=2, padx=5, pady=5, sticky="ne")
        self.cmbLang.grid(row=1, column=3, padx=5, pady=5, sticky="nw")
        self.lblTranslation.grid(row=2, column=2, padx=5, sticky="es")
        self.txtTranslation.grid(row=2, column=3, padx=5, sticky="sw")
        self.btnUpdate.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="new")
        self.btnSave.grid(row=4, column=5, padx=20, pady=5, sticky="e")
        self.btnCancel.grid(row=5, column=5, padx=20, pady=5, sticky="se")


    # --------------------------------------------------------------------------
    # Method for changing frame language
    # --------------------------------------------------------------------------

    def change_lang(self):
        '''Changes frames language.'''
        self.lblTitle.config(text = puc.messages["program.title"] + "  –  "
                    + puc.messages["main.button.translate"].lower())

        self.lblLang.config(text = puc.messages["translation.label.to_lang"])
        self.lblTranslation.config(text = puc.messages["translation.label.translation"])
        self.btnUpdate.config(text = puc.messages["button.change"])
        self.btnSave.config(text = puc.messages["button.save"])
        self.btnCancel.config(text = puc.messages["button.cancel"])


    # --------------------------------------------------------------------------
    # Methods for navigation in listbox
    # --------------------------------------------------------------------------

    def _keyUpDwn(self, curIndx, nxtIndx):
        self.lstWords.selection_clear(curIndx)
        self.lstWords.selection_set(nxtIndx)
        self.lstWords.see(nxtIndx)
        #self.lstWords.selection_anchor(nxtIndx)
        self.lstWords.event_generate("<<ListboxSelect>>")

    def key_down(self, evt):
        '''Selects next item in listbox.'''
        curIndex = self.lstWords.curselection()

        if not len(curIndex):
            self._keyUpDwn(-1, 0)
        elif curIndex[0]+1 < self.lstWords.size():
            self._keyUpDwn(curIndex[0], curIndex[0]+1)

    def key_up(self, evt):
        '''Selects previous item in listbox.'''
        curIndex = self.lstWords.curselection()

        if not len(curIndex):
            self._keyUpDwn(0, self.lstWords.size()-1)
        elif curIndex[0] > 0:
            self._keyUpDwn(curIndex[0], curIndex[0]-1)


    # --------------------------------------------------------------------------
    # Helper methods
    # --------------------------------------------------------------------------

    def get_words(self):
        '''Gets all unit names for translation.'''
        words = []
        for unit_list in self.controller.data:
            self.lstWords.insert(puc.END, unit_list)
            for unit in self.controller.data[unit_list]:
                if not unit == "base_unit":
                    self.lstWords.insert(puc.END, unit)


    def get_translation(self):
        '''If there is translation, then add it to the textbox.'''
        self.txtTranslation.delete(0, puc.END)
        if self.selected["word"] and self.selected["lang"]:
            word = self.selected["word"]
            lang = self.selected["lang"]

            if lang in self.controller.u_langs["translations"]:
                if word in self.controller.u_langs["translations"][lang]:
                    self.txtTranslation.insert(
                        0,
                        self.controller.u_langs["translations"][lang][word])

    def update_translation(self):
        '''Adds/Changes translation for unit names.'''
        if self.selected["word"] and self.selected["lang"]:
            word = self.selected["word"]
            lang = self.selected["lang"]
            transl = self.txtTranslation.get().strip().capitalize()
            self.controller.u_langs["translations"][lang][word] = transl
            self.txtTranslation.delete(0, puc.END)
            self.txtTranslation.insert(0, transl)

            if puc.settings["saving_mode"] > puc.SM_NONE:
                self.controller.unsaved = True
                self.enable_btnSave()


    def lang_selected(self, evt):
        '''Take some actions on language selection.'''

        # Put selection back, if there is any
        if hasattr(self, "_index") and len(self._index):
            self.lstWords.selection_set(self._index)

        self.selected["lang"] = self.cmbLang.get()
        self.get_translation()

    def word_selected(self, evt):
        '''Take some actions on word selection.'''
        # By unknown reason selecting lang removes selection from listbox
        if len(self.lstWords.curselection()):
            self._index = self.lstWords.curselection()
            self.selected["word"] = self.lstWords.get(self._index)
            self.get_translation()
        else:
            self._index = ()
            self.txtTranslation.delete(0, puc.END)


    def enable_btnSave(self):
        '''Enables button `Save`.'''
        self.btnSave.state(["!disabled"])
        self.controller.get_frame(puc.Main).btnSave.state(["!disabled"])


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
        """Closes translation frame (raises main frame)."""
        self.controller.get_frame(puc.Converter).reset_units_list()
        self.controller.show_frame(puc.Main)
