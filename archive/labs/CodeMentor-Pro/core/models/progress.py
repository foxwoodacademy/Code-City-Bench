"""
Progress Models for CodeMentor Pro
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SkillCategory(str, Enum):
    """Skill categories for the skill tree."""
    FUNDAMENTALS = "fundamentals"
    EXECUTION = "execution"
    DESIGN = "design"
    QUALITY = "quality"
    MASTERY = "mastery"


class SkillTreeNode(BaseModel):
    """A node in the skill tree."""
    id: str
    name: str
    description: str
    category: SkillCategory
    icon: str = "📚"
    
    # Progression
    level: int = 0
    max_level: int = 5
    xp: int = 0
    xp_required: int = 100
    
    # Status
    unlocked: bool = False
    completed: bool = False
    
    # Dependencies
    prerequisites: List[str] = []
    dependencies: List[str] = []
    
    # Metadata
    tags: List[str] = []
    difficulty: int = 1
    estimated_hours: float = 1.0
    
    # Learning resources
    resources: List[Dict[str, Any]] = []
    
    class Config:
        from_attributes = True


class SkillTree(BaseModel):
    """Complete skill tree structure."""
    version: str = "1.0.0"
    nodes: Dict[str, SkillTreeNode] = {}
    categories: Dict[SkillCategory, List[str]] = {}
    
    # Predefined skill tree structure (from Kimi-Code)
    @classmethod
    def get_default_tree(cls) -> "SkillTree":
        """Get the default skill tree."""
        nodes = {}
        
        # Fundamentals
        nodes["code_reading"] = SkillTreeNode(
            id="code_reading",
            name="Code Reading",
            description="Understand and interpret existing code effectively",
            category=SkillCategory.FUNDAMENTALS,
            icon="👓",
            xp_required=150
        )
        nodes["syntax_mastery"] = SkillTreeNode(
            id="syntax_mastery",
            name="Syntax Mastery",
            description="Master language syntax and idioms",
            category=SkillCategory.FUNDAMENTALS,
            icon="📖",
            prerequisites=["code_reading"],
            xp_required=200
        )
        nodes["problem_decomposition"] = SkillTreeNode(
            id="problem_decomposition",
            name="Problem Decomposition",
            description="Break down complex problems into manageable parts",
            category=SkillCategory.FUNDAMENTALS,
            icon="🧩",
            prerequisites=["code_reading", "syntax_mastery"],
            xp_required=250
        )
        
        # Execution
        nodes["debugging"] = SkillTreeNode(
            id="debugging",
            name="Debugging",
            description="Find and fix issues in code effectively",
            category=SkillCategory.EXECUTION,
            icon="🐛",
            prerequisites=["code_reading"],
            xp_required=150
        )
        nodes["testing"] = SkillTreeNode(
            id="testing",
            name="Testing",
            description="Write effective tests and understand testing strategies",
            category=SkillCategory.EXECUTION,
            icon="✅",
            prerequisites=["code_reading", "syntax_mastery"],
            xp_required=200
        )
        nodes["refactoring"] = SkillTreeNode(
            id="refactoring",
            name="Refactoring",
            description="Improve code structure without changing behavior",
            category=SkillCategory.EXECUTION,
            icon="🔄",
            prerequisites=["debugging", "testing"],
            xp_required=250
        )
        
        # Design
        nodes["system_design"] = SkillTreeNode(
            id="system_design",
            name="System Design",
            description="Design scalable and maintainable systems",
            category=SkillCategory.DESIGN,
            icon="🏗️",
            prerequisites=["problem_decomposition", "refactoring"],
            xp_required=300
        )
        nodes["algorithmic_thinking"] = SkillTreeNode(
            id="algorithmic_thinking",
            name="Algorithmic Thinking",
            description="Design efficient algorithms and data structures",
            category=SkillCategory.DESIGN,
            icon="🧮",
            prerequisites=["problem_decomposition"],
            xp_required=300
        )
        
        # Quality
        nodes["security_awareness"] = SkillTreeNode(
            id="security_awareness",
            name="Security Awareness",
            description="Identify and prevent security vulnerabilities",
            category=SkillCategory.QUALITY,
            icon="🔒",
            prerequisites=["code_reading", "debugging"],
            xp_required=200
        )
        nodes["performance_optimization"] = SkillTreeNode(
            id="performance_optimization",
            name="Performance Optimization",
            description="Identify and fix performance bottlenecks",
            category=SkillCategory.QUALITY,
            icon="⚡",
            prerequisites=["algorithmic_thinking", "refactoring"],
            xp_required=250
        )
        
        # Mastery
        nodes["fullstack_mastery"] = SkillTreeNode(
            id="fullstack_mastery",
            name="Fullstack Mastery",
            description="Master both frontend and backend development",
            category=SkillCategory.MASTERY,
            icon="👑",
            prerequisites=["system_design", "algorithmic_thinking", "security_awareness"],
            max_level=10,
            xp_required=500
        )
        nodes["architect"] = SkillTreeNode(
            id="architect",
            name="Architect",
            description="Design and oversee complex software systems",
            category=SkillCategory.MASTERY,
            icon="🏛️",
            prerequisites=["fullstack_mastery"],
            max_level=10,
            xp_required=1000
        )
        
        return cls(
            nodes=nodes,
            categories={
                SkillCategory.FUNDAMENTALS: [
                    "code_reading", "syntax_mastery", "problem_decomposition"
                ],
                SkillCategory.EXECUTION: [
                    "debugging", "testing", "refactoring"
                ],
                SkillCategory.DESIGN: [
                    "system_design", "algorithmic_thinking"
                ],
                SkillCategory.QUALITY: [
                    "security_awareness", "performance_optimization"
                ],
                SkillCategory.MASTERY: [
                    "fullstack_mastery", "architect"
                ]
            }
        )


class Achievement(BaseModel):
    """User achievement model."""
    id: str
    user_id: str
    achievement_type: str
    title: str
    description: str
    icon: str
    xp_reward: int = 0
    is_unlocked: bool = False
    unlocked_at: Optional[datetime] = None
    
    # Metadata
    rarity: str = "common"  # common, rare, epic, legendary
    category: str = "general"
    
    class Config:
        from_attributes = True


class UserProgress(BaseModel):
    """Comprehensive user progress model."""
    user_id: str
    
    # Global progress
    global_level: int = 1
    global_xp: int = 0
    total_time_spent_minutes: int = 0
    
    # Streaks
    streak_days: int = 0
    last_active_date: Optional[str] = None  # YYYY-MM-DD format
    
    # Counters
    total_challenges_completed: int = 0
    total_explanations: int = 0
    total_hat_analyses: int = 0
    total_sessions: int = 0
    
    # Skill tree progress
    skill_tree: Dict[str, int] = {}
    unlocked_skills: List[str] = []
    completed_skills: List[str] = []
    
    # Language progress
    languages: Dict[str, Dict[str, Any]] = {}
    
    # Hat mastery
    hats_mastery: Dict[str, Dict[str, Any]] = {
        "white": {"level": 1, "xp": 0, "challenges": 0},
        "red": {"level": 1, "xp": 0, "challenges": 0},
        "black": {"level": 1, "xp": 0, "challenges": 0},
        "yellow": {"level": 1, "xp": 0, "challenges": 0},
        "green": {"level": 1, "xp": 0, "challenges": 0},
        "blue": {"level": 1, "xp": 0, "challenges": 0},
    }
    
    # Achievements
    achievements: List[str] = []
    
    # Preferences
    preferences: Dict[str, Any] = {
        "primary_language": "python",
        "difficulty_curve": "adaptive",
        "session_length": 30,
        "hints_enabled": True,
        "six_hats_mode": False
    }
    
    # Adaptive weights
    adaptive_weights: Dict[str, float] = {
        "success_rate": 0.3,
        "time_factor": 0.2,
        "complexity_tolerance": 0.25,
        "hat_balance": 0.25
    }
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
    def get_level_threshold(self, level: int) -> int:
        """Get XP threshold for a given level."""
        thresholds = [0, 1000, 3000, 7000, 15000, 30000, 50000, 100000]
        return thresholds[min(level, len(thresholds) - 1)]
    
    def get_level_from_xp(self, xp: int) -> int:
        """Calculate level from XP."""
        thresholds = [0, 1000, 3000, 7000, 15000, 30000, 50000, 100000]
        for i, threshold in enumerate(thresholds):
            if xp < threshold:
                return i
        return len(thresholds)
    
    def calculate_difficulty_modifier(self) -> float:
        """Calculate adaptive difficulty multiplier."""
        weights = self.adaptive_weights
        
        # Success rate (simplified - would need history in real impl)
        success_rate = 0.8  # Placeholder
        
        # Time factor
        avg_time = self.total_time_spent_minutes / max(1, self.total_challenges_completed)
        time_factor = 1 - (avg_time / 600)  # 10 min baseline
        
        # Complexity tolerance
        complexity_factor = min(1.0, self.global_level / 10)
        
        # Hat balance
        hat_levels = [h["level"] for h in self.hats_mastery.values()]
        hat_variance = max(hat_levels) - min(hat_levels) if hat_levels else 0
        balance_factor = 1 - (hat_variance / 20)
        
        modifier = (
            weights["success_rate"] * success_rate +
            weights["time_factor"] * time_factor +
            weights["complexity_tolerance"] * complexity_factor +
            weights["hat_balance"] * balance_factor
        )
        
        return max(0.5, min(2.0, modifier))
