
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop()

# --- Helper Functions ---
def get_content_from_url(url):
    """Fetches and parses the text content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return None

def get_content_from_file(uploaded_file):
    """Reads content from an uploaded file."""
    if uploaded_file is not None:
        return uploaded_file.read().decode("utf-8")
    return None

# --- UI Elements ---
st.set_page_config(page_title="Gemini Playground", layout="wide")
st.title("Gemini Playground")

# Sidebar for options
with st.sidebar:
    st.header("Options")
    mode = st.selectbox("Choose a mode:", ["Chat", "Flashcards", "MCQ Quiz", "Video Summary"])
    
    st.subheader("Input")
    input_method = st.radio("Choose input method:", ["URL", "File Upload"])

    content = None
    if input_method == "URL":
        url = st.text_input("Enter a URL:")
        if url:
            content = get_content_from_url(url)
    else:
        uploaded_file = st.file_uploader("Upload a document or video:")
        if uploaded_file:
            content = get_content_from_file(uploaded_file)

    st.subheader("Gemini Models")
    model_name = st.selectbox("Select a model:", ["models/gemini-pro-latest", "models/gemini-2.5-pro", "models/gemini-2.5-flash"])


# --- Main Content ---
if mode == "Chat":
    st.header("Chat with your document")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if content:
        st.text_area("Content:", content, height=200)
        
        for author, text in st.session_state.chat_history:
            st.markdown(f"**{author}:** {text}")

        prompt = st.text_input("Ask a question:")
        if st.button("Send"):
            if prompt:
                st.session_state.chat_history.append(("You", prompt))
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(f"Based on the following content, answer the user's question.\nContent:\n{content}\n\nQuestion: {prompt}")
                st.session_state.chat_history.append(("Bot", response.text))
                st.rerun()


elif mode == "Flashcards":
    st.header("Generate Flashcards")

    if 'flashcards' not in st.session_state:
        st.session_state.flashcards = []
        st.session_state.card_index = 0
        st.session_state.show_answer = False

    if content:
        st.text_area("Content:", content, height=200)
        if st.button("Generate Flashcards"):
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(f"Based on the following content, generate a set of flashcards. Each flashcard should have a question and an answer, separated by '---'.\nContent:\n{content}")
            flashcards_text = response.text.split('\n\n')
            st.session_state.flashcards = [card.split('---') for card in flashcards_text if '---' in card]
            st.session_state.card_index = 0
            st.session_state.show_answer = False
            st.rerun()

    if st.session_state.flashcards:
        card = st.session_state.flashcards[st.session_state.card_index]
        question = card[0]
        answer = card[1]

        st.markdown(f"**Question:** {question}")

        if st.session_state.show_answer:
            st.markdown(f"**Answer:** {answer}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Previous") and st.session_state.card_index > 0:
                st.session_state.card_index -= 1
                st.session_state.show_answer = False
                st.rerun()
        with col2:
            if st.button("Flip"):
                st.session_state.show_answer = not st.session_state.show_answer
                st.rerun()
        with col3:
            if st.button("Next") and st.session_state.card_index < len(st.session_state.flashcards) - 1:
                st.session_state.card_index += 1
                st.session_state.show_answer = False
                st.rerun()


elif mode == "MCQ Quiz":
    st.header("Generate MCQ Quiz")

    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
        st.session_state.question_index = 0
        st.session_state.selected_option = None
        st.session_state.show_feedback = False

    if content:
        st.text_area("Content:", content, height=200)
        if st.button("Generate MCQ Quiz"):
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(f"Based on the following content, generate a multiple-choice quiz. Each question should have four options and a correct answer. Format each question as: Question\n A) Option 1\n B) Option 2\n C) Option 3\n D) Option 4\nAnswer: Correct Answer\n\n. \nContent:\n{content}")
            
            questions_text = response.text.strip().split('\n\n')
            st.session_state.quiz_questions = []
            for q_text in questions_text:
                lines = q_text.strip().split('\n')
                if len(lines) >= 6:
                    question = lines[0]
                    options = [line.strip() for line in lines[1:5]]
                    answer = lines[5].replace("Answer: ", "").strip()
                    st.session_state.quiz_questions.append({"question": question, "options": options, "answer": answer})
            
            st.session_state.question_index = 0
            st.session_state.selected_option = None
            st.session_state.show_feedback = False
            st.rerun()

    if st.session_state.quiz_questions:
        question_data = st.session_state.quiz_questions[st.session_state.question_index]
        st.markdown(f"**Question {st.session_state.question_index + 1}:** {question_data['question']}")
        
        options = question_data['options']
        st.session_state.selected_option = st.radio("Choose your answer:", options, key=f"q{st.session_state.question_index}")

        if st.button("Check Answer"):
            st.session_state.show_feedback = True
            st.rerun()

        if st.session_state.show_feedback:
            if st.session_state.selected_option == question_data['answer']:
                st.success("Correct!")
            else:
                st.error(f"Incorrect. The correct answer is: {question_data['answer']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Question") and st.session_state.question_index > 0:
                st.session_state.question_index -= 1
                st.session_state.selected_option = None
                st.session_state.show_feedback = False
                st.rerun()
        with col2:
            if st.button("Next Question") and st.session_state.question_index < len(st.session_state.quiz_questions) - 1:
                st.session_state.question_index += 1
                st.session_state.selected_option = None
                st.session_state.show_feedback = False
                st.rerun()





elif mode == "Video Summary":
    st.header("Generate Video Summary from Document")

    if input_method == "File Upload" and uploaded_file is not None:
        st.text_area("Content:", content, height=200)

        if st.button("Generate Video Summary"):
            with st.spinner("Generating video summary... This may take a while."):
                try:
                    # Step 1: Summarize the text using a text-based model
                    text_model = genai.GenerativeModel(model_name)
                    summary_response = text_model.generate_content(f"Summarize the following content for a video script:\n{content}")
                    summary_text = summary_response.text

                    st.subheader("Generated Summary:")
                    st.markdown(summary_text)

                    # Step 2: Generate a video using the Wan 2.2 model
                    st.subheader("Generated Video:")
                    from diffusers import DiffusionPipeline
                    import torch

                    pipe = DiffusionPipeline.from_pretrained("Wan-AI/Wan2.2-Animate-14B", torch_dtype=torch.float16, variant="fp16")
                    pipe.to("cuda")

                    # Generate video
                    video_frames = pipe(summary_text, num_inference_steps=25, num_frames=16).frames

                    # Save video to a temporary file
                    video_path = "temp_video.mp4"
                    from moviepy.editor import ImageSequenceClip
                    clip = ImageSequenceClip(video_frames, fps=8)
                    clip.write_videofile(video_path, codec="libx264")

                    st.video(video_path)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a document to generate a video summary.")



