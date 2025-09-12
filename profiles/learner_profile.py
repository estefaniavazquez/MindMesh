from dataclasses import dataclass


@dataclass
class LearnerProfile:
    goal_understanding: int = 0
    problematic: str = ""
    explanation_style: str = ""
    precision_level: int = 0
    analogies: int = 0
    conciseness: int = 0
    interactivity: str = ""
    tone: str = ""
    humor: str = ""
    motivation: str = ""
    learning_mode: int = 0
    adaptability: str = ""

