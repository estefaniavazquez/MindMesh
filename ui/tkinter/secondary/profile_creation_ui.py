# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:28:24 2025

@author: maxyo
"""

import tkinter as tk
from db.db_management import save_profile
from llm.questionnaire import LearnerProfile

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