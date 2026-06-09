import sqlite3
from .config import DB_PATH


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS recordings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dialect_name TEXT NOT NULL,
            province TEXT NOT NULL,
            city TEXT DEFAULT '',
            uploader_location TEXT DEFAULT '',
            audio_file_path TEXT NOT NULL,
            preset_text TEXT NOT NULL,
            is_preset INTEGER DEFAULT 0,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS dialects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            province TEXT NOT NULL,
            description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS understanding_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recording_id INTEGER NOT NULL,
            province TEXT NOT NULL,
            understood INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recording_id) REFERENCES recordings(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS vocabulary_annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recording_id INTEGER NOT NULL,
            dialect_word TEXT NOT NULL,
            standard_word TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recording_id) REFERENCES recordings(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS game_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recording_id INTEGER NOT NULL,
            correct_meaning TEXT NOT NULL,
            wrong_options TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recording_id) REFERENCES recordings(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_recordings_dialect ON recordings(dialect_name);
        CREATE INDEX IF NOT EXISTS idx_recordings_province ON recordings(province);
        CREATE INDEX IF NOT EXISTS idx_marks_recording ON understanding_marks(recording_id);
        CREATE INDEX IF NOT EXISTS idx_vocab_recording ON vocabulary_annotations(recording_id);
        CREATE INDEX IF NOT EXISTS idx_game_recording ON game_questions(recording_id);
    """)
    conn.commit()
    conn.close()
