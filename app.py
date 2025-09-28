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
            st.button("Action 2")
            st.button("Action 3")
        with b_col2:
            st.button("Action 4")
            st.button("Action 5")
            st.button("Action 6")
        st.button("Full Width Action")

        lottie_url_2 = "https://lottie.host/3ae4f794-0101-499b-888f-3743146d410e/ntRtMqOUj0.json"
        lottie_json_2 = load_lottieurl(lottie_url_2)
        if lottie_json_2:
            st_lottie(lottie_json_2, height=200)

if __name__ == "__main__":
    main()