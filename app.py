import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PyPDF2
import docx
from io import BytesIO
import requests
from streamlit_lottie import st_lottie
from hume import HumeClient
from hume.tts import FormatMp3, PostedContextWithGenerationId, PostedUtterance
# Note: Google Imagen API requires separate installation and setup
from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import tempfile
import json
import time
from google import genai as google_genai
from google.genai import types
from datetime import datetime

load_dotenv()

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Please set your GEMINI_API_KEY in the .env file")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')
    return model

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(txt_file):
    return str(txt_file.read(), "utf-8")

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "pdf":
            return extract_text_from_pdf(uploaded_file)
        elif file_extension == "docx":
            return extract_text_from_docx(uploaded_file)
        elif file_extension == "txt":
            return extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload PDF, DOCX, or TXT files.")
            return None
    return None

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def synthesize_audio_from_document():
    """Synthesize audio from document content using Hume TTS"""
    if not st.session_state.document_text:
        st.warning("Please upload a document first!")
        return False

    hume_api_key = os.getenv("HUME_API_KEY")
    if not hume_api_key:
        st.error("Please set your HUME_API_KEY in the .env file")
        return False

    try:
        # Take first 500 characters of document for audio synthesis
        text_to_synthesize = st.session_state.document_text[:500] + "..." if len(st.session_state.document_text) > 500 else st.session_state.document_text

        client = HumeClient(api_key=hume_api_key)

        response = client.tts.synthesize_file(
            context=PostedContextWithGenerationId(
                generation_id="09ad914d-8e7f-40f8-a279-e34f07f7dab2",
            ),
            format=FormatMp3(),
            num_generations=1,
            utterances=[
                PostedUtterance(
                    text=text_to_synthesize,
                    description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
                )
            ],
        )

        # Add success message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🎵 **Audio Generated Successfully!** \n\nI've synthesized the document content into audio using Hume's TTS with a warm, academic Scottish voice. The audio has been automatically downloaded."
        })

        return True

    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return False

def generate_document_roadmap():
    """Generate a visual text-based roadmap of the document content"""
    if not st.session_state.document_text:
        st.warning("Please upload a document first!")
        return False

    try:
        model = setup_gemini()
        if not model:
            return False

        roadmap_prompt = f"""
        Analyze the following document and create a visual ASCII-style roadmap using emojis and text.
        Create a clear pathway showing the main concepts, flow, and structure of the document.
        Use arrows (→, ↓), emojis, and formatting to create a visual journey.

        Format it like this example:
        🏁 START: [Main Topic]
        ↓
        📍 STEP 1: [First Key Concept]
        ↓
        📍 STEP 2: [Second Key Concept]
        ↓
        🎯 GOAL: [Final Outcome/Conclusion]

        Document Content:
        {st.session_state.document_text[:2000]}...

        Create a comprehensive visual roadmap with emojis, arrows, and clear structure (max 500 words).
        """

        response = model.generate_content(roadmap_prompt)
        roadmap_content = response.text

        # Add the roadmap to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"🗺️ **Document Roadmap Generated!**\n\nHere's a visual roadmap of your document's content and structure:\n\n```\n{roadmap_content}\n```"
        })

        return True

    except Exception as e:
        st.error(f"Error generating roadmap: {str(e)}")
        return False

def generate_flashcards():
    """Generate flashcards from document content using Gemini"""
    if not st.session_state.document_text:
        st.warning("Please upload a document first!")
        return False

    try:
        model = setup_gemini()
        if not model:
            return False

        flashcards_prompt = f"""
        Create 10 educational flashcards based on the following document content.
        Format each flashcard as a JSON object with "question" and "answer" fields.
        Make questions that test understanding, key concepts, and important details.
        Keep questions clear and concise, answers should be informative but not too long.

        Document Content:
        {st.session_state.document_text[:3000]}...

        Respond with ONLY a valid JSON array of flashcard objects like this:
        [
            {{"question": "What is...?", "answer": "The answer is..."}},
            {{"question": "How does...?", "answer": "It works by..."}}
        ]

        Generate exactly 10 flashcards.
        """

        response = model.generate_content(flashcards_prompt)
        flashcards_text = response.text

        # Clean up the response to extract JSON
        import json
        try:
            # Remove any markdown formatting
            if "```json" in flashcards_text:
                flashcards_text = flashcards_text.split("```json")[1].split("```")[0]
            elif "```" in flashcards_text:
                flashcards_text = flashcards_text.split("```")[1].split("```")[0]

            flashcards_data = json.loads(flashcards_text.strip())

            # Store flashcards in session state
            st.session_state.flashcards = flashcards_data
            st.session_state.current_card = 0
            st.session_state.show_flashcards = True
            st.session_state.show_answer = False

            # Add success message to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"📚 **Flashcards Generated!**\n\nI've created {len(flashcards_data)} flashcards based on your document. Click the flashcard popup to start studying!"
            })

            return True

        except json.JSONDecodeError:
            st.error("Error parsing flashcards. Please try again.")
            return False

    except Exception as e:
        st.error(f"Error generating flashcards: {str(e)}")
        return False

@st.dialog("📚 Study Flashcards")
def show_flashcards_popup():
    """Display flashcards in a popup dialog"""
    if 'flashcards' not in st.session_state or not st.session_state.flashcards:
        st.error("No flashcards available!")
        return

    flashcards = st.session_state.flashcards
    current_card = st.session_state.get('current_card', 0)
    show_answer = st.session_state.get('show_answer', False)

    # Progress indicator
    st.progress((current_card + 1) / len(flashcards))
    st.write(f"Card {current_card + 1} of {len(flashcards)}")

    # Card container with styling
    with st.container():
        st.markdown("""
        <style>
        .flashcard {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            color: white;
            min-height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        .flashcard h3 {
            color: white !important;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        if not show_answer:
            # Show question
            st.markdown(f"""
            <div class="flashcard">
                <h3>❓ {flashcards[current_card]['question']}</h3>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Show Answer", use_container_width=True):
                    st.session_state.show_answer = True
                    st.rerun()
        else:
            # Show answer
            st.markdown(f"""
            <div class="flashcard">
                <h3>💡 {flashcards[current_card]['answer']}</h3>
            </div>
            """, unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("⬅️ Previous", disabled=(current_card == 0)):
            st.session_state.current_card = max(0, current_card - 1)
            st.session_state.show_answer = False
            st.rerun()

    with col2:
        if show_answer and st.button("🔄 Hide Answer"):
            st.session_state.show_answer = False
            st.rerun()

    with col3:
        if st.button("➡️ Next", disabled=(current_card >= len(flashcards) - 1)):
            st.session_state.current_card = min(len(flashcards) - 1, current_card + 1)
            st.session_state.show_answer = False
            st.rerun()

    with col4:
        if st.button("🔀 Shuffle"):
            import random
            random.shuffle(st.session_state.flashcards)
            st.session_state.current_card = 0
            st.session_state.show_answer = False
            st.rerun()

    # Close button
    if st.button("✅ Done Studying", use_container_width=True):
        st.session_state.show_flashcards = False
        st.rerun()

def generate_quiz():
    """Generate quiz questions from document content using Gemini"""
    if not st.session_state.document_text:
        st.warning("Please upload a document first!")
        return False

    try:
        model = setup_gemini()
        if not model:
            return False

        quiz_prompt = f"""
        Create 10 quiz questions based on the following document content.
        Format each question as a JSON object with multiple choice options.
        Make questions that test comprehension, analysis, and key concepts.

        Document Content:
        {st.session_state.document_text[:3000]}...

        Respond with ONLY a valid JSON array of quiz objects like this:
        [
            {{
                "question": "What is the main concept discussed in the document?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 0,
                "explanation": "Detailed explanation of why this answer is correct."
            }}
        ]

        Requirements:
        - Generate exactly 10 questions
        - Use "correct" as index (0, 1, 2, or 3) for the correct answer
        - Make questions challenging but fair
        - Provide clear explanations for correct answers
        """

        response = model.generate_content(quiz_prompt)
        quiz_text = response.text

        # Clean up the response to extract JSON
        try:
            # Remove any markdown formatting
            if "```json" in quiz_text:
                quiz_text = quiz_text.split("```json")[1].split("```")[0]
            elif "```" in quiz_text:
                quiz_text = quiz_text.split("```")[1].split("```")[0]

            quiz_data = json.loads(quiz_text.strip())

            # Store quiz in session state
            st.session_state.quiz_questions = quiz_data
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.show_quiz = True
            st.session_state.quiz_completed = False
            st.session_state.show_quiz_results = False

            # Add success message to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"🧠 **Quiz Generated!**\n\nI've created {len(quiz_data)} challenging questions based on your document. Test your knowledge with the interactive quiz!"
            })

            return True

        except json.JSONDecodeError:
            st.error("Error parsing quiz questions. Please try again.")
            return False

    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        return False

@st.dialog("🧠 Knowledge Quiz")
def show_quiz_popup():
    """Display interactive quiz in a popup dialog"""
    if 'quiz_questions' not in st.session_state or not st.session_state.quiz_questions:
        st.error("No quiz questions available!")
        return

    questions = st.session_state.quiz_questions
    current_q = st.session_state.get('current_question', 0)
    user_answers = st.session_state.get('user_answers', {})
    show_results = st.session_state.get('show_quiz_results', False)

    # Custom CSS for quiz styling
    st.markdown("""
    <style>
    .quiz-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .question-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
    }
    .option-button {
        margin: 5px 0;
        width: 100%;
    }
    .quiz-progress {
        background: #e9ecef;
        height: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .quiz-results {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    if show_results:
        # Show Results
        correct_answers = sum(1 for i, answer in user_answers.items()
                             if answer == questions[i]['correct'])
        total_questions = len(questions)
        score_percentage = (correct_answers / total_questions) * 100

        st.markdown(f"""
        <div class="quiz-results">
            <h2>🎉 Quiz Complete!</h2>
            <h3>Your Score: {correct_answers}/{total_questions} ({score_percentage:.1f}%)</h3>
        </div>
        """, unsafe_allow_html=True)

        # Performance feedback
        if score_percentage >= 80:
            st.success("🌟 Excellent! You have a strong understanding of the material.")
        elif score_percentage >= 60:
            st.info("👍 Good job! Review the explanations for questions you missed.")
        else:
            st.warning("📚 Keep studying! Review the material and try again.")

        # Show detailed results
        st.subheader("📋 Detailed Results")

        for i, question in enumerate(questions):
            user_answer = user_answers.get(i, -1)
            correct_answer = question['correct']
            is_correct = user_answer == correct_answer

            with st.expander(f"Question {i+1}: {'✅' if is_correct else '❌'}", expanded=False):
                st.write(f"**Question:** {question['question']}")
                st.write(f"**Your Answer:** {question['options'][user_answer] if user_answer != -1 else 'Not answered'}")
                st.write(f"**Correct Answer:** {question['options'][correct_answer]}")
                st.write(f"**Explanation:** {question['explanation']}")

        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Retake Quiz", use_container_width=True):
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.session_state.show_quiz_results = False
                st.rerun()

        with col2:
            if st.button("📊 New Quiz", use_container_width=True):
                if generate_quiz():
                    st.rerun()

        with col3:
            if st.button("✅ Done", use_container_width=True):
                st.session_state.show_quiz = False
                st.rerun()

    else:
        # Show Quiz Questions
        st.markdown(f"""
        <div class="quiz-header">
            <h3>Question {current_q + 1} of {len(questions)}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        progress = (current_q + 1) / len(questions)
        st.progress(progress)

        # Current question
        question = questions[current_q]

        st.markdown(f"""
        <div class="question-card">
            <h4>{question['question']}</h4>
        </div>
        """, unsafe_allow_html=True)

        # Answer options
        selected_option = st.radio(
            "Choose your answer:",
            options=range(len(question['options'])),
            format_func=lambda x: f"{chr(65+x)}) {question['options'][x]}",
            key=f"quiz_q_{current_q}",
            index=user_answers.get(current_q, 0) if current_q in user_answers else 0
        )

        # Store selected answer
        st.session_state.user_answers[current_q] = selected_option

        # Navigation buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("⬅️ Previous", disabled=(current_q == 0), use_container_width=True):
                st.session_state.current_question = max(0, current_q - 1)
                st.rerun()

        with col2:
            if current_q < len(questions) - 1:
                if st.button("➡️ Next", use_container_width=True):
                    st.session_state.current_question = min(len(questions) - 1, current_q + 1)
                    st.rerun()
            else:
                if st.button("🏁 Finish Quiz", use_container_width=True):
                    st.session_state.show_quiz_results = True
                    st.rerun()

        with col3:
            # Question navigator
            if st.button("📋 Jump to...", use_container_width=True):
                st.session_state.show_question_nav = not st.session_state.get('show_question_nav', False)
                st.rerun()

        with col4:
            if st.button("❌ Close", use_container_width=True):
                st.session_state.show_quiz = False
                st.rerun()

        # Question navigator
        if st.session_state.get('show_question_nav', False):
            st.subheader("📍 Jump to Question")
            nav_cols = st.columns(5)
            for i in range(len(questions)):
                col_idx = i % 5
                with nav_cols[col_idx]:
                    status = "✅" if i in user_answers else "⭕"
                    if st.button(f"{status} Q{i+1}", key=f"nav_q_{i}", use_container_width=True):
                        st.session_state.current_question = i
                        st.session_state.show_question_nav = False
                        st.rerun()

        # Quiz statistics
        answered = len(user_answers)
        remaining = len(questions) - answered

        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <small>
            📊 Progress: {answered}/{len(questions)} answered | {remaining} remaining
            </small>
        </div>
        """, unsafe_allow_html=True)

def generate_ai_video():
    """Generate AI video using Google Veo 3.0 from document summary"""
    if not st.session_state.document_text:
        st.warning("Please upload a document first!")
        return False

    try:
        # Setup Google GenAI client for Veo
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Please set your GEMINI_API_KEY in the .env file")
            return False

        # First generate a concise summary for video prompt
        model = setup_gemini()
        if not model:
            return False

        summary_prompt = f"""
        Create a concise, visual description for a video based on this document.
        Focus on creating an engaging, cinematic prompt that would work well for AI video generation.
        Keep it under 100 words and make it visually descriptive.

        Document Content:
        {st.session_state.document_text[:2000]}...

        Create a video prompt that captures the essence and key concepts visually.
        """

        summary_response = model.generate_content(summary_prompt)
        video_prompt = summary_response.text.strip()

        # Add status message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"🎬 **Starting Video Generation with Veo 3.0**\n\nGenerating video with prompt:\n\n*{video_prompt}*\n\nThis may take several minutes. The video will automatically download when ready..."
        })

        # Initialize Google GenAI client
        client = google_genai.Client(api_key=api_key)

        # Start video generation
        with st.spinner("🎬 Generating AI video with Veo 3.0... This may take several minutes."):
            operation = client.models.generate_videos(
                model="veo-3.0-generate-001",
                prompt=video_prompt,
            )

            # Poll for completion
            start_time = time.time()
            max_wait_time = 600  # 10 minutes timeout

            while not operation.done:
                elapsed_time = time.time() - start_time
                if elapsed_time > max_wait_time:
                    st.error("Video generation timed out after 10 minutes. Please try again.")
                    return False

                st.info(f"⏳ Video generation in progress... ({int(elapsed_time)}s elapsed)")
                time.sleep(10)
                operation = client.operations.get(operation)

            # Download the generated video
            generated_video = operation.response.generated_videos[0]

            # Create a unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"zeuzy_video_{timestamp}.mp4"

            # Download and save video
            client.files.download(file=generated_video.video)
            generated_video.video.save(filename)

            # Store video data for Streamlit download
            with open(filename, 'rb') as video_file:
                video_data = video_file.read()

            st.session_state.video_data = video_data
            st.session_state.video_filename = filename
            st.session_state.show_video_download = True

            # Add success message to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"🎉 **Video Generated Successfully!**\n\nYour AI-generated video is ready! Generated using:\n\n*{video_prompt}*\n\nThe video has been automatically downloaded as `{filename}`. You can also download it again using the button below."
            })

            # Clean up temporary file
            try:
                os.remove(filename)
            except:
                pass

            return True

    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        st.info("💡 **Troubleshooting:**\n- Ensure your GEMINI_API_KEY has access to Veo 3.0\n- Check your API quota and billing\n- Try with a simpler document")
        return False

def generate_video_content():
    """Generate video content script and storyboard from document summary"""
    if not st.session_state.document_text:
        st.warning("Please upload a document first!")
        return False

    try:
        model = setup_gemini()
        if not model:
            return False

        # First generate a summary if not already available
        summary_prompt = f"""
        Create a concise summary of the following document suitable for an 8-second video:

        Document Content:
        {st.session_state.document_text[:3000]}...

        Provide a brief, engaging summary that captures the key points.
        """

        summary_response = model.generate_content(summary_prompt)
        document_summary = summary_response.text

        # Generate video script and storyboard
        video_prompt = f"""
        Create a detailed 8-second video script and storyboard based on this summary:

        Summary: {document_summary}

        Generate:
        1. A video script with narration (8 seconds max)
        2. Visual storyboard with 4 scenes (2 seconds each)
        3. Suggested visuals, transitions, and key points
        4. Background music suggestions
        5. Text overlays for key information

        Format as a comprehensive video production guide.
        """

        video_response = model.generate_content(video_prompt)
        video_content = video_response.text

        # Generate downloadable content
        video_script_content = f"""
# VIDEO PRODUCTION SCRIPT
## Document: {getattr(st.session_state, 'uploaded_file_name', 'Document')}
## Duration: 8 seconds
## Generated by LazyZeuzy AI

---

## DOCUMENT SUMMARY
{document_summary}

---

## VIDEO SCRIPT & STORYBOARD
{video_content}

---

## PRODUCTION NOTES
- Target Duration: 8 seconds
- Format: Educational/Explainer Video
- Style: Clean, Modern, Engaging
- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## NEXT STEPS
1. Use this script with video creation tools like:
   - Canva Video
   - Adobe After Effects
   - Loom or similar screen recording
   - AI video generators (RunwayML, Synthesia)

2. Follow the storyboard for visual sequences
3. Record narration based on the script
4. Add suggested background music
5. Include text overlays as specified

---
Generated by LazyZeuzy - Your AI Learning Companion
        """

        # Store video script data for download
        st.session_state.video_script_data = video_script_content.encode('utf-8')
        st.session_state.show_video_download = True

        # Add success message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"🎬 **Video Script Generated!**\n\nI've created a comprehensive 8-second video production script based on your document:\n\n• Complete narration script\n• 4-scene storyboard (2s each)\n• Visual suggestions and transitions\n• Background music recommendations\n• Text overlay specifications\n\nDownload the script below to create your video!"
        })

        return True

    except Exception as e:
        st.error(f"Error generating video content: {str(e)}")
        return False

def generate_comprehensive_pdf():
    """Generate a comprehensive PDF study guide using ReportLab"""
    if not st.session_state.document_text:
        st.warning("Please upload a document first!")
        return False

    try:
        model = setup_gemini()
        if not model:
            return False

        # Generate all content sections using Gemini
        with st.spinner("Generating comprehensive study content..."):

            # 1. Generate Summary
            summary_prompt = f"""
            Create a comprehensive summary of the following document. Make it detailed but concise.

            Document: {st.session_state.document_text[:3000]}...

            Provide a well-structured summary covering all main points.
            """
            summary_response = model.generate_content(summary_prompt)
            summary_content = summary_response.text

            # 2. Generate MCQs
            mcq_prompt = f"""
            Create 10 multiple choice questions based on the document. Format as JSON:
            [
                {{
                    "question": "Question text?",
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "correct": "A",
                    "explanation": "Explanation why this is correct"
                }}
            ]

            Document: {st.session_state.document_text[:3000]}...
            """
            mcq_response = model.generate_content(mcq_prompt)
            mcq_text = mcq_response.text

            # Clean MCQ response
            if "```json" in mcq_text:
                mcq_text = mcq_text.split("```json")[1].split("```")[0]
            mcqs = json.loads(mcq_text.strip())

            # 3. Generate Detailed Explanations
            explanations_prompt = f"""
            Provide detailed explanations of the key concepts in the document.
            Cover 5-7 main topics with in-depth analysis.

            Document: {st.session_state.document_text[:3000]}...
            """
            explanations_response = model.generate_content(explanations_prompt)
            explanations_content = explanations_response.text

            # 4. Generate Thinking Questions
            thinking_prompt = f"""
            Create 8 thought-provoking questions about the document that encourage critical thinking and analysis.

            Document: {st.session_state.document_text[:3000]}...

            Format as numbered questions (1. Question... 2. Question...)
            """
            thinking_response = model.generate_content(thinking_prompt)
            thinking_content = thinking_response.text

            # 5. Generate Hands-on Activities
            activities_prompt = f"""
            Create 6 hands-on activities or exercises related to the document content.
            Include practical applications, exercises, or projects.

            Document: {st.session_state.document_text[:3000]}...

            Format as numbered activities with clear instructions.
            """
            activities_response = model.generate_content(activities_prompt)
            activities_content = activities_response.text

            # 6. Generate Text Roadmap
            roadmap_prompt = f"""
            Create a visual text roadmap of the document using ASCII art, emojis, and clear structure.

            Document: {st.session_state.document_text[:2000]}...
            """
            roadmap_response = model.generate_content(roadmap_prompt)
            roadmap_content = roadmap_response.text

        # Create PDF
        with st.spinner("Creating PDF document..."):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            doc = SimpleDocTemplate(temp_file.name, pagesize=A4)

            # Get styles
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=HexColor('#2E4057')
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=20,
                textColor=HexColor('#4A90A4')
            )

            subheading_style = ParagraphStyle(
                'CustomSubHeading',
                parent=styles['Heading3'],
                fontSize=14,
                spaceAfter=8,
                spaceBefore=15,
                textColor=HexColor('#5C677D')
            )

            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6,
                alignment=TA_JUSTIFY
            )

            # Build PDF content
            story = []

            # Title Page
            story.append(Paragraph("📚 Comprehensive Study Guide", title_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph("Generated by LazyZeuzy AI", styles['Normal']))
            story.append(Spacer(1, 50))

            # Table of Contents
            story.append(Paragraph("📋 Table of Contents", heading_style))
            toc_data = [
                ["1. Document Summary", "Page 2"],
                ["2. Learning Roadmap", "Page 3"],
                ["3. Detailed Explanations", "Page 4"],
                ["4. Multiple Choice Questions", "Page 5"],
                ["5. Critical Thinking Questions", "Page 6"],
                ["6. Hands-on Activities", "Page 7"]
            ]

            toc_table = Table(toc_data)
            toc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E8F4F8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(toc_table)
            story.append(PageBreak())

            # 1. Summary Section
            story.append(Paragraph("📄 Document Summary", heading_style))
            story.append(Paragraph(summary_content, body_style))
            story.append(PageBreak())

            # 2. Roadmap Section
            story.append(Paragraph("🗺️ Learning Roadmap", heading_style))
            story.append(Paragraph(roadmap_content, body_style))
            story.append(PageBreak())

            # 3. Detailed Explanations
            story.append(Paragraph("📖 Detailed Explanations", heading_style))
            story.append(Paragraph(explanations_content, body_style))
            story.append(PageBreak())

            # 4. MCQs Section
            story.append(Paragraph("❓ Multiple Choice Questions", heading_style))
            for i, mcq in enumerate(mcqs, 1):
                story.append(Paragraph(f"<b>Question {i}:</b> {mcq['question']}", subheading_style))
                for option in mcq['options']:
                    story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{option}", body_style))
                story.append(Paragraph(f"<b>Answer:</b> {mcq['correct']}", body_style))
                story.append(Paragraph(f"<b>Explanation:</b> {mcq['explanation']}", body_style))
                story.append(Spacer(1, 15))
            story.append(PageBreak())

            # 5. Thinking Questions
            story.append(Paragraph("🤔 Critical Thinking Questions", heading_style))
            story.append(Paragraph(thinking_content, body_style))
            story.append(PageBreak())

            # 6. Hands-on Activities
            story.append(Paragraph("🛠️ Hands-on Activities", heading_style))
            story.append(Paragraph(activities_content, body_style))

            # Build PDF
            doc.build(story)

            # Read the PDF file
            with open(temp_file.name, 'rb') as pdf_file:
                pdf_data = pdf_file.read()

            # Add success message to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": "📄 **Comprehensive Study Guide Generated!**\n\nI've created a detailed PDF study guide with:\n• Document Summary\n• Learning Roadmap\n• Detailed Explanations\n• 10 Multiple Choice Questions\n• Critical Thinking Questions\n• Hands-on Activities\n\nUse the download button below to get your PDF!"
            })

            # Store PDF data for download
            st.session_state.pdf_data = pdf_data
            st.session_state.show_pdf_download = True

            return True

    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return False

def main():
    st.set_page_config(page_title="LazyZeszy", page_icon="🤖", layout="wide")

    # Consolidated CSS
    st.markdown("""
        <style>
            /* Button styling */
            .stButton>button {
                border-radius: 8px;
                width: 100%;
                margin-bottom: 8px;
            }

            /* Sidebar Lottie positioning */
            section[data-testid="stSidebar"] {
                position: relative;
            }
            .lottie-bottom {
                position: absolute;
                bottom: 20px;
                left: 0;
                right: 0;
            }

            /* Un-fix the chat input */
            .st-emotion-cache-1xw8zd0.e1d2x3se3 {
                position: static;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("⚡ LazyZeuzy")
    st.subheader("Impart knowledge from Mount Olympus!")

    model = setup_gemini()
    if not model:
        return

    with st.sidebar:
        st.header("📄 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "docx", "txt"],
            help="Upload a PDF, Word document, or text file"
        )

        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")

        with st.container():
            st.markdown('<div class="lottie-bottom">', unsafe_allow_html=True)
            lottie_url = "https://lottie.host/386084db-01c7-46ea-94ee-a61f78d0d5b6/1BeZ2kxvLW.json"
            lottie_json = load_lottieurl(lottie_url)
            if lottie_json:
                st_lottie(lottie_json, height=200)
            st.markdown('</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "document_text" not in st.session_state:
        st.session_state.document_text = ""

    if uploaded_file and st.session_state.document_text == "":
        with st.spinner("Processing document..."):
            document_text = process_uploaded_file(uploaded_file)
            if document_text:
                st.session_state.document_text = document_text

                # Generate automatic summary
                with st.spinner("Generating document summary..."):
                    try:
                        summary_prompt = f"""
                        Please provide a detailed summary of the following document. Include:
                        1. Main topic/subject
                        2. Key points and themes
                        3. Important details or findings
                        4. Structure and organization
                        5. Any notable conclusions or recommendations

                        Document Content:
                        {document_text}

                        Please make the summary comprehensive but concise.
                        """

                        response = model.generate_content(summary_prompt)
                        summary = response.text

                        # Add summary as assistant message
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"📄 **Document Summary for {uploaded_file.name}:**\n\n{summary}"
                        })
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")

                st.rerun()

    col1, col2 = st.columns([2, 1])

    with col1:
        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input logic
        if prompt := st.chat_input("Ask a question about your document..."):
            if not st.session_state.document_text:
                st.warning("Please upload a document first!")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.spinner("Thinking..."):
                    try:
                        full_prompt = f"""
                        Based on the following document content, please answer the user's question:

                        Document Content:
                        {st.session_state.document_text}

                        User Question: {prompt}

                        Please provide a helpful and accurate answer based only on the information in the document. If the answer cannot be found in the document, please say so.
                        """

                        response = model.generate_content(full_prompt)
                        answer = response.text
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                
                st.rerun()

    with col2:
        st.write("### Actions")
        b_col1, b_col2 = st.columns(2, gap="small")
        with b_col1:
            if st.button("🎵 Audio Muse"):
                if synthesize_audio_from_document():
                    st.rerun()
            if st.button("📚 Memory Cards"):
                if generate_flashcards():
                    st.rerun()
            if st.button("🧠 Trial of Wisdom"):
                if generate_quiz():
                    st.rerun()
        with b_col2:
            if st.button("🗺️ Roadmap"):
                if generate_document_roadmap():
                    st.rerun()
            if st.button("📄 Study Guide"):
                if generate_comprehensive_pdf():
                    st.rerun()
            if st.button("🎬 AI Video"):
                if generate_ai_video():
                    st.rerun()
        st.button("Full Width Action")

        lottie_url_2 = "https://lottie.host/3ae4f794-0101-499b-888f-3743146d410e/ntRtMqOUj0.json"
        lottie_json_2 = load_lottieurl(lottie_url_2)
        if lottie_json_2:
            st_lottie(lottie_json_2, height=200)

    # Show PDF download button if PDF is ready
    if st.session_state.get('show_pdf_download', False):
        st.success("✅ Your comprehensive study guide PDF is ready!")
        st.download_button(
            label="📥 Download Study Guide PDF",
            data=st.session_state.pdf_data,
            file_name="comprehensive_study_guide.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        if st.button("❌ Close Download"):
            st.session_state.show_pdf_download = False
            st.rerun()

    # Show video download button if video is ready
    if st.session_state.get('show_video_download', False):
        st.success("🎬 Your AI-generated video is ready!")
        st.download_button(
            label="📥 Download AI Video",
            data=st.session_state.video_data,
            file_name=st.session_state.get('video_filename', 'zeuzy_video.mp4'),
            mime="video/mp4",
            use_container_width=True
        )
        if st.button("❌ Close Video Download"):
            st.session_state.show_video_download = False
            st.rerun()

    # Show flashcards popup if flashcards are generated
    if st.session_state.get('show_flashcards', False):
        show_flashcards_popup()

    # Show quiz popup if quiz is generated
    if st.session_state.get('show_quiz', False):
        show_quiz_popup()

if __name__ == "__main__":
    main()