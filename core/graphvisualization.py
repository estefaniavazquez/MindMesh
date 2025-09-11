# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 14:30:19 2025

@author: maxyo
"""

import networkx as nx
import matplotlib.pyplot as plt

def create_graph(profiles, project_name="Projet"):
    """
    Retourne une figure matplotlib représentant les profils.
    profiles: liste (id, profil_dict)
    """
    G = nx.Graph()
    G.add_node("Projet", size=5000, group="Projet")

    domain_nodes = {}
    for _, prof in profiles:
        domain = prof["main_field"] or "Autre"
        if domain not in domain_nodes:
            domain_nodes[domain] = []
            G.add_node(domain, size=4000, group="Domaine")
            G.add_edge("Projet", domain)

        size = 100 + prof["prereq_level"] * 2500
        label = f"{prof['name']}\n({prof['prereq_level']:.2f})"
        G.add_node(label, size=size, group="Profil")
        G.add_edge(domain, label)

    pos = nx.spring_layout(G, k=0.5, iterations=500, center=(0,0))
    pos["Projet"] = (0,0)

    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_title(f"Carte des profils - {project_name}")
    ax.axis("off")

    sizes = [G.nodes[n].get("size", 500) for n in G.nodes()]
    colors = []
    for n in G.nodes():
        g = G.nodes[n].get("group","Profil")
        if g == "Projet": colors.append("red")
        elif g == "Domaine": colors.append("lightblue")
        else: colors.append("lightgreen")

    nx.draw_networkx(
        G, pos, ax=ax,
        with_labels=True,
        node_size=sizes,
        node_color=colors,
        font_size=7,
        font_weight="bold",
        edge_color="gray",
        alpha=0.8
    )
    return fig