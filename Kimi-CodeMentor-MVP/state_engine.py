
# Core state engine - persistent progression system
state_engine_py = '''"""
Kimi-Code: Persistent State Engine
Tracks user progression, skill levels, challenge history, and adaptive difficulty.
"""
import json
import os
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

class StateEngine:
    """Manages persistent user state with progressive difficulty scaling."""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', 'data')
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        self.state_file = os.path.join(self.data_dir, 'user_state.json')
        self.history_file = os.path.join(self.data_dir, 'challenge_history.jsonl')
        self.state = self._load_state()
    
    def _load_state(self) -> Dict[str, Any]:
        """Load or initialize user state."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return self._init_state()
    
    def _init_state(self) -> Dict[str, Any]:
        """Initialize fresh user state."""
        return {
            "user_id": self._generate_user_id(),
            "created_at": datetime.now().isoformat(),
            "last_session": datetime.now().isoformat(),
            "global_level": 1,
            "global_xp": 0,
            "total_challenges_completed": 0,
            "total_time_spent_minutes": 0,
            "streak_days": 0,
            "last_active_date": datetime.now().strftime('%Y-%m-%d'),
            "languages": {},
            "skill_tree": {
                "problem_solving": 1,
                "code_reading": 1,
                "debugging": 1,
                "refactoring": 1,
                "security_awareness": 1,
                "system_design": 1,
                "algorithmic_thinking": 1,
                "testing": 1
            },
            "hats_mastery": {
                "white": {"level": 1, "xp": 0, "challenges": 0},
                "red": {"level": 1, "xp": 0, "challenges": 0},
                "black": {"level": 1, "xp": 0, "challenges": 0},
                "yellow": {"level": 1, "xp": 0, "challenges": 0},
                "green": {"level": 1, "xp": 0, "challenges": 0},
                "blue": {"level": 1, "xp": 0, "challenges": 0}
            },
            "achievements": [],
            "preferences": {
                "primary_language": "python",
                "difficulty_curve": "adaptive",  # adaptive, linear, aggressive
                "session_length": 30,  # minutes
                "hints_enabled": True,
                "six_hats_mode": False
            },
            "adaptive_weights": {
                "success_rate": 0.3,
                "time_factor": 0.2,
                "complexity_tolerance": 0.25,
                "hat_balance": 0.25
            }
        }
    
    def _generate_user_id(self) -> str:
        """Generate unique user identifier."""
        seed = f"{datetime.now().timestamp()}{os.urandom(16).hex()}"
        return hashlib.sha256(seed.encode()).hexdigest()[:16]
    
    def save(self):
        """Persist current state to disk."""
        self.state["last_session"] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_language_state(self, language: str) -> Dict[str, Any]:
        """Get or initialize language-specific state."""
        if language not in self.state["languages"]:
            self.state["languages"][language] = {
                "level": 1,
                "xp": 0,
                "challenges_completed": 0,
                "tracks_unlocked": ["basics"],
                "current_track": "basics",
                "mastery_score": 0.0
            }
        return self.state["languages"][language]
    
    def update_skill(self, skill: str, delta: float):
        """Update a skill score (0-100 scale)."""
        current = self.state["skill_tree"].get(skill, 1)
        self.state["skill_tree"][skill] = min(100, current + delta)
        self._check_skill_milestones(skill, current, self.state["skill_tree"][skill])
    
    def update_hat_mastery(self, hat: str, success: bool, time_taken: int, complexity: int):
        """Update Six Thinking Hats mastery based on challenge performance."""
        hat_data = self.state["hats_mastery"][hat]
        base_xp = complexity * 10
        
        if success:
            time_bonus = max(0, 1 - (time_taken / 300))  # 5 min baseline
            hat_data["xp"] += int(base_xp * (1 + time_bonus))
            hat_data["challenges"] += 1
            
            # Level up check
            xp_needed = hat_data["level"] * 100
            if hat_data["xp"] >= xp_needed:
                hat_data["level"] += 1
                hat_data["xp"] -= xp_needed
                self._log_event("hat_level_up", {"hat": hat, "new_level": hat_data["level"]})
        else:
            hat_data["xp"] += int(base_xp * 0.1)  # Participation xp
        
        self.save()
    
    def calculate_difficulty_modifier(self) -> float:
        """Calculate adaptive difficulty multiplier based on performance."""
        weights = self.state["adaptive_weights"]
        
        # Success rate factor (last 10 challenges)
        recent = self._get_recent_history(10)
        if not recent:
            return 1.0
        
        successes = sum(1 for r in recent if r.get("success", False))
        success_rate = successes / len(recent)
        
        # Time factor
        avg_time = sum(r.get("time_taken", 300) for r in recent) / len(recent)
        time_factor = 1 - (avg_time / 600)  # 10 min baseline
        
        # Complexity tolerance
        avg_complexity = sum(r.get("complexity", 5) for r in recent) / len(recent)
        complexity_factor = avg_complexity / 10
        
        # Hat balance (encourage weaker hats)
        hat_levels = [h["level"] for h in self.state["hats_mastery"].values()]
        hat_variance = max(hat_levels) - min(hat_levels)
        balance_factor = 1 - (hat_variance / 20)
        
        modifier = (
            weights["success_rate"] * success_rate +
            weights["time_factor"] * time_factor +
            weights["complexity_tolerance"] * complexity_factor +
            weights["hat_balance"] * balance_factor
        )
        
        # Clamp between 0.5 and 2.0
        return max(0.5, min(2.0, modifier))
    
    def _get_recent_history(self, n: int) -> List[Dict]:
        """Get last n challenge records."""
        if not os.path.exists(self.history_file):
            return []
        records = []
        with open(self.history_file, 'r') as f:
            for line in f:
                records.append(json.loads(line))
        return records[-n:]
    
    def log_challenge(self, challenge_data: Dict[str, Any]):
        """Log a completed challenge to history."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.state["user_id"],
            **challenge_data
        }
        with open(self.history_file, 'a') as f:
            f.write(json.dumps(record) + '\n')
        
        # Update aggregates
        self.state["total_challenges_completed"] += 1
        self.state["total_time_spent_minutes"] += challenge_data.get("time_taken", 0)
        
        # Check streak
        today = datetime.now().strftime('%Y-%m-%d')
        if today != self.state["last_active_date"]:
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            if self.state["last_active_date"] == yesterday:
                self.state["streak_days"] += 1
            else:
                self.state["streak_days"] = 1
            self.state["last_active_date"] = today
        
        self.save()
    
    def _check_skill_milestones(self, skill: str, old_val: float, new_val: float):
        """Check and award skill milestones."""
        milestones = [25, 50, 75, 90, 100]
        for m in milestones:
            if old_val < m <= new_val:
                self._log_event("skill_milestone", {"skill": skill, "level": m})
                if m == 100:
                    self.state["achievements"].append(f"{skill.replace('_', ' ').title()} Master")
    
    def _log_event(self, event_type: str, data: Dict):
        """Log system event."""
        event_file = os.path.join(self.data_dir, 'events.jsonl')
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        with open(event_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Generate data for user dashboard."""
        return {
            "global_level": self.state["global_level"],
            "global_xp": self.state["global_xp"],
            "streak": self.state["streak_days"],
            "total_challenges": self.state["total_challenges_completed"],
            "skill_tree": self.state["skill_tree"],
            "hats_mastery": self.state["hats_mastery"],
            "languages": {
                lang: {
                    "level": data["level"],
                    "mastery": data["mastery_score"],
                    "tracks": data["tracks_unlocked"]
                }
                for lang, data in self.state["languages"].items()
            },
            "achievements": self.state["achievements"],
            "difficulty_modifier": self.calculate_difficulty_modifier()
        }
'''

with open(f"{base_dir}/core/state_engine.py", 'w') as f:
    f.write(state_engine_py)

print("✅ state_engine.py written")