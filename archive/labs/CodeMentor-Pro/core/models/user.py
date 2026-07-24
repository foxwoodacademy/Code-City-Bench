"""
User Models for CodeMentor Pro
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from pydantic.json_schema import JsonSchemaValue


class UserRole(str, Enum):
    """User roles in the system."""
    USER = "user"
    PRO = "pro"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    TEAM_LEAD = "team_lead"


class UserBase(BaseModel):
    """Base user model."""
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User registration model."""
    password: str = Field(..., min_length=8, max_length=128)
    referrer_code: Optional[str] = None
    subscription_tier: Optional[str] = "free"


class UserUpdate(BaseModel):
    """User update model."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    preferences: Optional[dict] = None


class UserPreferences(BaseModel):
    """User preferences model."""
    primary_language: str = "python"
    theme: str = "dark"
    editor_font_size: int = 14
    difficulty_curve: str = "adaptive"  # adaptive, linear, aggressive
    hints_enabled: bool = True
    six_hats_mode: bool = False
    notifications_enabled: bool = True
    email_notifications: bool = False


class UserStatistics(BaseModel):
    """User statistics model."""
    total_xp: int = 0
    global_level: int = 1
    streak_days: int = 0
    total_sessions: int = 0
    total_time_spent_minutes: int = 0
    challenges_completed: int = 0
    explanations_requested: int = 0
    perfect_solutions: int = 0
    hat_analyses: int = 0


class User(UserBase):
    """Full user model with all fields."""
    id: str
    hashed_password: str
    roles: List[UserRole] = [UserRole.USER]
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    statistics: UserStatistics = Field(default_factory=UserStatistics)
    
    # Account status
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    last_active: Optional[datetime] = None
    
    # Profile
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    github_username: Optional[str] = None
    twitter_username: Optional[str] = None
    
    # Referral
    referrer_id: Optional[str] = None
    referral_code: str
    referred_users: List[str] = []
    
    # Subscription
    subscription_tier: str = "free"
    subscription_status: str = "active"
    subscription_expires: Optional[datetime] = None
    
    # Team
    team_id: Optional[str] = None
    team_role: Optional[str] = None
    
    # API Keys
    api_keys: List[str] = []
    
    # Security
    mfa_secret: Optional[str] = None
    mfa_enabled: bool = False
    backup_codes: List[str] = []
    
    # Social logins
    github_id: Optional[str] = None
    google_id: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [{
                "id": "user_123",
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "roles": ["user"],
                "is_active": True,
                "is_verified": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
            }]
        }


class UserPublic(BaseModel):
    """Public user model (excludes sensitive data)."""
    id: str
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    roles: List[UserRole]
    statistics: UserStatistics
    created_at: datetime
    
    class Config:
        from_attributes = True
