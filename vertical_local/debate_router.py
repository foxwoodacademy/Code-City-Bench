import os
import json
from typing import List
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from debate_engine import run_debate
from reports import render_report

router = APIRouter()
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'personas.json')

class DebateRequest(BaseModel):
    title: str | None = None
    case_text: str
    persona_ids: List[str] | None = None
    turns: int | None = 3
    sims: int | None = 25
    use_thoth: bool | None = False
    use_scouts: bool | None = False


def _read_personas():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


@router.post('/')
def start_debate(req: DebateRequest):
    personas = _read_personas()
    if req.persona_ids:
        personas = [p for p in personas if p.get('id') in req.persona_ids]
    if not personas:
        # seed with three archetypes if none
        personas = [
            {'id':'p1','name':'Chair - Strategic','role':'Chair','bio':'Focus on high-level strategy','strategy':'prioritize long-term growth'},
            {'id':'p2','name':'CFO - Metrics','role':'CFO','bio':'Focus on numbers','strategy':'optimize margins'},
            {'id':'p3','name':'CTO - Technical','role':'CTO','bio':'Focus on tech debt','strategy':'modernize stack'},
        ]

    report = run_debate(case_text=req.case_text, personas=personas, turns=req.turns or 3, sims=req.sims or 25, use_thoth=bool(req.use_thoth), use_scouts=bool(req.use_scouts))
    html = render_report(report)
    return Response(content=html, media_type='text/html')
