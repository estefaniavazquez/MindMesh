# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 14:06:48 2025

@author: maxyo
"""

def reply(profile, message: str) -> str:
    """
    Fonction de réponse de l’agent.
    Pour l’instant c’est un stub, mais tu peux brancher un vrai LLM ici.
    """
    return f"[Stub Agent] J’ai reçu: «{message}» (profil {profile['main_field']})"