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

app = Flask(__name__)
app.secret_key = 'athenas_divine_wisdom_2024'

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main dashboard - three panel layout like zeuzy.png"""
    return render_template('dashboard.html', files=uploaded_files, chat_history=chat_history)

@app.route('/upload')
def upload_page():
    """Upload page inspired by uploading_docs.png"""
    return render_template('upload.html')

@app.route('/chat')
def chat_page():
    """Dedicated chat page"""
    return render_template('chat.html', files=uploaded_files, chat_history=chat_history)

@app.route('/studio')
def studio_page():
    """Creative studio page with tools"""
    return render_template('studio.html')

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

        uploaded_files.append(file_info)

        return jsonify({
            'success': True,
            'message': 'Sacred text uploaded to Athena\'s library',
            'file': file_info
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

    # Placeholder AI response (integrate your AI here)
    ai_response = f"Athena's wisdom: I understand you wish to know about '{message}'. Let me consult the sacred scrolls and provide divine insight."

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
    print("Upload Sacred Texts: http://localhost:5000/upload")
    print("Divine Chat: http://localhost:5000/chat")
    print("Creative Studio: http://localhost:5000/studio")
    print("May wisdom guide your journey!")

    app.run(debug=True, host='0.0.0.0', port=5000)