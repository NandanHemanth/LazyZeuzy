"""
Flask Application Example for Adaptive Accessibility Tracker
This example demonstrates how to integrate the accessibility tracker into a web application.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from adaptive_accessibility import FlaskAccessibilityAPI
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global accessibility tracker instance
accessibility_tracker = FlaskAccessibilityAPI()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/start-tracking', methods=['POST'])
def start_tracking():
    """Start accessibility tracking"""
    try:
        camera_index = request.json.get('camera_index', 0)
        result = accessibility_tracker.start_tracking(camera_index)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stop-tracking', methods=['POST'])
def stop_tracking():
    """Stop accessibility tracking"""
    try:
        result = accessibility_tracker.stop_tracking()
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/current-data')
def get_current_data():
    """Get current accessibility data"""
    try:
        data = accessibility_tracker.get_real_time_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/dashboard-data')
def get_dashboard_data():
    """Get complete dashboard data"""
    try:
        data = accessibility_tracker.get_analytics_dashboard_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/tiny-graphs')
def get_tiny_graphs():
    """Get tiny graphs for visualization"""
    try:
        time_window = request.args.get('hours', 1, type=int)
        data = accessibility_tracker.get_tiny_graphs_json(time_window_hours=time_window)
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/recommendations')
def get_recommendations():
    """Get accessibility recommendations"""
    try:
        data = accessibility_tracker.get_accessibility_recommendations()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/insights')
def get_insights():
    """Get learning insights"""
    try:
        data = accessibility_tracker.get_learning_insights()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/export-session')
def export_session():
    """Export session data"""
    try:
        data = accessibility_tracker.export_session_analytics()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/demo-data', methods=['POST'])
def generate_demo_data():
    """Generate demo data for testing"""
    try:
        duration = request.json.get('duration_minutes', 5)
        result = accessibility_tracker.simulate_demo_data(duration_minutes=duration)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# HTML Template for dashboard (basic example)
dashboard_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Adaptive Accessibility Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .metric-card { background: #f5f5f5; padding: 20px; border-radius: 8px; text-align: center; }
        .metric-value { font-size: 2em; font-weight: bold; margin: 10px 0; }
        .charts { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .controls { margin-bottom: 20px; }
        button { padding: 10px 20px; margin: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .recommendations { background: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #ffc107; }
        .alert { background: #f8d7da; color: #721c24; padding: 15px; margin: 10px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Adaptive Accessibility Dashboard</h1>

        <div class="controls">
            <button onclick="startTracking()">Start Tracking</button>
            <button onclick="stopTracking()">Stop Tracking</button>
            <button onclick="generateDemoData()">Generate Demo Data</button>
            <button onclick="refreshData()">Refresh Data</button>
        </div>

        <div class="metrics" id="metrics">
            <!-- Metrics will be populated here -->
        </div>

        <div id="recommendations">
            <!-- Recommendations will be populated here -->
        </div>

        <div class="charts">
            <div class="chart-container">
                <div id="emotions_pie"></div>
            </div>
            <div class="chart-container">
                <div id="metrics_timeline"></div>
            </div>
            <div class="chart-container">
                <div id="adhd_gauge"></div>
            </div>
            <div class="chart-container">
                <div id="accessibility_heatmap"></div>
            </div>
            <div class="chart-container">
                <div id="performance_radar"></div>
            </div>
        </div>
    </div>

    <script>
        let updateInterval;

        function startTracking() {
            fetch('/api/start-tracking', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({camera_index: 0})
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.status === 'success') {
                    startAutoRefresh();
                }
            });
        }

        function stopTracking() {
            fetch('/api/stop-tracking', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                stopAutoRefresh();
            });
        }

        function generateDemoData() {
            fetch('/api/demo-data', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({duration_minutes: 3})
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                refreshData();
            });
        }

        function refreshData() {
            // Get dashboard data
            fetch('/api/dashboard-data')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateMetrics(data.data.current_state);
                    updateRecommendations(data.data.recommendations, data.data.critical_alerts);
                }
            });

            // Get visualizations
            fetch('/api/tiny-graphs')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateCharts(data.visualizations);
                }
            });
        }

        function updateMetrics(state) {
            const metricsHtml = `
                <div class="metric-card">
                    <h3>Current Emotion</h3>
                    <div class="metric-value">${state.emotion}</div>
                </div>
                <div class="metric-card">
                    <h3>Stress Level</h3>
                    <div class="metric-value">${state.stress_level.toFixed(1)}%</div>
                </div>
                <div class="metric-card">
                    <h3>Attention Score</h3>
                    <div class="metric-value">${state.attention_score.toFixed(1)}%</div>
                </div>
                <div class="metric-card">
                    <h3>ADHD Risk</h3>
                    <div class="metric-value">${state.adhd_risk.toFixed(1)}</div>
                </div>
                <div class="metric-card">
                    <h3>Engagement</h3>
                    <div class="metric-value">${state.engagement_level.toFixed(1)}%</div>
                </div>
                <div class="metric-card">
                    <h3>Visual Strain</h3>
                    <div class="metric-value">${state.visual_strain.toFixed(1)}%</div>
                </div>
            `;
            document.getElementById('metrics').innerHTML = metricsHtml;
        }

        function updateRecommendations(recommendations, alerts) {
            let html = '<h3>Current Recommendations</h3>';

            if (alerts && alerts.length > 0) {
                alerts.forEach(alert => {
                    html += `<div class="alert">${alert.message}</div>`;
                });
            }

            if (recommendations && recommendations.length > 0) {
                html += '<div class="recommendations"><ul>';
                recommendations.forEach(rec => {
                    html += `<li>${rec}</li>`;
                });
                html += '</ul></div>';
            } else {
                html += '<div class="recommendations">No specific recommendations at this time.</div>';
            }

            document.getElementById('recommendations').innerHTML = html;
        }

        function updateCharts(visualizations) {
            Object.keys(visualizations).forEach(chartName => {
                const element = document.getElementById(chartName);
                if (element) {
                    const plotData = JSON.parse(visualizations[chartName]);
                    Plotly.newPlot(element, plotData.data, plotData.layout, {responsive: true});
                }
            });
        }

        function startAutoRefresh() {
            updateInterval = setInterval(refreshData, 5000); // Refresh every 5 seconds
        }

        function stopAutoRefresh() {
            if (updateInterval) {
                clearInterval(updateInterval);
            }
        }

        // Initialize dashboard
        refreshData();
    </script>
</body>
</html>
"""

# Create templates directory and save template
import os
if not os.path.exists('templates'):
    os.makedirs('templates')

with open('templates/dashboard.html', 'w') as f:
    f.write(dashboard_template)

if __name__ == '__main__':
    print("Starting Flask Adaptive Accessibility Dashboard...")
    print("Dashboard available at: http://localhost:5000")
    print("API endpoints:")
    print("  POST /api/start-tracking - Start camera tracking")
    print("  POST /api/stop-tracking - Stop tracking")
    print("  GET  /api/current-data - Get real-time data")
    print("  GET  /api/dashboard-data - Get dashboard data")
    print("  GET  /api/tiny-graphs - Get visualizations")
    print("  GET  /api/recommendations - Get recommendations")
    print("  GET  /api/insights - Get AI insights")
    print("  POST /api/demo-data - Generate demo data")

    app.run(debug=True, port=5000)