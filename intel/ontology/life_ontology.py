# -*- coding: utf-8 -*-
"""
life_ontology.py
Deliverable 1: Universal Life Ontology
Defines all possible human life domains in a hierarchical structure.
Nothing should exist outside this ontology.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class DomainCategory:
    name: str
    code: str
    description: str
    sub_domains: List[str] = field(default_factory=list)
    primary_houses: List[int] = field(default_factory=list)
    primary_karakas: List[str] = field(default_factory=list)

class UniversalLifeOntology:
    """Master ontology mapping all possible user life questions and life domains."""

    DOMAINS: Dict[str, DomainCategory] = {
        "CAREER_AND_PROFESSION": DomainCategory(
            name="Career, Profession & Status",
            code="CAREER",
            description="Job, business, promotion, transfer, government job, authority, public reputation, and career rise or fall.",
            sub_domains=["Government Job", "Private Job", "Promotion", "Transfer", "Business", "Executive Authority", "Public Fame", "Job Loss", "Retirement"],
            primary_houses=[10, 6, 2, 11, 1],
            primary_karakas=["Sun", "Saturn", "Mercury", "Jupiter"]
        ),
        "MARRIAGE_AND_RELATIONSHIPS": DomainCategory(
            name="Marriage, Love & Partnerships",
            code="MARRIAGE",
            description="Marriage timing, spouse characteristics, marital stability, divorce, love affairs, synastry, and partnerships.",
            sub_domains=["Marriage Timing", "Spouse Nature", "Love Affair", "Marital Harmony", "Divorce / Separation", "Second Marriage", "Business Partnerships"],
            primary_houses=[7, 2, 4, 8, 12, 5],
            primary_karakas=["Venus", "Jupiter"]
        ),
        "FINANCE_AND_WEALTH": DomainCategory(
            name="Wealth, Finance & Assets",
            code="WEALTH",
            description="Income, savings, investments, loans, debts, inheritance, sudden wealth, and financial losses.",
            sub_domains=["Income & Gains", "Accumulated Wealth", "Loans & Debts", "Inheritance", "Speculation & Stocks", "Financial Losses", "Bankruptcy"],
            primary_houses=[2, 11, 5, 8, 9, 12],
            primary_karakas=["Jupiter", "Mercury", "Venus"]
        ),
        "PROPERTY_AND_VEHICLES": DomainCategory(
            name="Property, Land & Vehicles",
            code="PROPERTY",
            description="Real estate purchase, home construction, vehicle acquisition, land ownership, and ancestral property.",
            sub_domains=["Home Purchase", "Land Ownership", "Vehicle Acquisition", "Ancestral Property", "Property Litigation"],
            primary_houses=[4, 11, 2, 12],
            primary_karakas=["Mars", "Venus", "Saturn"]
        ),
        "HEALTH_AND_LONGEVITY": DomainCategory(
            name="Health, Longevity & Diseases",
            code="HEALTH",
            description="Physical health, chronic diseases, surgeries, mental health, accidents, hospitalization, and longevity.",
            sub_domains=["General Health", "Chronic Illness", "Surgeries", "Mental Health", "Accidents", "Hospitalization", "Longevity / Death"],
            primary_houses=[1, 6, 8, 12],
            primary_karakas=["Sun", "Mars", "Saturn", "Rahu"]
        ),
        "CHILDREN_AND_FAMILY": DomainCategory(
            name="Children, Progeny & Family",
            code="CHILDREN",
            description="Progeny timing, child health, intelligence, higher learning, and extended family dynamics.",
            sub_domains=["Child Birth", "Progeny Timing", "Child Health", "Family Relations", "Parents Wellbeing"],
            primary_houses=[5, 9, 2, 4],
            primary_karakas=["Jupiter", "Moon", "Sun"]
        ),
        "FOREIGN_TRAVEL_AND_IMMIGRATION": DomainCategory(
            name="Foreign Travel, Settlement & Immigration",
            code="FOREIGN",
            description="Foreign trips, foreign education, PR / Visa approval, overseas settlement, and foreign trade.",
            sub_domains=["Foreign Trips", "Foreign Education", "Permanent Settlement", "Visa Approval", "Foreign Trade"],
            primary_houses=[9, 12, 7, 3],
            primary_karakas=["Rahu", "Saturn", "Jupiter"]
        ),
        "LITIGATION_AND_ENEMIES": DomainCategory(
            name="Litigation, Enemies & Legal Conflicts",
            code="LITIGATION",
            description="Court cases, legal disputes, hidden enemies, victory over rivals, and imprisonment / detention.",
            sub_domains=["Court Cases", "Legal Victory", "Enemies & Rivals", "Imprisonment / Jail", "Disputes"],
            primary_houses=[6, 8, 12],
            primary_karakas=["Mars", "Saturn", "Rahu"]
        ),
        "EDUCATION_AND_KNOWLEDGE": DomainCategory(
            name="Education, Exams & Intellect",
            code="EDUCATION",
            description="Basic schooling, higher education, competitive exams, research, memory, and academic success.",
            sub_domains=["Competitive Exams", "Higher Education", "Research & PhD", "Academic Awards", "Memory & Focus"],
            primary_houses=[4, 5, 9],
            primary_karakas=["Mercury", "Jupiter"]
        ),
        "SPIRITUALITY_AND_MOKSHA": DomainCategory(
            name="Spirituality, Occult & Liberation",
            code="SPIRITUALITY",
            description="Spiritual initiation, mantra siddhi, astrology & occult practice, pilgrimage, and Moksha.",
            sub_domains=["Spiritual Practice", "Occult & Astrology", "Pilgrimage", "Mantra Siddhi", "Moksha / Liberation"],
            primary_houses=[9, 12, 8, 5],
            primary_karakas=["Ketu", "Jupiter", "Saturn"]
        )
    }

    @classmethod
    def get_all_domains(cls) -> List[str]:
        return list(cls.DOMAINS.keys())

    @classmethod
    def find_domain_by_keyword(cls, keyword: str) -> str:
        kw = keyword.lower()
        for code, dom in cls.DOMAINS.items():
            if kw in dom.name.lower() or kw in dom.code.lower():
                return code
            for sub in dom.sub_domains:
                if kw in sub.lower():
                    return code
        return "CAREER_AND_PROFESSION"
