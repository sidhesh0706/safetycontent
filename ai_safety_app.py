import streamlit as st
from src.quiz_engine import run_quiz
from src.content_manager import load_markdown_content, load_research_sources
import pandas as pd
import os
import json

# --- Define the shared experiences file path ---
FEEDBACK_FILE = "data/interactive/shared_experiences.csv"


# -----------------------------------------------

# --- Inject Custom CSS Function ---
def inject_custom_css():
    """Reads and injects the custom CSS for a better look."""
    try:
        with open("styles/style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Could not find styles/style.css. Please check the 'styles' directory.")


# -----------------------------------


# --- Community Sharing Helpers ---

def delete_experience(row_index):
    """Loads data, deletes the specified row index, and overwrites the CSV."""
    try:
        df = pd.read_csv(FEEDBACK_FILE)
        df = df.sort_values(by='Timestamp', ascending=False).reset_index(drop=True)

        if 0 <= row_index < len(df):
            df = df.drop(row_index).reset_index(drop=True)
            df.to_csv(FEEDBACK_FILE, mode='w', index=False, header=True)
            st.success("Post deleted successfully!")
            st.rerun()
        else:
            st.error("Invalid post index for deletion.")

    except FileNotFoundError:
        st.error("No shared experiences file found to delete from.")
    except Exception as e:
        st.error(f"Error during deletion: {e}")


def save_experience(name, role, experience):
    """Saves the user experience to a CSV file."""

    new_data = pd.DataFrame({
        'Timestamp': [pd.Timestamp.now()],
        'Name': [name],
        'Role': [role],
        'Experience': [experience]
    })

    if not os.path.exists(FEEDBACK_FILE):
        new_data.to_csv(FEEDBACK_FILE, mode='w', index=False, header=True)
    else:
        new_data.to_csv(FEEDBACK_FILE, mode='a', index=False, header=False)

    st.success("🎉 Thank you! Your experience has been shared with the community.")


def load_shared_experiences():
    """Loads and displays existing shared experiences with a Delete button."""
    try:
        df = pd.read_csv(FEEDBACK_FILE)
        df = df.sort_values(by='Timestamp', ascending=False).reset_index(drop=True)

        st.markdown("### Recent Experiences from Parents and Educators")

        for index, row in df.iterrows():
            col_content, col_delete = st.columns([6, 1])

            with col_content:
                with st.container(border=True):
                    st.markdown(f"**{row['Name']}** ({row['Role']}) shared on {str(row['Timestamp'])[:10]}:")
                    st.write(f"*{row['Experience']}*")

            with col_delete:
                if st.button("❌ Delete", key=f"delete_{index}"):
                    delete_experience(index)

        if len(df) == 0:
            st.info("Be the first to share your experience!")

    except FileNotFoundError:
        st.info("Be the first to share your experience!")
    except Exception as e:
        st.error(f"Could not load shared experiences: {e}")


def display_sharing_section():
    """Renders the Community Sharing Form and displays recent posts."""

    st.header("Community Voices: Share Your Experience 🗣️")
    st.divider()

    st.markdown("""
    This space is for parents and educators to share challenges, successful monitoring techniques, or useful resources they've found regarding AI-generated content.
    """)

    with st.form("experience_form", clear_on_submit=True):
        st.markdown("#### Tell us what you've learned or encountered")

        col_name, col_role = st.columns(2)

        with col_name:
            user_name = st.text_input("Your Name/Alias", max_chars=50)

        with col_role:
            user_role = st.selectbox("I am a:", ["Parent", "Educator", "Other"], index=0)

        experience = st.text_area("Your Experience or Tip (Max 500 characters)", max_chars=500, height=150)

        submitted = st.form_submit_button("Share Experience")

        if submitted:
            if user_name and experience:
                save_experience(user_name, user_role, experience)
            else:
                st.error("Please provide your name and experience before sharing.")

    st.divider()

    load_shared_experiences()


# ----------------------------------

def display_intro_section():
    """Renders a high-density Project Introduction, Mission, and Overview with Diagrams."""

    # 1. Strategic Mission - Glossy Card
    st.markdown("### 🎯 Strategic Mission")
    st.info("""
        **Our Core Mission:** To foster systemic digital resilience by promoting advanced critical thinking 
        and foundational digital literacy in the age of generative AI. We empower families and 
        educators with a logic-based framework to identify, scrutinize, and neutralize synthetic 
        misinformation. Our goal is to ensure that the next generation can distinguish between human 
        intent and algorithmic output, protecting the integrity of our shared information landscape 
        through verified knowledge and ethical interaction.
    """)

    st.title("PROJECT OVERVIEW & SAFETY MISSION")
    st.divider()

    # 2. Detailed Project Overview & The Need for AI Safety
    st.header("The Critical Need for AI Safety")
    col_text, col_viz = st.columns([2, 1])

    with col_text:
        st.write("""
            The rapid proliferation of AI-generated text, images, and videos has fundamentally altered our 
            relationship with digital reality. We are currently navigating a 'post-truth' era where 
            synthetic media is virtually indistinguishable from genuine human creation. This technological 
            leap necessitates a multi-layered defense guide. 
            \n**The Psychological Impact:** Children are particularly vulnerable to 'algorithmic persuasion,' 
            where AI models can subtly manipulate opinions or create obsessive usage patterns. 
            \n**The Information Crisis:** When fakes become perfect, the 'Liar’s Dividend' takes effect—people 
            begin to doubt real evidence, leading to a total collapse of shared truth. This project serves 
            as a centralized strategic resource, moving beyond basic awareness into technical deconstruction 
            to restore that lost trust.
        """)

    with col_viz:
        # Informative diagram showing the loop of AI content creation vs. human verification
        st.markdown("")
        st.caption("The AI Safety Feedback Loop")

    st.divider()

    # 3. Strategic Priorities (Expanded Content & Large Fonts)
    st.header("Core Strategic Priorities")
    cp1, cp2 = st.columns(2)

    with cp1:
        st.metric(label="RISK AWARENESS", value="Priority 01")
        st.markdown("""
            **Technical Forensics:** We prioritize the granular detection of synthetic artifacts. This includes 
            educating users on 'Deepfake signatures'—biometric glitches, inconsistent light-source mapping, 
            and audio spectral irregularities. 
            \n**Threat Landscape Mapping:** Beyond pixels, we examine the 'Why.' We analyze how deepfakes are 
            weaponized for financial fraud (voice phishing) and political destabilization, ensuring users 
            understand the social engineering tactics used in modern misinformation.
        """)

    with cp2:
        st.metric(label="DIGITAL LITERACY", value="Priority 02")
        st.markdown("""
            **The 'Verify-First' Architecture:** Our secondary priority is the cultivation of cognitive resilience. 
            We implement 'Lateral Reading' techniques, where users are trained to cross-reference AI-generated 
            claims against a hierarchy of human-verified, peer-reviewed, and authoritative databases.
            \n**Algorithmic Transparency:** We demystify the 'Black Box.' By teaching users that AI models 
            predict probability rather than possessing objective 'truth,' we strip away the illusion of 
            infallibility that often leads to over-reliance on automated tools.
        """)

    st.divider()

    # 4. Operational Approach (Triple-Expanded)
    st.header("Our Core Approach")
    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("#### 🚫 Threat Identification")
        st.write("""
            We systematically deconstruct the risk spectrum, ranging from automated phishing bots to the 
            subtle amplification of systemic bias within training data. We explore 'Data Poisoning' 
            and its impact on the safety of child-facing content.
        """)

    with p2:
        st.markdown("#### 🧠 Cognitive Defense")
        st.write("""
            We deploy logic-based educational modules that focus on the psychology of belief. By 
            studying common logical fallacies—such as the 'appeal to authority'—and seeing how 
            AI mimics these, users develop a robust mental shield.
        """)

    with p3:
        st.markdown("#### 🔒 Technical Guardrails")
        st.write("""
            Our approach provides actionable blueprints for deploying 'Secure Digital Sandboxes.' 
            This includes the implementation of robust monitoring software, granular gating 
            protocols, and cryptographic verification of content.
        """)


def display_risks_section():
    """Enhanced Risks section with tripled General content and conditional age-gating."""
    is_gated = st.session_state.get('age_profile') == "Pre-Teen (Gated Content)"

    # --- Section Header ---
    st.header("Understanding the Dangers 🚨")
    st.divider()

    # --- 1. THE EVOLUTION OF SYNTHETIC MEDIA ---
    st.subheader("1. The Evolution of Synthetic Media")
    col_img, col_text = st.columns([1, 2])

    with col_img:
        st.image("https://diplo-media.s3.eu-central-1.amazonaws.com/2024/09/Zelensky-deepfake-1024x585.png",
                 caption="AI Facial Reconstruction Mapping")

    with col_text:
        if is_gated:
            st.markdown("""
                **How it works:** Some AI tools are like very smart "copy-cats." They can look at a photo or listen to a voice and make a new version that looks or sounds almost real. 
                \n**The Risk:** Someone might use these tools to pretend to be someone else. 
                \n**What to do:** If you see a video of a friend or family member doing or saying something very strange or asking for money, don't believe it right away. Talk to a trusted adult first!
            """)
        else:
            st.markdown("""
                **The Technical Core: Generative Adversarial Networks (GANs).** Deepfakes are powered by an adversarial deep learning architecture where two neural networks—the *Generator* and the *Discriminator*—compete in a zero-sum game. The Generator creates synthetic data while the Discriminator evaluates its authenticity against real training sets. This continuous backpropagation loop forces the Generator to produce artifacts that are mathematically indistinguishable from reality.

                **The Critical Threat: AI Voice Phishing (Vishing).** Scammers utilize "Vocal biomarkers"—pitch, tone, and breathing patterns—cloned from as little as 3 seconds of audio. This is integrated into "Urgent Crisis" social engineering pretexts. Because AI voices can now replicate human emotional nuances, they bypass the brain's natural "uncanny valley" response, making specious requests for funds or data highly convincing.

                **The Societal Impact: The Liar’s Dividend.** As synthetic media proliferates, we face a "Continuous Reality Doubt." The 'Liar’s Dividend' occurs when the mere *possibility* of deepfakes allows malicious actors to dismiss genuine, incriminating evidence (like leaked recordings) as fake. This erodes the shared informational environment, undermining legal accountability and public trust in verified journalism.

                **Future Trajectory: Real-Time Interactive Deepfakes.** We are moving from static image generation to live, generative video-stream injection. This allows attackers to assumes a target's identity during live video calls, potentially bypassing biometric "liveness" tests and multi-factor authentication (MFA) systems.
            """)

    st.divider()

    # --- 2. DETAILED FOCUS AREAS ---
    st.header("Major Focus Areas & Technical Risks")
    col_misinfo, col_bias, col_inapp = st.columns(3)

    # --- Pillar 01: Weaponized Media ---
    with col_misinfo:
        st.markdown("#### 🚫 Weaponized Media")
        if is_gated:
            st.warning("Simplified Content")
            st.write("""
                **What it means:** AI can create fake images and videos that look very real. 
                Always ask yourself: "Did I see this happen in person, or just on a screen?"
            """)
        else:
            st.info("Technical Details: Identity & Fraud")
            st.write("""
                **Fraudulent Infrastructure:** Adversarial actors now use specialized tools like **FraudGPT** to generate hyper-realistic phishing templates and replicate high-fidelity banking interfaces in milliseconds. 
                \n**NCID Vulnerabilities:** Non-Consensual Intimate Deepfakes (NCID) represent a profound violation of autonomy, often used in "Sextortion" schemes targeting minors and public figures. These synthetic images lurk online indefinitely, causing permanent reputational and psychological trauma.
                \n**Political Destabilization:** Hyper-targeted misinformation campaigns can fabricate diplomatic crises or "hot mic" scandals hours before elections, exploiting social fractures before human fact-checkers can respond.
                \n**Defense:** Implement cryptographic watermarking and utilize metadata analysis tools to verify the "Chain of Custody" of digital assets.
            """)

    # --- Pillar 02: Algorithmic Bias ---
    with col_bias:
        st.markdown("#### ⚖️ Systemic Inequality")
        if is_gated:
            st.warning("Simplified Content")
            st.write("""
                **What it means:** AI isn't always fair. Because it learns from the internet, it can pick up old, mean, or wrong ideas.
                \n**What to do:** Remember that AI doesn't "know" everything. It’s always good to look at books or talk to teachers to get the full story.
            """)
        else:
            st.info("Technical Details: The Bias Loop")
            st.write("""
                **Historical & Sample Bias:** AI models suffer from **Historical Bias**, mirroring past societal prejudices (e.g., gender-biased hiring models), and **Sample Bias**, where training data fails to represent marginalized groups. This results in facial recognition systems having significantly higher error rates for people of color.
                \n**Filter Bubbles & Echo Chambers:** Recommendation algorithms curate content based on similarity scores, enclosing users in "Filter Bubbles." This intellectual isolation reinforces pre-existing prejudices and eliminates exposure to conflicting viewpoints.
                \n**Algorithmic Erasure:** When certain groups or perspectives are underrepresented in training data, they are effectively "erased" from the model's output, leading to skewed educational content and biased automated decision-making.
            """)

    # --- Pillar 03: Safety Bypasses ---
    with col_inapp:
        st.markdown("#### 🛑 Content Bypasses")
        if is_gated:
            st.warning("Simplified Content")
            st.write("""
                **What it means:** Sometimes people try to "trick" AI into breaking the rules or saying mean things.
                \n**What to do:** If an AI ever says something scary, mean, or tells you to do something dangerous, **close the app immediately** and tell a grown-up.
            """)
        else:
            st.error("Technical Details: Jailbreaking")
            st.write("""
                **Adversarial Prompt Injection:** Attackers use **Character Injection** (zero-width characters) and **Prompt Smuggling** (hiding commands in emojis or hyperlinks) to bypass safety guardrails. 
                \n**Persona Adoption:** The "DAN" (Do Anything Now) exploit shifts a model into a roleplay context, coercing it to disregard policy restrictions and generate harmful instructions (e.g., pharmaceutical recipes or violent blueprints).
                \n**Emotional Coercion:** By framing unethical requests as life-or-death moral dilemmas, attackers exploit the model's objective-alignment to bypass "Ethics" guardrails.
                \n**Data Exfiltration:** Sophisticated prompts can trigger "training data leakage," tricking models into revealing PII (Personally Identifiable Information) embedded in their weights.
            """)

    st.divider()
    st.subheader("Why Critical Thinking is the Ultimate Guardrail")
    st.write("""
        Technical filters are in a permanent arm's race with adversarial engineering. The only sustainable defense is cognitive: 
        developing a **verify-first mindset**. Question the source, scrutinize the intent, and acknowledge that in a synthetic era, 
        seeing is no longer believing.
    """)

def display_literacy_section():
    """Displays the enhanced Literacy section using visual structure and columns."""

    is_gated = st.session_state.get('age_profile') == "Pre-Teen (Gated Content)"  # Add gating check here

    st.header("Practical Guidance for Families & Classrooms 👨‍👩‍👧‍👦")
    st.divider()

    markdown_text = load_markdown_content("literacy_tips.md")
    st.subheader("Digital Literacy and Monitoring: The Ultimate Defense")
    st.write(markdown_text.split("---")[0].strip())

    st.divider()

    # ----------------------------------------------------
    # SECTION 1: CRITICAL EVALUATION (Dynamic Cards/Containers)
    # ----------------------------------------------------
    st.markdown("### 1. Critical Evaluation Skills 🔎")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("#### Source Reliability & Scrutiny")
            st.info("Don't ask 'Is it true?', ask 'Who says so?'")
            with st.expander("Expand for detail"):
                st.write(
                    "Teach verification techniques: reverse image search, cross-checking facts with established news sources, and looking up the author or publisher of the AI model.")

    with col2:
        with st.container(border=True):
            st.markdown("#### Spotting AI Artifacts & Deepfakes")
            st.warning("Learn to detect the uncanny valley.")
            with st.expander("Expand for detail"):
                st.write(
                    "For images: look for unnatural hands, strange text/logos, and inconsistent lighting. For text: look for overly generic language, perfect grammar, and lack of unique insight.")

    with col3:
        with st.container(border=True):
            st.markdown("#### Fact vs. Algorithmic Opinion")
            st.success("AI blends information seamlessly.")
            with st.expander("Expand for detail"):
                st.write(
                    "Help children distinguish between verifiable facts and generated summaries or opinions. Emphasize that AI models do not 'know' things; they predict likely word sequences.")

    st.divider()

    # ----------------------------------------------------
    # SECTION 2: TECHNICAL & SOCIAL SAFEGUARDS
    # ----------------------------------------------------
    st.markdown("### 2. Implementing Safeguards and Rules 🔒")
    col_tools, col_pact = st.columns(2)

    with col_tools:
        st.markdown("#### Technical Tools and Monitoring")
        with st.expander("See Recommended Actions", expanded=True):
            st.markdown("""
            - **Parental Controls:** Use built-in filtering tools on browsers and devices.
            - **Usage Logs:** Regularly check the history/logs of AI chat applications (e.g., ChatGPT, Gemini).
            - **Data Privacy:** Discuss not submitting personal, identifiable information (PII) to public AI tools.
            """)

    with col_pact:
        st.markdown("#### Ethical & Family Pacts")
        with st.expander("Drafting the 'AI Code'", expanded=True):
            st.markdown("""
            - **Define Cheating:** Clearly state when using AI for schoolwork is plagiarism.
            - **Attribution:** Teach children to properly credit AI models (e.g., "AI assisted with outline").
            - **Responsibility:** If AI produces misinformation, the user is responsible for correcting it before sharing.
            """)

    st.divider()

    # ----------------------------------------------------
    # SECTION 3: DEEPER ETHICAL DISCUSSION (Applying Gating Here)
    # ----------------------------------------------------
    st.markdown("### 3. Fostering Ethical and Social Responsibility 🤝")

    if is_gated:
        st.info("Discussion Focus: Responsibility")
        st.write("Focus discussions on empathy: how misuse of AI by others can hurt feelings or reputations online.")
    else:
        st.markdown("""
        Digital citizenship extends beyond safety—it's about empathy and impact. Encourage deep discussion on the social consequences of AI.
        """)

        with st.expander("🗣️ Discussion Prompt: The Impact of Bias"):
            st.markdown("""
            Discuss: If an AI model tends to exclude certain groups in its generated images or text, what negative impact does this have on society? 
            The goal is to teach children that technology is not neutral, and they are part of the solution to make it fair.
            """)

    st.success("Digital literacy is an ongoing conversation—keep the dialogue open!")
    st.caption("Content source: **literacy_tips.md**")


def display_research_section():
    """Displays the enhanced research section, including articles and videos with hyperlinks."""
    st.header("Research and External Resources 📚")
    st.divider()

    st.write(
        "This guide is built upon established ethical, educational, and legislative foundations. Our research ensures that the advice provided is current, responsible, and aligned with global standards.")

    # ----------------------------------------------------
    # 1. CORE RESEARCH SOURCES (DataFrame with Hyperlinks)
    # ----------------------------------------------------
    st.subheader("1. Foundational Documents and Organizations")

    # Load the data from CSV
    sources_df = load_research_sources()

    # CRITICAL: Convert Link column to Markdown links for display, then drop Link column
    if 'Link' in sources_df.columns and 'Source' in sources_df.columns:
        sources_df['Source'] = sources_df.apply(
            lambda row: f"[{row['Source']}]({row['Link']})" if pd.notna(row['Link']) and row['Link'] else row['Source'],
            axis=1
        )
        sources_df = sources_df.drop(columns=['Link'], errors='ignore')

    with st.container(border=True):
        st.markdown("#### 🔗 Core Research Sources")

        # Display as a table; Streamlit renders the Markdown links correctly here
        st.table(sources_df)

        st.caption("These sources provide the ethical and technical foundation for the guide.")

    st.divider()

    # ----------------------------------------------------
    # 2. EXPERT ARTICLES (External Links)
    # ----------------------------------------------------
    st.subheader("2. Expert Articles on Risks and Prevention")
    st.markdown("Read these detailed articles to gain a deeper understanding of the threats and actionable steps.")

    col_art1, col_art2, col_art3 = st.columns(3)

    with col_art1:
        with st.container(border=True):
            st.markdown("#### **AI Safety Tips for Parents**")
            st.markdown("Six top tips covering everything from checking sources to discussing generative AI misuse.")
            st.link_button("Read NSPCC Tips",
                           "https://www.nspcc.org.uk/about-us/news-opinion/2025/artificial-intelligence-safety-tips-for-parents/")

    with col_art2:
        with st.container(border=True):
            st.markdown("#### **Teens Turning to AI for Mental Health**")
            st.markdown(
                "Report on systematic failures of AI chatbots to support teen mental health issues beyond explicit crisis statements.")
            st.link_button("Read Psychiatrist.com Report",
                           "https://www.psychiatrist.com/news/teens-are-turning-to-ai-for-support-a-new-report-says-its-not-safe/")

    with col_art3:
        with st.container(border=True):
            st.markdown("#### **AI Toys are NOT Safe**")
            st.markdown(
                "Advocates warn that AI toys may be powered by the same harmful models and invade family privacy by collecting sensitive data.")
            st.link_button("Read Fairplay Advisory",
                           "https://fairplayforkids.org/wp-content/uploads/2025/11/AI-Toys-Advisory.pdf")

    st.divider()

    # ----------------------------------------------------
    # 3. EDUCATIONAL VIDEOS (YouTube Embeds/Links)
    # ----------------------------------------------------
    st.subheader("3. Educational Videos and Campaigns")
    st.markdown("Watch these videos for visual and auditory explanations of AI safety concepts and risks.")

    col_vid1, col_vid2, col_vid3 = st.columns(3)

    with col_vid1:
        st.markdown("#### **AI is Dangerous, Not Why You Think**")
        st.video("https://www.youtube.com/watch?v=eXdVDhOGqoE")
        st.caption(
            "Focuses on current negative impacts: bias, carbon emissions, and copyright infringement (TED Talk).")

    with col_vid2:
        st.markdown("#### **Ethics and AI in Education**")
        st.video("https://www.youtube.com/watch?v=tcRGJdmu3go")
        st.caption(
            "Khan Academy video exploring ethical considerations, privacy, and risk mitigation in AI educational tools.")

    with col_vid3:
        st.markdown("#### **Risks of AI for Children**")
        st.video("https://www.youtube.com/watch?v=vhlmfX26UJE")
        st.caption("Explores key risks like inappropriate content and potential harms in everyday AI use for families.")

    st.divider()
    st.success("For more deep dives, we encourage exploring resources from global institutions.")


def display_parental_control_section():
    """Renders the Parental Control Section focusing on YouTube Kids, Family Link, and Qustodio."""

    st.header("Practical Parental Controls & Safety Tools 🔒")
    st.divider()

    st.markdown("""
    While the guide focuses on AI literacy, effective digital parenting requires implementing safeguards. We recommend leveraging dedicated, curated platforms and comprehensive monitoring apps for effective management.
    """)

    # ----------------------------------------------------
    # SECTION 1: YouTube Kids (Content Curation)
    # ----------------------------------------------------
    st.subheader("1. Content Curation: YouTube Kids 🛡️")

    col_info, col_controls = st.columns(2)

    with col_info:
        st.markdown("#### Curated, Safer Content")
        st.info("YouTube Kids offers a smaller, curated selection of videos designed for a family audience.")
        st.markdown("""
        * **Age-Based Content:** Content can be aligned with ages (Preschool, Younger, Older).
        * **Reduced Risk:** The platform features **no comment sections** and limited algorithmic 'rabbit hole' effects.
        """)

    with col_controls:
        st.markdown("#### Enhanced Parental Controls")
        st.warning("The platform provides essential tools to guide viewing habits.")
        st.markdown("""
        * **Time Limits:** Parents can set screen time limits using a built-in timer.
        * **Search Restriction:** Parents can restrict users from accessing the search tool.
        """)

    st.divider()

    # ----------------------------------------------------
    # SECTION 2: Comprehensive Monitoring Apps
    # ----------------------------------------------------
    st.subheader("2. Platform & Activity Monitoring")

    col_family, col_qustodio = st.columns(2)

    with col_family:
        with st.container(border=True):
            st.markdown("#### **Google Family Link (Native Control)**")
            st.markdown(
                "Family Link is a **free, native solution** excellent for users primarily on Android and ChromeOS devices.")
            st.markdown("""
            * **Usage Transparency:** Parents can see how their child spends time on their device.
            * **App Management:** Allows setting daily time limits, individual app limits, and requiring approval for new app downloads.
            * **Google Service Filtering:** Provides controls over Google services like Chrome, YouTube, and Search, allowing you to block inappropriate sites.
            """)
            st.link_button("Go to Family Link", "https://families.google/familylink/")

    with col_qustodio:
        with st.container(border=True):
            st.markdown("#### **Qustodio (Cross-Platform & Advanced)**")
            st.markdown(
                "Qustodio is a **comprehensive suite** known for its powerful web filtering and cross-platform support.")
            st.markdown("""
            * **Web & App Blocking:** Excellent at filtering websites by category (e.g., violence, drugs) and blocking games/apps.
            * **Activity Reports:** Provides detailed daily and weekly reports of online activity, browsing history, and YouTube views.
            * **Time Management:** Features daily screen time limits and a "Pause the internet" button for immediate breaks.
            * **AI Chat Monitoring:** Advanced plans include **AI-powered alerts** for concerning searches or messages on social media, which is crucial for monitoring chatbot risks.
            """)
            st.link_button("Go to Qustodio", "https://www.qustodio.com/en/")

    st.divider()

    # ----------------------------------------------------
    # SECTION 3: Launch YouTube Kids (Direct Link)
    # ----------------------------------------------------
    st.subheader("Launch YouTube Kids Directly")

    st.markdown("""
    Use the button below to quickly open the **YouTube Kids website**. Parental involvement remains vital for monitoring.
    """)

    # Custom HTML button to open the link in a new tab
    st.markdown(
        """
        <a href="https://www.youtube.com/kids/" target="_blank">
            <button style="
                background-color: #ffb300; color: #11151c; font-weight: bold;
                border-radius: 12px; padding: 10px 20px; border: none;
                cursor: pointer; font-size: 16px;">
                🚀 Open YouTube Kids Website
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

def display_forensic_module():
        """Interactive Deepfake 'Spot the Difference' Challenge."""
        st.header("Forensic Challenge: Spot the Artifacts 🔍")
        st.markdown("""
            **Instruction:** Closely inspect the image below. AI models often struggle with 'logical physics'—specifically 
            biometrics like earlobes, matching accessories, and hair textures.
        """)

        col_img, col_forensics = st.columns([2, 1])

        with col_img:
            # Forensic Subject: High-resolution deepfake example
            st.image("https://deepseekimagegenerator.in/public/gallery/girl.png",
                     caption="Forensic Subject Analysis: Can you find the glitches?")

        with col_forensics:
            st.subheader("Forensic Checklist")
            st.write("- **Symmetry:** Do earrings or glasses match on both sides?")
            st.write("- **Edges:** Look for blurring where hair meets the background.")
            st.write("- **Texture:** Does the skin look overly smooth or 'waxy'?")

            if st.button("Reveal Artifacts"):
                st.error(
                    "**Artifact 1: Mismatched Symmetry.** Notice the ear structure and accessories often differ because the AI generates each side independently.")
                st.error(
                    "**Artifact 2: 'Liquid' Hair.** Look at the edges; AI struggles with fine strands, often creating a blurry 'halo' effect.")
                st.error("**Artifact 3: Background Warping.** The space around the head may shimmer or look distorted.")
                st.balloons()


# ---------------------------------------------------------


def display_guide():
    """Sets up the Streamlit page, custom CSS, and navigation."""

    st.set_page_config(
        page_title="Enhanced AI Safety Guide",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={'About': 'A comprehensive guide built with Streamlit and Python.'}
    )

    inject_custom_css()

    # --- TOP BANNER (Custom HTML for HIERARCHY) ---
    st.markdown(
        "<h1>🛡️ Safety of AI-Generated Content</h1>",
        unsafe_allow_html=True
    )
    st.markdown("### A Guide for Parents, Educators, and Children")
    st.divider()

    # --- Sidebar Navigation ---
    st.sidebar.title("Guide Sections")

    section_map = {
        "Project Introduction (Start Here)": "INTRO_SECTION",
        "The Risks (Misinformation & Bias)": "risks_misinfo.md",
        "Forensic Challenge: Spot the Fake": "FORENSIC_SECTION",  # Add this
        "Digital Literacy & Monitoring": "literacy_tips.md",
        "Interactive Quiz": "QUIZ_SECTION",
        "Research & Resources": "RESEARCH_SECTION",
        "Community Sharing": "SHARE_SECTION",
        "Parental Controls & Tools": "PARENTAL_CONTROL_SECTION",
    }

    if 'current_section' not in st.session_state:
        st.session_state.current_section = "Project Introduction (Start Here)"

    # Age Gating Widget (placed in the sidebar for control)
    st.sidebar.markdown("### Content Gating 🔒")
    st.sidebar.selectbox(
        "Select User Profile:",
        ["General (All Content)", "Pre-Teen (Gated Content)"],
        key='age_profile'
    )
    st.sidebar.caption("Gating controls exposure to specific deepfake examples.")
    st.sidebar.divider()

    section = st.sidebar.radio(
        "Navigate to:",
        list(section_map.keys()),
        key='section_radio'
    )
    st.session_state.current_section = section

    # --- Content Display Logic ---
    content_key = section_map[st.session_state.current_section]

    if content_key == "INTRO_SECTION":
        display_intro_section()

    elif content_key == "FORENSIC_SECTION":
        display_forensic_module()

    elif content_key == "QUIZ_SECTION":
        st.header("Interactive Quiz: Test Your Knowledge 🧠")
        st.caption(
            "📝 Results are tracked temporarily. **Future Scope:** User profiles will save and track progress over time.")
        st.divider()
        run_quiz()

    elif content_key == "SHARE_SECTION":
        display_sharing_section()

    elif content_key == "PARENTAL_CONTROL_SECTION":
        display_parental_control_section()

    elif content_key == "RESEARCH_SECTION":
        display_research_section()

    elif content_key == "risks_misinfo.md":
        display_risks_section()

    elif content_key == "literacy_tips.md":
        display_literacy_section()


if __name__ == "__main__":
    display_guide()