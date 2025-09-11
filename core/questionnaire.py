# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 14:02:32 2025

@author: maxyo
"""

from dataclasses import dataclass, asdict


# --- Profil
@dataclass
class LearnerProfile:
    name: str
    prereq_level: float
    granularity: float
    cognitive_load_tol: float
    analogy_vector: dict
    modality_pref: dict
    formalism_first: float
    checkpoint_freq: float
    motivation: dict
    main_field: str

# class KnowledgeProfile:
#     domaine: str