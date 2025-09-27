# ⚡ Athena's Wisdom - Divine Greek Goddess Learning Platform ⚡

A revolutionary learning platform inspired by ancient Greek mythology, featuring an immersive Greek goddess theme with **Lottie animations**, **divine interactions**, **marble columns**, **golden particle effects**, and **authentic Greek design elements**.

## Features

### 🏛️ **Enhanced Divine Interface**
- **Authentic Greek goddess theme** with marble textures and golden particles
- **Lottie animations** from LottieFiles for smooth, professional animations
- **Responsive design** inspired by ancient Greek temples and architecture
- **Advanced particle system** with floating divine orbs and sparkle trails
- **Interactive hover effects** with divine auras and floating tooltips
- **Smooth transitions** and **cubic-bezier animations** throughout
- **Greek key patterns** and **column animations** for authenticity
- **Parallax scrolling effects** for immersive experience

### 📚 **Upload Sacred Sources**
- Drag and drop file upload
- Support for PDF, TXT, Markdown, Audio (MP3, WAV), Images, and PowerPoint files
- Google Drive integration placeholder
- Website and YouTube URL processing
- Text paste functionality

### 💬 **Divine Chat Interface**
- Three-panel dashboard layout (Sources | Chat | Studio)
- AI-powered chat with Athena persona
- Source-aware conversations
- Conversation starters and suggested prompts

### 🎨 **Creative Studio**
- **Audio Overview**: AI-generated narrated summaries
- **Video Overview**: Divine video presentations
- **Mind Map**: Visual knowledge constellation mapping
- **Divine Reports**: Comprehensive analysis documents
- **Flashcards**: Blessed memory cards by Mnemosyne
- **Quiz Generator**: Divine knowledge assessments

## Installation

1. **Clone or download the Greek folder**

2. **Install dependencies**:
   ```bash
   pip install flask flask-cors werkzeug
   ```

3. **Run the application**:
   ```bash
   cd Greek
   python app.py
   ```

4. **Access the platform**:
   - Main Dashboard: http://localhost:5000
   - Upload Page: http://localhost:5000/upload
   - Chat Interface: http://localhost:5000/chat
   - Creative Studio: http://localhost:5000/studio

## API Endpoints

### File Management
- `POST /api/upload` - Upload files to the divine library
- `GET /api/files` - Retrieve uploaded files

### Chat System
- `POST /api/chat` - Send messages to Athena for divine wisdom
- Chat history is maintained in memory

### Content Generation
- `POST /api/generate-content` - Create divine content (audio, video, etc.)

## File Structure

```
Greek/
├── app.py                 # Main Flask application
├── templates/            # HTML templates
│   ├── dashboard.html    # Three-panel dashboard
│   ├── upload.html      # File upload interface
│   ├── chat.html        # Dedicated chat page
│   └── studio.html      # Creative studio tools
├── static/
│   ├── css/
│   │   └── goddess.css  # Greek goddess theme styling
│   └── js/
│       ├── dashboard.js # Dashboard functionality
│       ├── upload.js    # Upload interactions
│       ├── chat.js      # Chat interface
│       └── studio.js    # Studio tools
├── uploads/             # User uploaded files
└── README.md           # This file
```

## Customization

### Adding AI Integration
Replace the placeholder AI responses in `app.py` with your preferred AI service:

```python
# In the /api/chat route
response = your_ai_service.generate(prompt, context)
```

### Database Integration
Replace the in-memory storage with a proper database:

```python
# Replace these lists with database models
uploaded_files = []  # -> File model
chat_history = []    # -> Chat model
```

### Content Generation
Implement actual content generation in the `/api/generate-content` endpoint using your preferred AI services.

## Theme Customization

The Greek goddess theme uses CSS custom properties for easy customization:

```css
:root {
    --olympus-gold: #D4AF37;     # Divine gold color
    --divine-blue: #4A90E2;      # Athena's blue
    --marble-white: #F8F6F0;     # Marble white
    --temple-stone: #2C1810;     # Dark temple stone
}
```

## Browser Support

- Modern browsers with CSS Grid and Flexbox support
- Chrome 70+, Firefox 65+, Safari 12+, Edge 79+

## License

This is a template project for educational and development purposes.

## Inspiration

Inspired by ancient Greek mythology, classical architecture, and divine wisdom of Athena, goddess of knowledge and learning.

---

*May the gods guide your learning journey!* ⚡🏛️