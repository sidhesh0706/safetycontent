import streamlit as st
import random
from src.content_manager import load_quiz_questions

# Number of questions to show per attempt
QUESTIONS_PER_ROUND = 3


def initialize_quiz_state():
    """Initializes and resets the quiz state, selecting a new batch of 3 questions."""

    # 1. Initialize persistent global variables
    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0
    if 'quiz_round' not in st.session_state:
        st.session_state.quiz_round = 1

    # 2. Initialize ephemeral (round-specific) variables
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []

    if 'round_answers' not in st.session_state:
        st.session_state.round_answers = {}
    if 'round_score' not in st.session_state:
        st.session_state.round_score = 0
    if 'round_score_added' not in st.session_state:
        st.session_state.round_score_added = 0  # Track which round's score was last added

    # 3. Logic to load new questions if needed (Check state AFTER initialization)
    # The condition is: Load new questions ONLY if there are no current questions OR if the last round was submitted AND the next round button was clicked.

    # Check if the session is currently marked for a new round transition
    if 'start_new_round' in st.session_state and st.session_state.start_new_round:
        del st.session_state.start_new_round
        load_new_questions = True
    else:
        load_new_questions = not st.session_state.current_questions

    if load_new_questions:

        full_pool = load_quiz_questions()

        if len(full_pool) < QUESTIONS_PER_ROUND:
            st.warning(f"Quiz error: Found only {len(full_pool)} questions. Need at least {QUESTIONS_PER_ROUND}.")
            st.session_state.current_questions = full_pool
        else:
            # Select 3 unique questions randomly
            st.session_state.current_questions = random.sample(full_pool, QUESTIONS_PER_ROUND)

        # Reset submission-specific state
        st.session_state.quiz_submitted = False
        st.session_state.round_answers = {}
        st.session_state.round_score = 0


def display_results(questions):
    """Calculates and displays the final score and explanations for the current round."""
    correct_count = 0

    st.markdown("## 🎉 Round Results Summary")

    for q_data in questions:
        user_answer = st.session_state.round_answers.get(q_data['id'])
        is_correct = user_answer == q_data['answer']

        with st.expander(
                f"Q{q_data['id']} - {'✅ CORRECT' if is_correct else '❌ INCORRECT'} ({q_data.get('topic', 'General')})",
                expanded=True):
            st.write(f"**Your Answer:** `{user_answer}`")
            st.write(f"**Correct Answer:** `{q_data['answer']}`")
            st.markdown(f"**Explanation:** *{q_data['explanation']}*")

        if is_correct:
            correct_count += 1

    st.session_state.round_score = correct_count

    st.metric(label="Round Score", value=f"{correct_count} / {len(questions)}")


def run_quiz():
    """Renders the quiz interface, handles submissions, and resets rounds."""

    initialize_quiz_state()

    questions = st.session_state.current_questions

    if not questions:
        st.error("Cannot run quiz: Question pool is empty. Please check quiz_data.json syntax.")
        return

    # --- RENDER QUIZ TITLE AND SCORE ---
    st.markdown(f"### Interactive Quiz: Round {st.session_state.quiz_round} 🧠")
    st.info(f"Answer the {QUESTIONS_PER_ROUND} questions below. Total Score Achieved: {st.session_state.total_score}")

    # --- Render Questions in Tabs ---
    tab_titles = [f"Q{i + 1}" for i in range(QUESTIONS_PER_ROUND)]
    tabs = st.tabs(tab_titles)

    is_submitted = st.session_state.quiz_submitted

    # Render all questions inside their respective tabs
    for i, q_data in enumerate(questions):
        with tabs[i]:
            st.markdown(f"#### {q_data['question']}")

            selected_option = st.session_state.round_answers.get(q_data['id'])

            try:
                default_index = q_data['options'].index(selected_option) if selected_option else 0
            except ValueError:
                default_index = 0

            user_choice = st.radio(
                "Your Choice:",
                options=q_data['options'],
                key=f"q_{q_data['id']}_{st.session_state.quiz_round}",
                index=default_index,
                disabled=is_submitted
            )

            st.session_state.round_answers[q_data['id']] = user_choice

            # --- Display brief feedback inside the tab if submitted ---
            if is_submitted:
                if user_choice == q_data['answer']:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. The correct answer was: {q_data['answer']}")

            st.markdown("---")

    # --- Submission and Scoring ---

    if st.session_state.quiz_submitted:
        # Display detailed results for the round
        display_results(questions)

        # Add score to total score only if this round's score has NOT been added yet
        if st.session_state.round_score_added != st.session_state.quiz_round:
            st.session_state.total_score += st.session_state.round_score
            st.session_state.round_score_added = st.session_state.quiz_round

    # Create two columns for the submission buttons
    col1, col2 = st.columns(2)

    with col1:
        if not st.session_state.quiz_submitted:
            # Check if ALL questions have answers before allowing submission
            # A set comparison is safer than checking for None, ensuring all IDs are present.
            if len(st.session_state.round_answers) < QUESTIONS_PER_ROUND or any(
                    v is None for v in st.session_state.round_answers.values()):
                st.warning("Please attempt all questions before submitting.")
                st.button(f"Submit Round {st.session_state.quiz_round}", disabled=True)
            else:
                # This button CLICK flips the state and causes a rerun for RESULTS
                if st.button(f"Submit Round {st.session_state.quiz_round}", key="submit_round_btn"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
        else:
            # This button CLICK increments the round number and causes a rerun for NEW QUESTIONS
            if st.button("Start Next Round (New Questions)", key="next_round_btn"):
                st.session_state.quiz_round += 1
                st.session_state.start_new_round = True  # Flag to trigger question reloading
                st.rerun()

    with col2:
        if st.button("Reset All Scores & Start Fresh", key="reset_all_btn"):
            # Delete all quiz-related state variables
            for key in list(st.session_state.keys()):
                if key.startswith('quiz_') or key == 'total_score' or key == 'round_score_added':
                    del st.session_state[key]
            st.rerun()