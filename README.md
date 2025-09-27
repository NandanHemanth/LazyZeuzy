# Adaptive Accessibility Tracker

A revolutionary AI-powered system for real-time emotion, stress, ADHD, and accessibility detection with analytics and visualization capabilities, ready for Flask integration.

## Features

### Core Detection Capabilities
- **Emotion Recognition**: Real-time facial emotion detection using DeepFace
- **Stress Level Monitoring**: Multi-factor stress assessment
- **ADHD Pattern Detection**: Movement and attention pattern analysis
- **Accessibility Assessment**: Visual, motor, and cognitive accessibility needs detection
- **Attention & Engagement Tracking**: Focus stability and engagement level monitoring

### Analytics & Visualization
- **Real-time Analytics**: Live data processing and storage
- **Tiny Graphs**: Flask-ready Plotly visualizations
- **Performance Metrics**: Comprehensive KPI tracking
- **AI-Powered Insights**: Automated pattern recognition and recommendations
- **Critical Alerts**: Immediate notifications for concerning patterns

### Flask Integration
- **REST API**: Complete API endpoints for web integration
- **Dashboard**: Ready-to-use web dashboard
- **Real-time Updates**: Live data streaming capabilities
- **Export Functionality**: Session data export for analysis

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

### Core Dependencies
- OpenCV (camera and computer vision)
- MediaPipe (face and hand tracking)
- DeepFace (emotion recognition)
- Plotly (interactive visualizations)
- Pandas (data analysis)
- NumPy (numerical computing)
- Flask (web framework)

## Quick Start

### 1. Basic Usage
```python
from adaptive_accessibility import AdaptiveLearningCV

# Initialize the tracker
tracker = AdaptiveLearningCV()

# Process a frame (from camera or video)
result = tracker.process_frame(frame)

# Get analytics report
report = tracker.generate_analytics_report()
```

### 2. Flask Integration
```python
from adaptive_accessibility import FlaskAccessibilityAPI

# Initialize Flask API
flask_api = FlaskAccessibilityAPI()

# Start tracking
result = flask_api.start_tracking()

# Get dashboard data
dashboard_data = flask_api.get_analytics_dashboard_data()

# Get tiny graphs for web display
graphs = flask_api.get_tiny_graphs_json()
```

### 3. Demo Modes
Run the built-in demo:
```bash
python adaptive_accessibility.py
```

Choose from:
1. **Camera Tracking**: Live webcam analysis
2. **Flask Integration Demo**: Generate sample data and test web integration
3. **Sample Data Generation**: Create analytics data for testing

### 4. Web Dashboard
```bash
python flask_example.py
```
Then open http://localhost:5000 for the interactive dashboard.

## API Endpoints

### Core Tracking
- `POST /api/start-tracking` - Start camera tracking
- `POST /api/stop-tracking` - Stop tracking
- `GET /api/current-data` - Get real-time data

### Analytics
- `GET /api/dashboard-data` - Complete dashboard data
- `GET /api/tiny-graphs` - Plotly visualizations
- `GET /api/recommendations` - Accessibility recommendations
- `GET /api/insights` - AI-powered insights

### Utilities
- `POST /api/demo-data` - Generate demo data
- `GET /api/export-session` - Export session analytics

## Key Classes

### AdaptiveLearningCV
Main computer vision and analytics engine.

**Key Methods:**
- `process_frame(frame)` - Analyze single video frame
- `generate_analytics_report()` - Create comprehensive analytics
- `get_flask_interface_data()` - Format data for web display

### FlaskAccessibilityAPI
Web integration helper class.

**Key Methods:**
- `start_tracking()` / `stop_tracking()` - Control tracking
- `get_analytics_dashboard_data()` - Dashboard data
- `get_tiny_graphs_json()` - Web-ready visualizations
- `simulate_demo_data()` - Generate test data

### Data Classes
- `LearningState` - Current user state
- `AccessibilityAssessment` - Accessibility needs analysis

## Visualization Types

### 1. Emotion Distribution (Pie Chart)
Shows breakdown of detected emotions over time.

### 2. Real-time Metrics Timeline
Multi-line chart tracking stress, attention, and engagement.

### 3. ADHD Risk Gauge
Gauge chart showing current ADHD risk assessment.

### 4. Accessibility Strain Heatmap
Heat map of visual strain, cognitive load, and stress levels.

### 5. Performance Radar Chart
Radar chart showing attention, engagement, motor precision, and focus stability.

## Analytics Features

### Summary Statistics
- Average stress levels and trends
- Dominant emotions and emotional diversity
- ADHD risk categorization
- Attention stability metrics
- Visual strain indicators
- Cognitive load assessments

### AI Insights
- Automatic pattern detection
- Trend analysis
- Risk assessment
- Performance optimization suggestions

### Recommendations Engine
- Stress management techniques
- ADHD support strategies
- Attention improvement methods
- Visual comfort adjustments
- Accessibility adaptations

## Use Cases

### Educational Technology
- Adaptive learning platforms
- Student engagement monitoring
- Accessibility compliance
- Personalized content delivery

### Healthcare & Therapy
- ADHD assessment tools
- Stress monitoring systems
- Accessibility evaluation
- Patient engagement tracking

### Workplace Wellness
- Employee well-being monitoring
- Ergonomic assessments
- Productivity optimization
- Stress intervention systems

### Research & Development
- Human-computer interaction studies
- Accessibility research
- Educational effectiveness analysis
- Behavioral pattern studies

## Configuration Options

### Camera Settings
```python
# Specify camera index
flask_api.start_tracking(camera_index=0)
```

### Analytics Time Windows
```python
# Generate report for specific time period
report = tracker.generate_analytics_report(time_window_hours=24)

# Get graphs for specific timeframe
graphs = flask_api.get_tiny_graphs_json(time_window_hours=2)
```

### Demo Data Generation
```python
# Generate sample data for testing
result = flask_api.simulate_demo_data(duration_minutes=5)
```

## Data Export

### Session Data Export
```python
session_data = tracker.export_session_data()
# Contains: emotions, attention, movements, analytics, alerts
```

### Analytics Report Export
```python
analytics_report = flask_api.export_session_analytics()
# Contains: complete analytics, visualizations, insights, recommendations
```

## Performance Considerations

- **Frame Processing**: System processes every 3rd frame for optimal performance
- **Data Storage**: Maintains rolling buffer of 1000 recent data points
- **Background Processing**: Camera tracking runs in separate thread
- **Memory Management**: Automatic cleanup of old data and alerts

## Troubleshooting

### Common Issues

1. **Camera Access**: Ensure camera permissions are granted
2. **Dependencies**: Install all required packages from requirements.txt
3. **Performance**: Reduce frame processing frequency if needed
4. **Unicode Issues**: System automatically handles emoji display issues

### Error Handling
- All API endpoints include comprehensive error handling
- Graceful degradation when camera is unavailable
- Fallback mechanisms for failed emotion detection

## Example Flask Integration

```python
from flask import Flask, jsonify
from adaptive_accessibility import FlaskAccessibilityAPI

app = Flask(__name__)
tracker = FlaskAccessibilityAPI()

@app.route('/api/status')
def get_status():
    data = tracker.get_real_time_data()
    return jsonify(data)

@app.route('/api/visualizations')
def get_visualizations():
    graphs = tracker.get_tiny_graphs_json()
    return jsonify(graphs)

if __name__ == '__main__':
    app.run(debug=True)
```

This system represents a breakthrough in adaptive accessibility technology, providing real-time insights that can transform how we approach inclusive education and human-computer interaction.

## Gemini Playground

This is a Streamlit application that uses the Gemini API to perform various tasks on a document or a website.

### Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up your API key:**
    - Create a file named `.env` in the root of the project.
    - Add your Gemini API key to the `.env` file like this:
      ```
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```

### Running the App

```bash
streamlit run streamlit_app.py
```

This will open the Gemini Playground in your web browser.