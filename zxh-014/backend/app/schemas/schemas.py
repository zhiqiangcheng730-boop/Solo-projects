from datetime import datetime
from pydantic import BaseModel, Field


# ── Dream ──

class DreamCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    emotion: str | None = Field(None, pattern="^(anxiety|calm|excited)$")
    user_id: str = Field(..., min_length=1)


class KeywordResponse(BaseModel):
    keyword: str
    frequency: int

    model_config = {"from_attributes": True}


class DreamResponse(BaseModel):
    id: int
    user_id: str
    content: str
    emotion: str | None
    created_at: datetime
    keywords: list[KeywordResponse] = []

    model_config = {"from_attributes": True}


# ── Symbol ──

class SymbolResponse(BaseModel):
    id: int
    keyword: str
    description: str | None

    model_config = {"from_attributes": True}


class ExplanationCreate(BaseModel):
    symbol_id: int
    explanation: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    source: str = Field("user")


class ExplanationResponse(BaseModel):
    id: int
    symbol_id: int
    user_id: str
    explanation: str
    source: str
    vote_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class VoteRequest(BaseModel):
    explanation_id: int
    user_id: str


# ── Sharing ──

class ShareCreate(BaseModel):
    dream_id: int


class ShareResponse(BaseModel):
    id: int
    share_token: str
    dream_content: str
    dream_emotion: str | None
    comment_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    user_id: str
    content: str


class CommentResponse(BaseModel):
    id: int
    user_id: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Stats ──

class TopKeyword(BaseModel):
    keyword: str
    count: int
    ratio: float


class EmotionCorrelation(BaseModel):
    emotion: str
    dream_count: int
    top_keywords: list[dict]


class StatsOverview(BaseModel):
    total_dreams: int
    total_symbols: int
    total_explanations: int
    total_shares: int
    top_keywords: list[TopKeyword]
    top_explanations: list[dict]
    emotion_correlations: list[dict]
