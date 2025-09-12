from dataclasses import dataclass, field
from typing import List

@dataclass
class KnowledgeProfile:
    name: str = ""
    age: str = ""
    background: str = ""
    familiarity_kw: str = ""
    math_eq: int = 0
    programming_comfort: int = 0
    confidence_asking: int = 0
    support_needs: List[str] = field(default_factory=list)
