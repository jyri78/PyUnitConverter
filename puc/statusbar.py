#! /usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

import puc


class Statusbar(puc.Frame):
    """Statusbar object class."""
    def __init__(self, parent: puc.Tk):
        puc.Frame.__init__(self, parent)

        (frmStatus, frmMode) = (puc.Frame(self), puc.Frame(self))
        for obj in (frmStatus, frmMode):
            obj['borderwidth'] = 2
            obj["relief"] = "sunken"
            obj["padx"] = "5"
            obj["pady"] = "2"

        self.lblStatus = puc.Label(frmStatus, text="")
        self.lblStatus.pack(fill = puc.X)

        self.lblMode = puc.Label(
            frmMode,
            text = puc.messages["status.saving_mode"][puc.settings["saving_mode"]+1])

        self.lblMode.state(["disabled"])
        self.lblMode.pack()

        # Finally puts frames with labels to the statusbar
        frmStatus.pack(side="left", fill=puc.X, expand=True)
        frmMode.pack(side="right")

    def set_status(self, message: str):
        """Sets message/text of statusbar.

        Parameter:
            message: text to set to the statusbar
        """
        self.lblStatus.config(text = message)
        self.lblStatus.update_idletasks()

    def del_status(self):
        """Clears statusbar.

        Same as `statusbar.set_status("")`
        """
        self.set_status("")

    def change_mode(self, mode = 0):
        """Changes saving mode status in statusbar.

        Parameter:
            mode: saving mode, integer (one of values 0, 1 or 2)
        """
        if not -1 < mode < 3: mode = 0
        self.set_status(puc.messages["status.saving_mode"][mode])
