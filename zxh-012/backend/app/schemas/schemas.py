from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


class RecordingCreate(BaseModel):
    dialect_name: str
    province: str
    city: str = ""
    uploader_location: str = ""
    preset_text: str
    is_preset: bool = False
    recorded_at: Optional[str] = None


class RecordingOut(BaseModel):
    id: int
    dialect_name: str
    province: str
    city: str
    uploader_location: str
    audio_file_path: str
    preset_text: str
    is_preset: bool
    recorded_at: Optional[str]
    created_at: Optional[str]


class DialectCreate(BaseModel):
    name: str
    province: str
    description: str = ""


class DialectOut(BaseModel):
    id: int
    name: str
    province: str
    description: str


class UnderstandingMarkCreate(BaseModel):
    recording_id: int
    province: str
    understood: bool = False


class UnderstandingStats(BaseModel):
    total: int
    understood: int


class HeatmapItem(BaseModel):
    province: str
    total: int
    understood: int
    ratio: float


class VocabularyCreate(BaseModel):
    recording_id: int
    dialect_word: str
    standard_word: str


class VocabularyOut(BaseModel):
    id: int
    recording_id: int
    dialect_word: str
    standard_word: str
    created_at: Optional[str]


class GameQuestionCreate(BaseModel):
    recording_id: int
    correct_meaning: str
    wrong_options: str


class GameQuestionOut(BaseModel):
    id: int
    recording_id: int
    correct_meaning: str
    wrong_options: str
    dialect_name: str
    province: str
    preset_text: str
    audio_file_path: str = ""


class DashboardStats(BaseModel):
    total_recordings: int
    total_dialects: int
    total_marks: int
    total_questions: int
    province_stats: list
