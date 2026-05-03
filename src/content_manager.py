import json
import pandas as pd
import streamlit as st  # <--- CRITICAL IMPORT ADDED

from src.config import CONTENT_DIR, QUIZ_FILE, RESEARCH_FILE


def load_markdown_content(filename: str) -> str:
    """Loads and returns the content of a markdown file."""
    filepath = CONTENT_DIR / filename
    try:
        with filepath.open("r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Use st.error only if running Streamlit, otherwise, print/log
        if 'streamlit' in st.__name__:
            st.error(f"Error: Content file '{filename}' not found at {filepath}.")
        return f"Error: Content file '{filename}' not found."
    except Exception as e:
        if 'streamlit' in st.__name__:
            st.error(f"Error reading content: {e}")
        return f"Error reading content: {e}"


def load_research_sources():
    """Loads a list of research sources (e.g., from a CSV)."""
    try:
        # Load from the actual CSV if available
        df = pd.read_csv(RESEARCH_FILE)
        return df
    except FileNotFoundError:
        # Placeholder data if the CSV doesn't exist yet
        return pd.DataFrame({
            'Source': ['(Placeholder) The AI Act', '(Placeholder) UNESCO AI Ethics Guide', '(Placeholder) Common Sense Media'],
            'Topic': ['Legislation', 'Educational Guidelines', 'Parenting Advice'],
            'Link': ['#', '#', '#']
        })
    except Exception as e:
        if 'streamlit' in st.__name__:
            st.error(f"Error loading research data: {e}")
        return pd.DataFrame({'Source': ['Error Loading Data'], 'Topic': ['Check CSV format'], 'Link': ['#']})


def load_quiz_questions() -> list:
    """Loads quiz questions from the external JSON file."""
    try:
        with QUIZ_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        if 'streamlit' in st.__name__:
            st.error(f"Error: Quiz data file not found at {QUIZ_FILE}. Please create it.")
        return []
    except json.JSONDecodeError:
        if 'streamlit' in st.__name__:
            st.error("Error: Could not decode the quiz JSON file. Check its formatting.")
        return []
    except Exception as e:
        if 'streamlit' in st.__name__:
            st.error(f"An unexpected error occurred while loading quiz data: {e}")
        return []
