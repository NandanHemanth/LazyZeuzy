# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LazyZeuzy is a dual-purpose Python project combining:

1. **Streamlit RAG Chatbot** (`app.py`) - A Greek mythology-themed document Q&A application using Google's Gemini API
2. **Adaptive Accessibility Computer Vision System** (`adaptive_accessibility.py`) - A comprehensive CV system for tracking learning states, emotions, and accessibility needs

## Running the Applications

### Streamlit RAG App
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment (required)
# Create .env file with:
# GEMINI_API_KEY="your_gemini_api_key"

# Run the main application
streamlit run app.py
```

### Adaptive Accessibility System
```bash
# Run the computer vision accessibility tracker
python adaptive_accessibility.py
```

## Common Development Commands

### Dependencies Management
```bash
# Install all dependencies (includes heavy ML libraries)
pip install -r requirements.txt

# Core Streamlit dependencies only
pip install streamlit Pillow streamlit-lottie python-dotenv google-generativeai beautifulsoup4 moviepy PyPDF2 python-docx

# Computer Vision dependencies (large downloads)
pip install opencv-python numpy pandas matplotlib seaborn plotly deepface mediapipe tensorflow scikit-learn tf-keras
```

### Testing and Development
```bash
# Run Streamlit in development mode with auto-reload
streamlit run app.py --server.runOnSave=true

# Test CV system with mock data (no camera required)
python adaptive_accessibility.py --demo-mode

# Check Python syntax
python -m py_compile app.py
python -m py_compile adaptive_accessibility.py
```

## Architecture Overview

### Streamlit App (`app.py`)
- **Document Processing**: Supports PDF, DOCX, and TXT file uploads with text extraction using PyPDF2 and python-docx
- **RAG Implementation**: Uses Gemini 2.5-flash model (not 2.5-pro) for document-based Q&A
- **UI Theme**: Greek mythology styling with custom CSS and Lottie animations
- **State Management**: Uses `st.session_state` for chat history and document content
- **Layout**: Single-column chat interface with sidebar for file uploads
- **File Processing Pipeline**: `process_uploaded_file()` → format-specific extractors → Gemini processing

### Adaptive Accessibility System (`adaptive_accessibility.py`)
- **Computer Vision**: Uses MediaPipe for face detection and gesture recognition
- **Emotion Analysis**: DeepFace integration for real-time emotion detection
- **Accessibility Assessment**: Tracks visual, motor, attention, and cognitive indicators
- **Analytics**: Comprehensive reporting with matplotlib/plotly visualizations
- **Data Classes**: Uses `@dataclass` for `AccessibilityAssessment` and `LearningState` structures
- **Real-time Processing**: `AdaptiveLearningCV` class handles live webcam analysis
- **Export Functionality**: Generates JSON reports with embedded Plotly visualizations

## Key Dependencies

- **Streamlit**: Web application framework
- **google-generativeai**: Gemini API integration
- **OpenCV**: Computer vision operations
- **MediaPipe**: Face and gesture detection
- **DeepFace**: Emotion recognition
- **PyPDF2/python-docx**: Document text extraction
- **plotly/matplotlib**: Data visualization

## File Structure

```
├── app.py                          # Main Streamlit RAG application
├── adaptive_accessibility.py       # CV accessibility tracking system
├── requirements.txt                # Python dependencies (heavy ML libs included)
├── .env                           # API keys (GEMINI_API_KEY required)
├── Images/                        # Greek-themed UI assets (greek1.png - greek12.png)
├── Greek/                         # Additional Greek theme assets
├── sample_analytics_report.json   # Example analytics output with Plotly charts
├── README.md                      # Project documentation
└── CLAUDE.md                      # This file (development guidance)
```

## Development Notes

### Environment & Dependencies
- The project uses multiple AI/ML models requiring significant dependencies (TensorFlow, PyTorch, MediaPipe, DeepFace)
- Large download sizes: expect 1-2GB for full ML dependencies
- Environment setup requires Gemini API key configuration in `.env` file
- Both applications can run independently

### Code Architecture Patterns
- **Streamlit App**: Functional approach with session state management
- **CV System**: Object-oriented with dataclass state containers
- **Error Handling**: Graceful fallbacks for missing dependencies or hardware
- **Performance**: CV system includes threading and buffer management for real-time processing

### Key Integration Points
- Gemini API configuration in `setup_gemini()` function (`app.py:13`)
- File processing pipeline in `process_uploaded_file()` (`app.py:40`)
- CV analysis engine in `AdaptiveLearningCV` class (`adaptive_accessibility.py:47`)
- Analytics export system generates standalone JSON with embedded visualizations