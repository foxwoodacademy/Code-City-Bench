"""
Kimi-Code Difficulty Tiers
"""
from .novice import get_tier_config as get_novice_config
from .apprentice import get_tier_config as get_apprentice_config
from .journeyman import get_tier_config as get_journeyman_config
from .expert import get_tier_config as get_expert_config
from .master import get_tier_config as get_master_config
from .architect import get_tier_config as get_architect_config

TIER_MAP = {
    'novice': get_novice_config,
    'apprentice': get_apprentice_config,
    'journeyman': get_journeyman_config,
    'expert': get_expert_config,
    'master': get_master_config,
    'architect': get_architect_config
}

def get_tier_config(tier: str) -> dict:
    """Get configuration for a difficulty tier."""
    getter = TIER_MAP.get(tier.lower())
    if getter:
        return getter()
    return {}

def get_all_tiers() -> list:
    return list(TIER_MAP.keys())
