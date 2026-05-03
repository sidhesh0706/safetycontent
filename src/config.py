"""Central project paths and app constants."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
CONTENT_DIR = DATA_DIR / "content"
INTERACTIVE_DIR = DATA_DIR / "interactive"
RESEARCH_DIR = DATA_DIR / "research"

IMAGES_DIR = PROJECT_ROOT / "images"
STYLES_DIR = PROJECT_ROOT / "styles"

STYLE_FILE = STYLES_DIR / "style.css"
RESEARCH_FILE = RESEARCH_DIR / "ai_safety_sources.csv"
QUIZ_FILE = INTERACTIVE_DIR / "quiz_data.json"
SHARED_EXPERIENCES_FILE = INTERACTIVE_DIR / "shared_experiences.csv"

QUESTIONS_PER_ROUND = 3
