# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains two main components:
1. **Adaptive Accessibility Tracker** - AI-powered system for real-time emotion, stress, ADHD, and accessibility detection with analytics
2. **Greek Goddess Learning Platform** - Flask-based web application with an immersive Greek mythology theme

## Architecture

### Main Components

- `adaptive_accessibility.py` - Core computer vision and AI analytics engine (66KB+ comprehensive system)
- `Greek/` - Complete Flask web application with mythological theme
  - `app.py` - Main Flask application with file upload, chat, and content generation APIs
  - `templates/` - HTML templates for dashboard, upload, chat, and studio pages
  - `static/` - CSS and JavaScript for Greek goddess theme with Lottie animations
  - `uploads/` - User uploaded files storage

### Key Technologies
- **Computer Vision**: OpenCV, MediaPipe, DeepFace for emotion and accessibility detection
- **AI/ML**: TensorFlow, scikit-learn for analytics and pattern recognition
- **Visualization**: Plotly, Matplotlib for interactive charts and analytics dashboards
- **Web Framework**: Flask with file upload, chat APIs, and content generation
- **Frontend**: Responsive Greek-themed UI with Lottie animations and particle effects

## Development Commands

### Setup and Installation
```bash
# Install all dependencies
pip install -r requirements.txt

# Set up environment variables (copy and modify)
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

### Running Applications

#### Greek Goddess Learning Platform
```bash
cd Greek
python app.py
```
Accessible at:
- All-in-One Dashboard: http://localhost:5000 (includes upload, chat, and studio functionality)

#### Adaptive Accessibility Tracker
```bash
# Run the main computer vision demo
python adaptive_accessibility.py
```
Demo options:
1. Camera Tracking - Live webcam analysis
2. Flask Integration Demo - Generate sample data and test web integration
3. Sample Data Generation - Create analytics data for testing

### Testing
No formal test framework is configured. Test manually using the demo modes in `adaptive_accessibility.py`.

## Key Classes and APIs

### AdaptiveLearningCV
Main computer vision engine with comprehensive emotion, stress, and accessibility tracking.

**Important Methods:**
- `process_frame(frame)` - Analyze single video frame for emotions and patterns
- `generate_analytics_report()` - Create comprehensive analytics with visualizations
- `get_flask_interface_data()` - Format data for web integration

### FlaskAccessibilityAPI
Web integration helper for the accessibility tracker.

**Key Methods:**
- `start_tracking()` / `stop_tracking()` - Control camera tracking
- `get_analytics_dashboard_data()` - Dashboard data with metrics
- `get_tiny_graphs_json()` - Plotly visualizations for web display
- `simulate_demo_data()` - Generate test data for development

### Greek Flask Application
File upload, chat, and content generation APIs with in-memory storage and Gemini AI integration.

**API Endpoints:**
- `POST /api/upload` - Upload files (PDF, TXT, audio, images, PowerPoint) with automatic text extraction and summarization
- `POST /api/chat` - Chat interface with Athena persona using **Gemini 2.5 Pro** with document context
- `GET /api/files` - Retrieve uploaded files
- `GET /api/chat-history` - Retrieve chat history including document summaries
- `POST /api/generate-content` - Generate audio/video content (placeholder)

**Document Processing:**
- PDF text extraction using PyPDF2
- Automatic document summarization using **Gemini 2.5 Pro** with structured, detailed summaries
- Document-aware chat responses with selected source context using **Gemini 2.5 Pro**
- Real-time dashboard updates when documents are uploaded
- Follow-up questions and deep analysis of uploaded content

## Data Storage

### Current Implementation
- **Greek App**: In-memory storage (`uploaded_files[]`, `chat_history[]`)
- **Accessibility Tracker**: Rolling buffer of 1000 data points, session-based analytics

### Production Considerations
Replace in-memory storage with proper database models for file metadata and chat history.

## File Upload Configuration
- **Allowed Extensions**: txt, pdf, png, jpg, jpeg, gif, mp3, wav, md, pptx
- **Max File Size**: 16MB
- **Upload Directory**: `Greek/uploads/`

## Environment Variables
- `GEMINI_API_KEY` - Required for Gemini AI integration (currently placeholder in chat)

## Performance Notes
- Accessibility tracker processes every 3rd frame for optimal performance
- Background camera tracking runs in separate thread
- Automatic cleanup of old data and memory management
- Greek app uses secure filename handling with timestamp prefixes

## Integration Points
The accessibility tracker includes `FlaskAccessibilityAPI` specifically designed to integrate with Flask applications like the Greek platform, enabling real-time emotion and accessibility monitoring in educational contexts.