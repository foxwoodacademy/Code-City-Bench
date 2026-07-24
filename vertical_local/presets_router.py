import json
import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'presets.json')

class Preset(BaseModel):
    id: str | None = None
    name: str
    description: str | None = None
    provider: str = 'openai'
    model: str = 'gpt-4o-mini'
    prompt_template: str | None = None


def _read():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def _write(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@router.get('/')
def list_presets():
    return _read()


@router.post('/')
def create_preset(p: Preset):
    data = _read()
    p.id = p.id or str(uuid.uuid4())
    data.append(p.dict())
    _write(data)
    return p


@router.delete('/{preset_id}')
def delete_preset(preset_id: str):
    data = _read()
    new = [x for x in data if x.get('id') != preset_id]
    if len(new) == len(data):
        raise HTTPException(status_code=404, detail='not found')
    _write(new)
    return {'deleted': preset_id}
