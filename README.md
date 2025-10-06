# LazyZeuzy - Beyond Google's NotebookLM

A beautiful Streamlit application themed around Greek goddesses, featuring a RAG (Retrieval-Augmented Generation) chatbot named Hera with interactive learning tools.

## ✨ Features

### 🎨 Greek Goddesses Theme
- Beautiful gradient backgrounds and Greek-inspired styling
- Custom fonts (Cinzel) for an authentic ancient feel
- Lottie animations for enhanced user experience
- Goddess-themed UI elements and colors

### 💬 Hera RAG Chatbot
- Interactive chat interface with Hera, Queen of the Gods
- Document upload functionality (PDF and TXT files)
- RAG-powered responses (ready for integration with your preferred LLM)
- Contextual responses based on uploaded documents

### 🎯 Learning Widgets (2x3 Grid)
- **🎥 Video Oracle**: Generate educational videos
- **🎵 Audio Muse**: Create audio content
- **📚 Memory Cards**: Generate flashcards for studying
- **❓ Trial of Wisdom**: Interactive quizzes
- **📊 Oracle's Report**: Analytical reports
- **🛠️ Forge of Learning**: Hands-on exercises

### 📖 Story Mode
- Large dedicated button for immersive story-based learning
- Mythological narrative experiences
- Quest-based learning adventures

## 🚀 Quick Start

### Option 1: Using the Launcher (Recommended)
```bash
python run_hera.py
```

### Option 2: Manual Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run hera_app.py
```

## 📋 Requirements

- Python 3.7+
- Streamlit
- Pillow (PIL)
- streamlit-lottie (optional, for animations)

## 🏗️ Project Structure

```
├── hera_app.py          # Main enhanced Streamlit application
├── app.py               # Basic version of the application  
├── run_hera.py          # Launcher script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎨 Customization

### Adding Your RAG Backend
The application is designed to be easily integrated with your preferred RAG system. Look for the comment `[This is where the RAG system would process your documents]` in the chat interface to add your implementation.

### Modifying Themes
- Edit the CSS in the `st.markdown()` sections to customize colors and styling
- Replace Lottie animation URLs with your preferred animations
- Modify the goddess names and themes in the text content

### Adding New Widgets
Add new learning tools by:
1. Creating new button elements in the `render_widgets()` function
2. Adding corresponding functionality for each widget
3. Updating the styling as needed

## 🌟 Features in Detail

### Sidebar Upload
- Drag-and-drop file upload interface
- Support for multiple file types (TXT, PDF)
- Real-time file processing feedback
- Document management with file details

### Chat Interface  
- Persistent chat history
- Contextual responses based on uploaded documents
- Greek mythology-themed responses
- Real-time message streaming

### Interactive Widgets
Each widget is designed to trigger specific learning modes:
- **Video**: Educational content generation
- **Audio**: Podcast/audio lesson creation  
- **Flashcards**: Spaced repetition learning
- **Quizzes**: Knowledge assessment
- **Reports**: Analytics and progress tracking
- **Hands-on**: Interactive exercises

## 🔧 Technical Details

- **Framework**: Streamlit
- **Styling**: Custom CSS with Greek theme
- **Animations**: Lottie files for enhanced UX
- **Layout**: Responsive design with sidebar and main content areas
- **State Management**: Streamlit session state for chat persistence

## 🤝 Contributing

Feel free to contribute by:
- Adding new Greek goddess themes
- Improving the UI/UX design
- Integrating with different RAG backends
- Adding new learning widget types
- Enhancing the story mode functionality

## 📜 License

This project is open source and available under the MIT License.

---

*May the wisdom of the gods guide your learning journey! 🏛️⚡*
