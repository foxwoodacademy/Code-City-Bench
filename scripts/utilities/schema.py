"""
VERTICAL AI — Shared Schema
Universal data contract between scouts, conductor, boardroom, and outreach.
Every module speaks this language. Code City maps this graph.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime
import json


@dataclass
class CFPBComplaint:
    product: str
    issue: str
    state: str
    narrative: str
    date_received: Optional[str] = None


@dataclass
class WebSignal:
    title: str
    url: str
    snippet: str
    source: str


@dataclass
class ScoutTarget:
    """
    A single intelligence target.
    Output of scouts. Input to conductor.
    """
    name: str
    category: str
    source: str                          # "google_business" | "manual" | "cfpb" | "web"

    # Identity
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    has_website: bool = False

    # Market signals
    rating: Optional[float] = None
    review_count: Optional[int] = None
    price_tier: Optional[str] = None     # "$" | "$$" | "$$$"

    # Intelligence
    cfpb_complaints: list = field(default_factory=list)
    web_signals: list = field(default_factory=list)
    risk_flags: list = field(default_factory=list)
    opportunity_flags: list = field(default_factory=list)

    # Meta
    scouted_at: str = field(default_factory=lambda: datetime.now().isoformat())
    scout_version: str = "1.0"

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_conductor_context(self) -> dict:
        """Format for direct injection into Vertical AI conductor."""
        return {
            "type": "scrape",
            "label": f"{self.name} — {self.category}",
            "data": self.to_dict(),
            "raw": self.to_json()
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ScoutTarget":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class OutreachPayload:
    """
    Champion strategy → outreach agent input.
    Output of Vertical AI. Input to outreach agents.
    """
    session_id: str
    target_name: str
    champion_thesis: str
    first_action: str

    subject_line: str = ""
    hook: str = ""
    value_proposition: str = ""
    pain_point: str = ""
    call_to_action: str = ""
    tone: str = "consultative"

    email_body: str = ""
    linkedin_body: str = ""
    sms_body: str = ""

    objection_no_budget: str = ""
    objection_not_interested: str = ""
    objection_have_someone: str = ""

    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
