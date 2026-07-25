from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from datetime import datetime

@dataclass
class DashaPeriod:
    start_year: float
    end_year: float
    start_date: datetime
    end_date: datetime
    age_start: float
    age_end: float
    duration_years: float
    lord: str
    is_current: bool = False
    is_upcoming: bool = False
    period_quality: str = "Neutral"
    lord_strength: float = 0.0
    life_domains: List[str] = field(default_factory=list)
    sub_periods: List['DashaPeriod'] = field(default_factory=list)
    applicable: bool = True
    applicability_reason: str = "Default"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start_year": self.start_year,
            "end_year": self.end_year,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "age_start": self.age_start,
            "age_end": self.age_end,
            "duration_years": self.duration_years,
            "lord": self.lord,
            "is_current": self.is_current,
            "is_upcoming": self.is_upcoming,
            "period_quality": self.period_quality,
            "lord_strength": self.lord_strength,
            "life_domains": self.life_domains,
            "sub_periods": [sp.to_dict() for sp in self.sub_periods],
            "applicable": self.applicable,
            "applicability_reason": self.applicability_reason
        }
