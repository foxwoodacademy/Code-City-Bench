"""
CodeMentor Pro - Core Module

This module contains the core domain logic for the CodeMentor Pro platform,
integrating components from Kimi-Code, CodeMentor-MVP, and the VS Code extension.
"""

__version__ = "1.0.0"
__author__ = "CodeMentor Pro Team"
__description__ = "Unified AI Coding Mentor SaaS Platform"

# Submodule exports
from .models import (
    User,
    UserProgress,
    Challenge,
    ChallengeSubmission,
    CodeExplanation,
    SkillTreeNode,
    HatAnalysis,
    Achievement,
    Session,
    Team,
    Subscription,
)

from .engines.learning_engine import LearningEngine
from .engines.challenge_engine import ChallengeEngine
from .engines.progression_engine import ProgressionEngine
from .engines.six_hats_engine import SixHatsEngine
from .engines.analytics_engine import AnalyticsEngine

from .services.code_analyzer import CodeAnalyzer
from .services.explanation_service import ExplanationService
from .services.gamification_service import GamificationService

from .utils.cache import ResponseCache
from .utils.code_utils import CodeUtils

__all__ = [
    # Models
    "User",
    "UserProgress", 
    "Challenge",
    "ChallengeSubmission",
    "CodeExplanation",
    "SkillTreeNode",
    "HatAnalysis",
    "Achievement",
    "Session",
    "Team",
    "Subscription",
    # Engines
    "LearningEngine",
    "ChallengeEngine",
    "ProgressionEngine",
    "SixHatsEngine",
    "AnalyticsEngine",
    # Services
    "CodeAnalyzer",
    "ExplanationService",
    "GamificationService",
    # Utils
    "ResponseCache",
    "CodeUtils",
]
