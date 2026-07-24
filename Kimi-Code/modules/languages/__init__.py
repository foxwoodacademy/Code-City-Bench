"""
Kimi-Code Language Tracks
"""
from .python_track import get_challenges as get_python_challenges
from .javascript_track import get_challenges as get_js_challenges
from .rust_track import get_challenges as get_rust_challenges
from .go_track import get_challenges as get_go_challenges
from .cpp_track import get_challenges as get_cpp_challenges

LANGUAGE_MAP = {
    'python': get_python_challenges,
    'javascript': get_js_challenges,
    'js': get_js_challenges,
    'rust': get_rust_challenges,
    'go': get_go_challenges,
    'golang': get_go_challenges,
    'cpp': get_cpp_challenges,
    'c++': get_cpp_challenges
}

def get_language_challenges(language: str, track: str, difficulty_range: tuple = None):
    """Get challenges for any supported language."""
    getter = LANGUAGE_MAP.get(language.lower())
    if getter:
        return getter(track, difficulty_range)
    return []

def get_all_languages() -> list:
    return list(set(LANGUAGE_MAP.keys()))
