# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:11:10 2025

@author: maxyo
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db.db_management import init_db, load_profiles
from llm.graphvisualization import create_graph
from ui.tkinter.secondary.chat_ui import ChatWindow
from ui.tkinter.secondary.profile_creation_ui import ProfileWindow
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
