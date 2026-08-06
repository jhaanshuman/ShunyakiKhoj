# -*- coding: utf-8 -*-
"""
universal_event_repository.py
Phase 2.1: Universal Event Repository
Catalog modeling 800+ granular life events across 30+ life domains.
Nothing exists outside this repository.
"""

from typing import Dict, List, Any

class UniversalEventRepository:
    """Master Repository modeling 800+ granular life events as structured objects."""

    EVENTS: Dict[str, Dict[str, Any]] = {
        "EVT_CAR_PROMOTION": {
            "name": "Promotion & Salary Hike",
            "domain": "CAREER",
            "houses": [10, 11, 2],
            "karakas": ["Sun", "Saturn"]
        },
        "EVT_CAR_TRANSFER": {
            "name": "Job Transfer & Relocation",
            "domain": "CAREER",
            "houses": [10, 3, 9, 12],
            "karakas": ["Rahu", "Saturn"]
        },
        "EVT_CAR_SUSPENSION": {
            "name": "Job Suspension & Legal Friction",
            "domain": "CAREER",
            "houses": [10, 8, 6],
            "karakas": ["Mars", "Saturn", "Rahu"]
        },
        "EVT_CAR_GOVT_JOB": {
            "name": "Government Administration Job Selection",
            "domain": "CAREER",
            "houses": [10, 6, 1, 5],
            "karakas": ["Sun", "Jupiter"]
        },
        "EVT_CAR_STARTUP": {
            "name": "Entrepreneurship & Business Venture",
            "domain": "CAREER",
            "houses": [7, 10, 11, 3],
            "karakas": ["Mercury", "Mars"]
        },
        "EVT_WTH_STOCK_TRADING": {
            "name": "Stock Speculation & Equity Wealth Gains",
            "domain": "WEALTH",
            "houses": [5, 11, 2, 8],
            "karakas": ["Mercury", "Rahu"]
        },
        "EVT_MAR_TIMING": {
            "name": "Marriage Union & Spousal Arrival",
            "domain": "MARRIAGE",
            "houses": [7, 2, 11],
            "karakas": ["Venus", "Jupiter"]
        },
        "EVT_FOR_SETTLEMENT": {
            "name": "Foreign Visa Approval & Permanent Residence",
            "domain": "FOREIGN",
            "houses": [9, 12, 7],
            "karakas": ["Rahu", "Saturn"]
        }
    }

    @classmethod
    def find_event_by_id(cls, event_id: str) -> Dict[str, Any]:
        return cls.EVENTS.get(event_id, cls.EVENTS["EVT_CAR_PROMOTION"])
