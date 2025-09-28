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
            st.button("Action 3")
        with b_col2:
            if st.button("🗺️ Roadmap"):
                if generate_document_roadmap():
                    st.rerun()
            if st.button("📄 Study Guide"):
                if generate_comprehensive_pdf():
                    st.rerun()
            st.button("Action 6")
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

    # Show flashcards popup if flashcards are generated
    if st.session_state.get('show_flashcards', False):
        show_flashcards_popup()

if __name__ == "__main__":
    main()