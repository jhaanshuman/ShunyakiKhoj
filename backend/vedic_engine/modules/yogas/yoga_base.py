from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class YogaResult:
    id: str
    name: str
    sanskrit: str
    category: str
    source_text: str
    chapter: str
    verse: str
    is_active: bool
    strength: float
    confidence: float
    rules_matched: List[str] = field(default_factory=list)
    cancelling_conditions: List[str] = field(default_factory=list)
    affected_domains: List[str] = field(default_factory=list)
    evidence_chain: List[str] = field(default_factory=list)

class YogaEvaluator:
    """Base class for all yoga evaluators."""
    def evaluate(self, master_obj: Dict[str, Any]) -> List[YogaResult]:
        raise NotImplementedError("Subclasses must implement evaluate method")
