from pathlib import Path

from src.config import CONTENT_DIR, IMAGES_DIR, QUIZ_FILE, RESEARCH_FILE, STYLE_FILE
from src.content_manager import load_markdown_content, load_quiz_questions, load_research_sources


def test_required_project_assets_exist():
    required_paths = [
        CONTENT_DIR / "intro.md",
        CONTENT_DIR / "literacy_tips.md",
        CONTENT_DIR / "risks_misinfo.md",
        QUIZ_FILE,
        RESEARCH_FILE,
        STYLE_FILE,
        IMAGES_DIR / "readme_banner.svg",
    ]

    missing = [path for path in required_paths if not Path(path).exists()]
    assert not missing


def test_markdown_content_loader_returns_real_content():
    content = load_markdown_content("literacy_tips.md")

    assert isinstance(content, str)
    assert len(content) > 100
    assert "Digital Literacy" in content


def test_quiz_questions_have_required_fields():
    questions = load_quiz_questions()

    assert len(questions) >= 3
    for question in questions:
        assert {"id", "question", "options", "answer", "explanation", "topic"} <= set(question)
        assert question["answer"] in question["options"]


def test_research_sources_have_display_columns():
    sources = load_research_sources()

    assert not sources.empty
    assert {"Source", "Topic", "Link"} <= set(sources.columns)
