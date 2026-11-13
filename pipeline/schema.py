"""Structured output models for a public council record."""
from typing import Literal
from pydantic import BaseModel, Field

StageType = Literal['staff_recommendation', 'committee_decision', 'council_decision']
Outcome = Literal[
    'recommended', 'adopted', 'adopted_with_amendments',
    'received_for_information', 'referred', 'deferred',
    'not_adopted', 'pending', 'unknown',
]

class Stage(BaseModel):
    body: str
    date: str | None
    stage_type: StageType
    outcome: Outcome
    quote: str = Field(description='Verbatim quote showing the outcome; no paraphrase')

class Participation(BaseModel):
    can_still_comment: Literal['yes', 'no', 'not_stated']
    deadline_text: str | None
    how: str | None
    quote: str | None

class Phrase(BaseModel):
    phrase: str
    meaning_here: str
    quote: str

class DecisionCard(BaseModel):
    item_id: str
    title: str
    wards: list[str]
    what_is_proposed: str
    why: str
    who_is_affected: str
    stages: list[Stage]
    conditions: list[str]
    participation: Participation
    procedural_phrases: list[Phrase]
    uncertainties: list[str]
