# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:33:15 2025

@author: maxyo
"""

import tkinter as tk
from tkinter import ttk
from core.agent import reply

# ---------------- Chat Window ----------------
class ChatWindow(tk.Toplevel):
    def __init__(self, master, learner_id, profile):
        super().__init__(master)
        self.title(f"Chat - Profil {learner_id}")
        self.geometry("500x600")

        self.learner_id = learner_id
        self.profile = profile

        self.chat_history = tk.Text(self, wrap="word", state="disabled", bg="white")
        self.chat_history.pack(fill="both", expand=True, padx=5, pady=5)

        entry_frame = ttk.Frame(self)
        entry_frame.pack(fill="x", padx=5, pady=5)

        self.user_input = ttk.Entry(entry_frame)
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.user_input.bind("<Return>", self.send_message)

        send_btn = ttk.Button(entry_frame, text="Envoyer", command=self.send_message)
        send_btn.pack(side="right")

        self._append_message("System", f"Chat lancé pour {profile['main_field']} | Prérequis: {profile['prereq_level']:.2f}")

    def _append_message(self, sender, message):
        self.chat_history.config(state="normal")
        self.chat_history.insert("end", f"{sender}: {message}\n")
        self.chat_history.config(state="disabled")
        self.chat_history.see("end")

    def send_message(self, event=None):
        msg = self.user_input.get().strip()
        if not msg:
            return
        self._append_message("Vous", msg)
        self.user_input.delete(0, "end")
        reply_text = reply(self.profile, msg)   # calls backend agent
        self._append_message("Agent", reply_text)