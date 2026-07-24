"""
CodeMentor Pro - Core Models

Pydantic and SQLAlchemy models for the platform.
"""

from .user import User, UserCreate, UserUpdate, UserRole
from .progress import UserProgress, SkillTreeNode, Achievement
from .challenge import Challenge, ChallengeSubmission, ChallengeEvaluation
from .explanation import CodeExplanation, ExplanationRequest, HatAnalysis
from .session import Session, SessionType
from .team import Team, TeamMember, TeamRole
from .subscription import Subscription, SubscriptionTier, SubscriptionStatus

__all__ = [
    # User models
    "User",
    "UserCreate",
    "UserUpdate",
    "UserRole",
    # Progress models
    "UserProgress",
    "SkillTreeNode", 
    "Achievement",
    # Challenge models
    "Challenge",
    "ChallengeSubmission",
    "ChallengeEvaluation",
    # Explanation models
    "CodeExplanation",
    "ExplanationRequest",
    "HatAnalysis",
    # Session models
    "Session",
    "SessionType",
    # Team models
    "Team",
    "TeamMember",
    "TeamRole",
    # Subscription models
    "Subscription",
    "SubscriptionTier",
    "SubscriptionStatus",
]
