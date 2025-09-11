# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:11:10 2025

@author: maxyo
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from core.db import init_db, save_profile, load_profiles
from core.questionnaire import LearnerProfile
from core.agent import reply
from core.graphvisualization import create_graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Profile Creation Window ----------------
class ProfileWindow(tk.Toplevel):
    def __init__(self, master, db_path, refresh_callback):
        super().__init__(master)
        self.title("Créer un profil")
        self.db_path = db_path
        self.refresh_callback = refresh_callback

        self.sliders = {}
        self.text_entries = {}

        # --- numeric fields ---
        numeric_fields = [
            ("prereq_level", "Niveau de prérequis"),
            ("granularity", "Granularité"),
            ("cognitive_load_tol", "Charge cognitive tolérée"),
            ("formalism_first", "Préférence formalisation"),
            ("checkpoint_freq", "Fréquence checkpoints")
        ]

        row = 0
        ttk.Label(self, text="Nom :").grid(row=row, column=0, sticky="nw", padx=5, pady=5)
        self.expert_name = tk.Text(self, width=40, height=1)
        self.expert_name.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        for key, label in numeric_fields:
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            var = tk.DoubleVar(value=0.5)
            slider = ttk.Scale(self, from_=0, to=1, orient="horizontal", variable=var)
            slider.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            self.sliders[key] = var
            row += 1

        # --- vector groups ---
        vector_groups = {
            "analogy_vector": ["mechanical", "financial", "biological"],
            "modality_pref": ["text", "code", "tables"],
            "motivation": ["project", "exam", "curiosity"]
        }

        for group, keys in vector_groups.items():
            ttk.Label(self, text=f"{group}").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            frame = ttk.Frame(self)
            frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            row += 1
            self.sliders[group] = {}
            for k in keys:
                ttk.Label(frame, text=k).pack(anchor="w")
                var = tk.DoubleVar(value=0.5)
                s = ttk.Scale(frame, from_=0, to=1, orient="horizontal", variable=var, length=150)
                s.pack(fill="x", pady=2)
                self.sliders[group][k] = var

        # --- dropdown for main_field ---
        ttk.Label(self, text="Domaine principal").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.main_field_var = tk.StringVar()
        fields = ["Chimie","Physique","Mathématiques","Informatique","Sciences des matériaux","Biologie","Économie","Autre"]
        field_menu = ttk.Combobox(self, textvariable=self.main_field_var, values=fields, state="readonly")
        field_menu.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # --- text for expertise ---
        ttk.Label(self, text="Expertise / connaissances actuelles").grid(row=row, column=0, sticky="nw", padx=5, pady=5)
        self.domain_expertise_text = tk.Text(self, width=40, height=5)
        self.domain_expertise_text.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # --- save button ---
        save_btn = ttk.Button(self, text="Enregistrer le profil", command=self.save_profile)
        save_btn.grid(row=row, column=0, columnspan=2, pady=10)

    def save_profile(self):
        prof = LearnerProfile(
            name=self.expert_name.get("1.0","end").strip(),
            prereq_level=self.sliders["prereq_level"].get(),
            granularity=self.sliders["granularity"].get(),
            cognitive_load_tol=self.sliders["cognitive_load_tol"].get(),
            analogy_vector={k:v.get() for k,v in self.sliders["analogy_vector"].items()},
            modality_pref={k:v.get() for k,v in self.sliders["modality_pref"].items()},
            formalism_first=self.sliders["formalism_first"].get(),
            checkpoint_freq=self.sliders["checkpoint_freq"].get(),
            motivation={k:v.get() for k,v in self.sliders["motivation"].items()},
            main_field=self.main_field_var.get(),
            domain_expertise=self.domain_expertise_text.get("1.0","end").strip()
        )
        rid = save_profile(prof, self.db_path)
        messagebox.showinfo("Profil", f"Profil enregistré avec ID {rid}")
        self.refresh_callback()
        self.destroy()

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

# ---------------- Main App ----------------
class LearnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learning Style Manager")
        self.db_path = None
        self.project_name = "Projet"

        # --- project frame ---
        project_frame = ttk.LabelFrame(root, text="Projet")
        project_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(project_frame, text="Créer un projet", command=self.create_project).pack(side="left", padx=5, pady=5)
        ttk.Button(project_frame, text="Ouvrir un projet", command=self.open_project).pack(side="left", padx=5, pady=5)
        ttk.Button(project_frame, text="Carte des profils", command=self.show_bubble_map).pack(side="left", padx=5, pady=5)

        # --- profiles frame ---
        self.profile_frame = ttk.LabelFrame(root, text="Profils")
        self.profile_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.profile_list = tk.Listbox(self.profile_frame)
        self.profile_list.pack(fill="both", expand=True, padx=5, pady=5)

        btn_frame = ttk.Frame(self.profile_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Ajouter un profil", command=self.add_profile).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Sélectionner un profil", command=self.select_profile).pack(side="left", padx=5)

    def create_project(self):
        fname = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite DB","*.db")])
        if fname:
            init_db(fname)
            self.db_path = fname
            self.project_name = fname.split("/")[-1].replace(".db","")
            self.refresh_profiles()
            messagebox.showinfo("Projet", f"Projet créé: {fname}")

    def open_project(self):
        fname = filedialog.askopenfilename(filetypes=[("SQLite DB","*.db")])
        if fname:
            self.db_path = fname
            self.project_name = fname.split("/")[-1].replace(".db","")
            init_db(fname)
            self.refresh_profiles()
            messagebox.showinfo("Projet", f"Projet ouvert: {fname}")

    def refresh_profiles(self):
        if not self.db_path: return
        self.profile_list.delete(0, tk.END)
        for rid, prof in load_profiles(self.db_path):
            self.profile_list.insert(tk.END, f"ID {rid} | {prof['name']} | Domaine: {prof['main_field']} | Prérequis: {prof['prereq_level']:.2f}")

    def add_profile(self):
        if not self.db_path:
            messagebox.showerror("Erreur", "Ouvrez ou créez d'abord un projet.")
            return
        ProfileWindow(self.root, self.db_path, self.refresh_profiles)

    def select_profile(self):
        selection = self.profile_list.curselection()
        if not selection:
            messagebox.showwarning("Sélection", "Choisissez un profil dans la liste.")
            return
        index = selection[0]
        rid, prof = load_profiles(self.db_path)[index]
        ChatWindow(self.root, rid, prof)

    def show_bubble_map(self):
        if not self.db_path:
            messagebox.showerror("Erreur", "Ouvrez un projet avant d'afficher la carte.")
            return
        profiles = load_profiles(self.db_path)
        if not profiles:
            messagebox.showwarning("Carte vide", "Aucun profil enregistré.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Carte des profils - {self.project_name}")
        win.geometry("1200x900")

        fig = create_graph(profiles, self.project_name)
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
