import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PyPDF2
import docx
from io import BytesIO

load_dotenv()

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Please set your GEMINI_API_KEY in the .env file")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
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

def main():
    st.set_page_config(page_title="Document Chat with Gemini", page_icon="🤖", layout="wide")

    st.title("🤖 Document Chat with Gemini")
    st.subheader("Upload a document and ask questions about it!")

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

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "document_text" not in st.session_state:
        st.session_state.document_text = ""

    if uploaded_file and st.session_state.document_text == "":
        with st.spinner("Processing document..."):
            document_text = process_uploaded_file(uploaded_file)
            if document_text:
                st.session_state.document_text = document_text
                st.success("Document processed successfully! You can now ask questions about it.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your document..."):
        if not st.session_state.document_text:
            st.warning("Please upload a document first!")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
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

                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()