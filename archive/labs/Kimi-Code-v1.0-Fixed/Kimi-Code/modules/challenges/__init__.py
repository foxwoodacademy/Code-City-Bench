"""
Kimi-Code Challenge Types
"""
from .debug_missions import get_missions as get_debug_missions
from .refactor_ops import get_missions as get_refactor_missions
from .security_audits import get_missions as get_security_missions
from .algo_races import get_races as get_algo_races
from .system_design import get_challenges as get_system_designs

CHALLENGE_TYPES = {
    'debug': get_debug_missions,
    'refactor': get_refactor_missions,
    'security': get_security_missions,
    'algo': get_algo_races,
    'algorithm': get_algo_races,
    'system_design': get_system_designs
}

def get_challenges_by_type(challenge_type: str, difficulty_range: tuple = None):
    """Get challenges by type."""
    getter = CHALLENGE_TYPES.get(challenge_type.lower())
    if getter:
        return getter(difficulty_range)
    return []
