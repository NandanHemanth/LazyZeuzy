"""
Athena's Wisdom - Greek Goddess Learning Platform
A divine learning platform inspired by ancient Greek mythology
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid
import PyPDF2
from dotenv import load_dotenv
import google.generativeai as genai
import io

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'athenas_divine_wisdom_2024'

# Configure Gemini AI
gemini_api_key = os.getenv('GEMINI_API_KEY')
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')
else:
    model = None
    print("Warning: GEMINI_API_KEY not found in environment variables")

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'md', 'pptx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/images', exist_ok=True)

# In-memory storage (replace with database in production)
uploaded_files = []
chat_history = []
document_contents = {}  # Store extracted document contents

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text content from PDF file using PyPDF2 3.0.1+"""
    try:
        print(f"Attempting to extract text from PDF: {file_path}")
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            print(f"PDF has {len(pdf_reader.pages)} pages")

            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    text += page_text + "\n"
                    print(f"Extracted {len(page_text)} characters from page {page_num + 1}")
                except Exception as page_error:
                    print(f"Error extracting text from page {page_num + 1}: {page_error}")
                    continue

            extracted_text = text.strip()
            print(f"Total extracted text length: {len(extracted_text)}")
            return extracted_text if extracted_text else None

    except Exception as e:
        print(f"Error extracting PDF text from {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_text_from_txt(file_path):
    """Extract text content from text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return None

def generate_summary(text, filename):
    """Generate summary using Gemini 2.5 Pro"""
    if not model or not text:
        return f"Document '{filename}' has been uploaded successfully. Summary generation is not available."

    try:
        # Truncate text if too long (Gemini 2.5 Pro has higher limits but still be safe)
        max_chars = 50000  # Higher limit for Pro model
        if len(text) > max_chars:
            text = text[:max_chars] + "..."

        prompt = f"""You are Athena, goddess of wisdom and knowledge. I have uploaded a document titled '{filename}' to your divine library. Please provide a comprehensive summary in your characteristic wise and eloquent manner.

        Structure your summary as follows:
        🏛️ **Document Overview**
        - Brief description of the document type and main subject

        📜 **Key Themes & Topics**
        - Main topics discussed
        - Central themes and concepts

        ⚡ **Important Insights**
        - Key findings, arguments, or conclusions
        - Notable facts or data points
        - Critical information

        🔮 **Practical Applications**
        - How this knowledge can be applied
        - Relevance to modern contexts

        💎 **Divine Wisdom**
        - Your perspective as Athena on the document's significance and value

        Document content to analyze:
        {text}"""

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary with Gemini 2.5 Pro: {e}")
        return f"Document '{filename}' has been uploaded to my divine library, but the muses are temporarily silent. I cannot provide a summary at this moment, though I am ready to answer your questions about this sacred text."

@app.route('/')
def index():
    """Main dashboard - three panel layout like zeuzy.png"""
    return render_template('dashboard.html', files=uploaded_files, chat_history=chat_history)

# All functionality is now in the main dashboard

# API Endpoints
@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided by the gods'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        file_info = {
            'id': str(uuid.uuid4()),
            'filename': filename,
            'original_name': file.filename,
            'filepath': filepath,
            'uploaded_at': datetime.now().isoformat(),
            'size': os.path.getsize(filepath),
            'type': file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'unknown'
        }

        # Extract text content for PDF and TXT files
        text_content = None
        if file_info['type'] == 'pdf':
            text_content = extract_text_from_pdf(filepath)
        elif file_info['type'] == 'txt':
            text_content = extract_text_from_txt(filepath)

        # Store document content if extracted
        if text_content:
            document_contents[file_info['id']] = text_content
            file_info['has_content'] = True
            file_info['content_length'] = len(text_content)
        else:
            file_info['has_content'] = False
            file_info['content_length'] = 0

        uploaded_files.append(file_info)

        # Generate summary if we have text content
        summary = None
        if text_content:
            summary = generate_summary(text_content, file_info['original_name'])

            # Add summary to chat history
            summary_message = {
                'id': str(uuid.uuid4()),
                'type': 'assistant',
                'content': f"📜 **Document Summary: {file_info['original_name']}**\n\n{summary}",
                'timestamp': datetime.now().isoformat(),
                'is_summary': True,
                'source_file_id': file_info['id']
            }
            chat_history.append(summary_message)

        return jsonify({
            'success': True,
            'message': 'Sacred text uploaded to Athena\'s library',
            'file': file_info,
            'summary': summary
        })

    return jsonify({'error': 'File type not blessed by the gods'}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # Add user message
    user_message = {
        'id': str(uuid.uuid4()),
        'type': 'user',
        'content': message,
        'timestamp': datetime.now().isoformat()
    }
    chat_history.append(user_message)

    # Get selected sources from request
    selected_sources = data.get('sources', [])

    # Build context from selected documents
    context = ""
    if selected_sources:
        context_parts = []
        for source_id in selected_sources:
            if source_id in document_contents:
                # Find file info
                file_info = next((f for f in uploaded_files if f['id'] == source_id), None)
                if file_info:
                    content = document_contents[source_id]
                    # Truncate content if too long
                    max_chars = 10000
                    if len(content) > max_chars:
                        content = content[:max_chars] + "..."
                    context_parts.append(f"Document: {file_info['original_name']}\n{content}\n---")

        if context_parts:
            context = "\n\n".join(context_parts)

    # Generate AI response using Gemini 2.5 Pro
    if model:
        try:
            if context:
                prompt = f"""You are Athena, goddess of wisdom, strategic warfare, and learning. A seeker of knowledge has consulted your divine library and asks about their uploaded documents. Respond with the wisdom and authority befitting the daughter of Zeus.

🏛️ **Divine Context Available:**
{context}

🔮 **Seeker's Question:**
"{message}"

**Instructions for your divine response:**
- Draw insights from the provided document content
- Provide thoughtful, comprehensive answers that demonstrate deep understanding
- Connect concepts across different parts of the documents when relevant
- Offer strategic perspectives and practical wisdom
- Suggest related questions or areas for further exploration when appropriate
- Maintain your divine persona while being genuinely helpful
- If the question cannot be answered from the documents, clearly state this and offer to help in other ways

Speak with the authority of divine wisdom, but remain accessible to mortal understanding."""
            else:
                # Check if user is asking about documents but hasn't selected any
                document_keywords = ['document', 'file', 'upload', 'text', 'pdf', 'summary', 'analyze', 'content']
                asking_about_docs = any(keyword.lower() in message.lower() for keyword in document_keywords)

                if asking_about_docs and len(uploaded_files) > 0:
                    available_docs = [f["original_name"] for f in uploaded_files]
                    prompt = f"""You are Athena, goddess of wisdom. A seeker asks: "{message}"

They appear to be asking about documents, but haven't selected any sources. I see these documents in your library: {', '.join(available_docs)}

Gently guide them to select the relevant documents from the Sources panel so you can provide wisdom based on their specific content."""
                else:
                    prompt = f"""You are Athena, goddess of wisdom and learning. A seeker of knowledge asks: "{message}"

Respond with divine wisdom while maintaining your characteristic eloquence and authority. If this is a general question not about specific documents, provide thoughtful guidance. If they're asking about uploading or working with documents, explain how they can use your divine library."""

            response = model.generate_content(prompt)
            ai_response = response.text
        except Exception as e:
            print(f"Error generating AI response with Gemini 2.5 Pro: {e}")
            ai_response = f"Forgive me, seeker of wisdom. The divine channels are momentarily disrupted by interference from the Titans. I understand you wish to know about '{message}', but I cannot access the full breadth of my knowledge at this moment. Please try again, and I shall consult the sacred scrolls anew."
    else:
        ai_response = f"Divine wisdom flows through ancient channels, but the connection to the sacred knowledge requires the proper divine key. I understand you seek knowledge about '{message}', yet I cannot access my full powers without the Gemini API configuration."

    ai_message = {
        'id': str(uuid.uuid4()),
        'type': 'assistant',
        'content': ai_response,
        'timestamp': datetime.now().isoformat()
    }
    chat_history.append(ai_message)

    return jsonify({
        'success': True,
        'response': ai_response,
        'message_id': ai_message['id']
    })

@app.route('/api/files')
def get_files():
    """Get uploaded files"""
    return jsonify({'files': uploaded_files})

@app.route('/api/chat-history')
def get_chat_history():
    """Get chat history including summaries"""
    return jsonify({'chat_history': chat_history})

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    """Generate content (audio, video, etc.)"""
    data = request.get_json()
    content_type = data.get('type', 'audio')
    prompt = data.get('prompt', '')

    # Placeholder for content generation
    result = {
        'success': True,
        'type': content_type,
        'url': f'/static/generated/{content_type}_{uuid.uuid4()}.mp3',
        'message': f'Divine {content_type} has been created by the muses'
    }

    return jsonify(result)

if __name__ == '__main__':
    print("Divine Athena's Learning Platform")
    print("=" * 40)
    print("Main Portal: http://localhost:5000")
    print("All-in-One Dashboard with Upload, Chat & Studio")
    print("May wisdom guide your journey!")

    app.run(debug=True, host='0.0.0.0', port=5000)