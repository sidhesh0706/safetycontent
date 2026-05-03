# AI Safety Content Guide

![AI Safety Content Guide banner](images/readme_banner.svg)

**An interactive AI safety education platform for students, parents, and educators.**

AI Safety Content Guide turns synthetic-media risk into hands-on learning: users practice spotting deepfake artifacts, responding to AI-enabled scams, understanding prompt injection, moderating suspicious content, and building healthier digital literacy habits.

## Problem

Generative AI has lowered the barrier for creating convincing text, images, audio, and video. For families and classrooms, the challenge is not only technical detection. The larger problem is helping people slow down, verify information, recognize manipulation patterns, and know what to do when something feels suspicious.

## Solution

This project packages AI safety concepts into an interactive Streamlit experience. Instead of only presenting static advice, it gives learners practical modules for investigation, reflection, and response.

## Features

| Area | What It Does | Why It Matters |
| --- | --- | --- |
| AI misinformation lessons | Explains synthetic media, bias, hallucinations, and unsafe AI use cases | Builds a baseline mental model for non-technical users |
| Deepfake forensics | Uses local visual cases to teach artifact spotting | Turns detection into a concrete observation skill |
| Prompt-injection simulator | Demonstrates how roleplay and instruction attacks can bypass naive guardrails | Introduces AI security concepts in a safe environment |
| Scam response training | Walks through voice-clone, phishing, and deepfake endorsement scenarios | Teaches verification before action |
| Content moderation sandbox | Asks users to classify realistic social posts as safe, fake, or suspicious | Encourages context-aware media judgment |
| Quiz engine | Randomized rounds with scoring and explanations | Reinforces retention through practice |
| Digital literacy resources | Curated guidance for families and educators | Connects technical risks to everyday rules and habits |
| Community sharing | Local CSV-backed experience sharing | Allows lightweight discussion without external services |

## Tech Stack

| Layer | Tools |
| --- | --- |
| Application | Streamlit |
| Language | Python |
| Data | JSON, CSV, Markdown |
| Data handling | Pandas |
| Styling | Custom CSS and Streamlit theme config |
| Testing | Pytest |

## Architecture Overview

```text
Streamlit UI
   |
   |-- ai_safety_app.py         # Page layout, navigation, and interactive modules
   |-- src/config.py            # Centralized project paths and app constants
   |-- src/content_manager.py   # Markdown, quiz, and research source loading
   `-- src/quiz_engine.py       # Quiz state, scoring, and explanations

Data layer
   |
   |-- data/content/            # Educational markdown
   |-- data/interactive/        # Quiz data and local sharing example
   `-- data/research/           # Curated source list

Presentation
   |
   |-- styles/style.css         # Custom visual system
   `-- images/                  # Forensic examples and README assets
```

## Folder Structure

```text
.
|-- ai_safety_app.py
|-- src/
|   |-- config.py
|   |-- content_manager.py
|   `-- quiz_engine.py
|-- data/
|   |-- content/
|   |-- interactive/
|   `-- research/
|-- images/
|-- styles/
|-- tests/
|-- requirements.txt
|-- requirements-dev.txt
`-- README.md
```

## Local Setup

```bash
git clone https://github.com/sidhesh0706/safetycontent.git
cd safetycontent

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
streamlit run ai_safety_app.py
```

The app will open at the local URL printed by Streamlit, usually `http://localhost:8501`.

## Testing

Install development dependencies and run the lightweight test suite:

```bash
pip install -r requirements-dev.txt
pytest
```

Current tests cover:

- required content, image, style, quiz, and research files
- markdown content loading
- quiz question schema and answer validity
- research source table columns

## Deployment

This project is ready for Streamlit Community Cloud.

1. Push the repository to GitHub.
2. Create a new Streamlit app.
3. Select this repository.
4. Set the entry point to `ai_safety_app.py`.
5. Deploy with `requirements.txt`.

No API keys are required for the current version.

## Product Decisions

- **Streamlit-first UX:** prioritizes fast iteration and interactive education over heavy frontend infrastructure.
- **Local data files:** keeps the project easy to inspect, clone, and run without a database.
- **Rule-based simulations:** makes AI safety concepts understandable without pretending to be a production detector.
- **Centralized paths:** avoids fragile working-directory assumptions and makes tests easier to run.
- **Non-alarmist copy:** frames AI safety as practical literacy instead of fear-based messaging.

## What This Demonstrates

- Ability to turn a social/technical AI risk area into a usable educational product.
- Strong product framing for parents, educators, and students.
- Practical Streamlit app development with custom styling and multiple interactive workflows.
- Data-driven quiz/content loading using JSON, CSV, and Markdown.
- Basic maintainability through centralized config, repo hygiene, and tests.
- Recruiter-friendly documentation that explains product value, architecture, setup, and limitations.

## Known Limitations

- Community sharing uses a local CSV file and is not designed for multi-user production deployment.
- The text analyzer is educational and rule-based; it should not be treated as a reliable AI detector.
- The forensic cases are static training examples, not a full media authentication system.
- There is no authentication, moderation workflow, or persistent database yet.

## Roadmap

- Add deployed app screenshots and a hosted demo link.
- Move community submissions to a database or managed backend.
- Add role-specific learning paths for students, parents, and educators.
- Add facilitator notes or printable classroom activities.
- Expand tests around quiz scoring and data validation.
- Add accessibility QA for color contrast, keyboard navigation, and mobile layouts.

## Recommended GitHub Metadata

**Description:** Streamlit AI safety education platform with deepfake forensics, prompt-injection labs, scam simulations, quizzes, and digital literacy resources.

**Topics:** `ai-safety`, `streamlit`, `digital-literacy`, `deepfakes`, `misinformation`, `prompt-injection`, `cybersecurity-awareness`, `education`, `python`, `media-literacy`

## Author

Built by [Sidhesh](https://github.com/sidhesh0706) as an AI safety education and digital literacy project.
