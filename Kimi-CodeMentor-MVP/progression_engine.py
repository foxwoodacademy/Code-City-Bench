
# Core progression engine - adaptive difficulty and level progression
progression_engine_py = '''"""
Kimi-Code: Progression Engine
Manages level thresholds, unlocks, and adaptive challenge scaling.
"""
import math
from typing import Dict, List, Tuple, Optional
from .state_engine import StateEngine

class ProgressionEngine:
    """Handles all level-up logic, unlocks, and difficulty curves."""
    
    # XP thresholds for global levels (exponential curve)
    LEVEL_THRESHOLDS = {
        1: 0, 2: 100, 3: 250, 4: 500, 5: 900,
        6: 1500, 7: 2400, 8: 3700, 9: 5500, 10: 8000,
        11: 11500, 12: 16000, 13: 22000, 14: 30000, 15: 40000,
        16: 53000, 17: 70000, 18: 92000, 19: 120000, 20: 155000
    }
    
    # Difficulty tiers with complexity ranges
    DIFFICULTY_TIERS = {
        "novice": {"range": (1, 3), "label": "Novice", "color": "#4ade80"},
        "apprentice": {"range": (3, 5), "label": "Apprentice", "color": "#60a5fa"},
        "journeyman": {"range": (5, 7), "label": "Journeyman", "color": "#fbbf24"},
        "expert": {"range": (7, 9), "label": "Expert", "color": "#f97316"},
        "master": {"range": (9, 11), "label": "Master", "color": "#ef4444"},
        "architect": {"range": (11, 15), "label": "Architect", "color": "#a855f7"}
    }
    
    # Language unlock progression
    LANGUAGE_TRACKS = {
        "python": ["basics", "data_structures", "algorithms", "oop", "async", "metaprogramming", "system_design"],
        "javascript": ["basics", "dom", "async", "node", "frameworks", "performance", "architecture"],
        "rust": ["basics", "ownership", "lifetimes", "traits", "unsafe", "macros", "systems"],
        "go": ["basics", "concurrency", "interfaces", "testing", "performance", "microservices", "distributed"],
        "cpp": ["basics", "memory", "templates", "stl", "multithreading", "optimization", "embedded"]
    }
    
    def __init__(self, state_engine: StateEngine):
        self.state = state_engine
    
    def calculate_xp_reward(self, complexity: int, success: bool, time_taken: int, 
                         hints_used: int, hat_bonus: bool = False) -> int:
        """Calculate XP reward for a challenge."""
        if not success:
            return max(5, complexity * 2)  # Consolation xp
        
        base_xp = complexity * 25
        
        # Time bonus (faster = more xp)
        expected_time = complexity * 45  # seconds per complexity point
        time_ratio = time_taken / expected_time
        if time_ratio <= 0.5:
            time_multiplier = 2.0
        elif time_ratio <= 1.0:
            time_multiplier = 1.5
        elif time_ratio <= 1.5:
            time_multiplier = 1.0
        else:
            time_multiplier = 0.7
        
        # Hint penalty
        hint_penalty = max(0, hints_used * 0.15)
        
        # Hat mastery bonus
        hat_multiplier = 1.3 if hat_bonus else 1.0
        
        # Streak bonus
        streak_bonus = min(self.state.state["streak_days"] * 0.05, 0.5)
        
        final_xp = int(base_xp * time_multiplier * (1 - hint_penalty) * hat_multiplier * (1 + streak_bonus))
        return max(10, final_xp)
    
    def add_xp(self, amount: int, source: str = "challenge"):
        """Add XP and check for level ups."""
        self.state.state["global_xp"] += amount
        
        # Check global level up
        current_level = self.state.state["global_level"]
        new_level = self._calculate_level_from_xp(self.state.state["global_xp"])
        
        if new_level > current_level:
            self.state.state["global_level"] = new_level
            self._handle_level_up(current_level, new_level)
        
        self.state.save()
    
    def _calculate_level_from_xp(self, xp: int) -> int:
        """Determine level from total XP."""
        for level in sorted(self.LEVEL_THRESHOLDS.keys(), reverse=True):
            if xp >= self.LEVEL_THRESHOLDS[level]:
                return level
        return 1
    
    def _handle_level_up(self, old_level: int, new_level: int):
        """Handle level up rewards and unlocks."""
        self.state._log_event("level_up", {"old": old_level, "new": new_level})
        
        # Unlock new difficulty tiers
        if new_level >= 3:
            self.state.state["achievements"].append(f"Reached {self.DIFFICULTY_TIERS['apprentice']['label']}")
        if new_level >= 6:
            self.state.state["achievements"].append(f"Reached {self.DIFFICULTY_TIERS['journeyman']['label']}")
        if new_level >= 10:
            self.state.state["achievements"].append(f"Reached {self.DIFFICULTY_TIERS['expert']['label']}")
        if new_level >= 15:
            self.state.state["achievements"].append(f"Reached {self.DIFFICULTY_TIERS['master']['label']}")
        if new_level >= 20:
            self.state.state["achievements"].append(f"Reached {self.DIFFICULTY_TIERS['architect']['label']}")
        
        # Unlock new languages at certain levels
        language_unlocks = {
            2: "javascript",
            4: "rust",
            6: "go",
            8: "cpp"
        }
        
        for lvl, lang in language_unlocks.items():
            if old_level < lvl <= new_level:
                self.state.get_language_state(lang)  # Initializes
                self.state.state["achievements"].append(f"Unlocked {lang.title()} Track")
    
    def get_recommended_difficulty(self, language: str = None) -> Tuple[str, int]:
        """Get recommended difficulty tier and complexity for next challenge."""
        modifier = self.state.calculate_difficulty_modifier()
        global_level = self.state.state["global_level"]
        
        # Base difficulty from global level
        if global_level <= 2:
            base_tier = "novice"
        elif global_level <= 5:
            base_tier = "apprentice"
        elif global_level <= 8:
            base_tier = "journeyman"
        elif global_level <= 12:
            base_tier = "expert"
        elif global_level <= 16:
            base_tier = "master"
        else:
            base_tier = "architect"
        
        # Adjust by performance modifier
        tier_names = list(self.DIFFICULTY_TIERS.keys())
        current_idx = tier_names.index(base_tier)
        
        if modifier > 1.3 and current_idx < len(tier_names) - 1:
            recommended_tier = tier_names[current_idx + 1]
        elif modifier < 0.7 and current_idx > 0:
            recommended_tier = tier_names[current_idx - 1]
        else:
            recommended_tier = base_tier
        
        tier_data = self.DIFFICULTY_TIERS[recommended_tier]
        complexity_range = tier_data["range"]
        
        # Pick complexity within range, weighted by modifier
        min_c, max_c = complexity_range
        complexity = min_c + int((max_c - min_c) * (modifier - 0.5))
        complexity = max(min_c, min(max_c, complexity))
        
        return recommended_tier, complexity
    
    def get_next_track(self, language: str) -> Optional[str]:
        """Get the next track to unlock for a language."""
        lang_state = self.state.get_language_state(language)
        tracks = self.LANGUAGE_TRACKS.get(language, ["basics"])
        unlocked = lang_state["tracks_unlocked"]
        
        for track in tracks:
            if track not in unlocked:
                return track
        return None
    
    def check_track_unlock(self, language: str, current_track: str) -> bool:
        """Check if user qualifies to unlock next track."""
        lang_state = self.state.get_language_state(language)
        tracks = self.LANGUAGE_TRACKS.get(language, [])
        
        if current_track not in tracks:
            return False
        
        current_idx = tracks.index(current_track)
        if current_idx >= len(tracks) - 1:
            return False  # Already at last track
        
        # Requirements to unlock next track
        required_challenges = 5 + (current_idx * 3)  # 5, 8, 11, 14...
        required_mastery = 0.6 + (current_idx * 0.1)  # 60%, 70%, 80%...
        
        track_challenges = self._count_track_challenges(language, current_track)
        track_mastery = lang_state["mastery_score"]
        
        if track_challenges >= required_challenges and track_mastery >= required_mastery:
            next_track = tracks[current_idx + 1]
            lang_state["tracks_unlocked"].append(next_track)
            self.state.save()
            return True
        
        return False
    
    def _count_track_challenges(self, language: str, track: str) -> int:
        """Count completed challenges for a specific track."""
        history = self.state._get_recent_history(1000)
        return sum(1 for h in history 
                  if h.get("language") == language and h.get("track") == track)
    
    def get_progress_summary(self) -> Dict:
        """Get comprehensive progress summary."""
        return {
            "global": {
                "level": self.state.state["global_level"],
                "xp": self.state.state["global_xp"],
                "next_level_xp": self.LEVEL_THRESHOLDS.get(
                    self.state.state["global_level"] + 1, 
                    self.state.state["global_xp"] + 100000
                ),
                "streak": self.state.state["streak_days"]
            },
            "difficulty_recommendation": self.get_recommended_difficulty(),
            "skills": self.state.state["skill_tree"],
            "hats": self.state.state["hats_mastery"],
            "languages": {
                lang: {
                    "level": data["level"],
                    "current_track": data["current_track"],
                    "tracks": data["tracks_unlocked"],
                    "next_unlock": self.get_next_track(lang)
                }
                for lang, data in self.state.state["languages"].items()
            }
        }
'''

with open(f"{base_dir}/core/progression_engine.py", 'w') as f:
    f.write(progression_engine_py)

print("✅ progression_engine.py written")