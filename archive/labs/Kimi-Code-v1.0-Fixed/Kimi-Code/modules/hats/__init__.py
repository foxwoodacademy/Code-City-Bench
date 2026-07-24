"""
Kimi-Code Six Thinking Hats Modules
"""
from .white_hat import get_challenges as get_white_challenges
from .red_hat import get_challenges as get_red_challenges
from .black_hat import get_challenges as get_black_challenges
from .yellow_hat import get_challenges as get_yellow_challenges
from .green_hat import get_challenges as get_green_challenges
from .blue_hat import get_challenges as get_blue_challenges

HAT_MAP = {
    'white': get_white_challenges,
    'red': get_red_challenges,
    'black': get_black_challenges,
    'yellow': get_yellow_challenges,
    'green': get_green_challenges,
    'blue': get_blue_challenges
}

def get_hat_challenges(hat: str, difficulty_range: tuple = None):
    """Get challenges for a specific hat."""
    getter = HAT_MAP.get(hat.lower())
    if getter:
        return getter(difficulty_range)
    return []

def get_all_hats() -> list:
    return list(HAT_MAP.keys())
