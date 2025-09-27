# api/index.py - Simplified GERD Monitoring System for Vercel

import os
import sys
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configure Flask for Vercel
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Simple data classes for basic functionality
class WaterLevelMonitor:
    def __init__(self):
        self.current_level = 632.4
        self.normal_range = (620.0, 640.0)
        
    def generate_sample_data(self, days=30):
        """Generate sample water level data"""
        data = []
        base_date = datetime.now() - timedelta(days=days)
        for i in range(days):
            date = base_date + timedelta(days=i)
            level = 630 + random.uniform(-5, 8)
            data.append({
                'date': date.isoformat(),
                'water_level': round(level, 2),
                'precipitation': round(random.uniform(0, 50), 1),
                'temperature': round(random.uniform(20, 35), 1)
            })
        return data

class RealTimeMonitor:
    def __init__(self):
        self.gerd_location = {'lat': 11.215, 'lon': 35.092}
        
    def get_sample_weather_data(self, location_name="GERD Dam"):
        """Generate sample weather data"""
        return {
            'location': location_name,
            'temperature': round(random.uniform(25, 35), 1),
            'humidity': random.randint(40, 80),
            'precipitation': round(random.uniform(0, 20), 1),
            'wind_speed': round(random.uniform(2, 15), 1),
            'description': 'Partly Cloudy',
            'timestamp': datetime.now().isoformat()
        }
    
    def create_simple_chart(self, data):
        """Create simple Plotly chart"""
        dates = [d['date'] for d in data]
        levels = [d['water_level'] for d in data]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=levels,
            mode='lines+markers',
            name='Water Level',
            line=dict(color='#06b6d4', width=3)
        ))
        
        fig.update_layout(
            title='GERD Water Level Monitoring',
            xaxis_title='Date',
            yaxis_title='Water Level (m)',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#ffffff'}
        )
        
        return json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))

# Initialize monitors
water_monitor = WaterLevelMonitor()
realtime_monitor = RealTimeMonitor()

# Routes to serve HTML files
@app.route('/')
def index():
    """Serve the main index page"""
    try:
        return send_from_directory('public', 'gerd_solutions_center.html')
    except Exception:
        return jsonify({
            'message': 'GERD Complete Advanced Monitoring System - DEPLOYED ON VERCEL',
            'version': '6.0.0',
            'status': 'operational',
            'note': 'Simplified version for Vercel deployment'
        })

@app.route('/realtime')
def realtime():
    """Serve the real-time monitoring page"""
    try:
        return send_from_directory('public', 'realtime_monitoring.html')
    except Exception:
        return jsonify({'error': 'Real-time monitoring page not found'}), 404

@app.route('/sidebar')
def sidebar():
    """Serve the sidebar interface page"""
    try:
        return send_from_directory('public', 'gerd_with_botpress_sidebar.html')
    except Exception:
        return jsonify({'error': 'Sidebar interface page not found'}), 404

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from public directory"""
    return send_from_directory('public', filename)

# API Routes (Simplified versions)
@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': 'simplified-6.0.0',
        'systems': {
            'water_monitoring': 'operational',
            'weather_integration': 'operational',
            'api_endpoints': 'operational'
        }
    })

@app.route('/api/dashboard')
def get_dashboard():
    """Get dashboard data"""
    try:
        sample_data = water_monitor.generate_sample_data(30)
        weather_data = realtime_monitor.get_sample_weather_data()
        chart_data = realtime_monitor.create_simple_chart(sample_data)
        
        return jsonify({
            'success': True,
            'water_data': sample_data[-7:],  # Last 7 days
            'weather': weather_data,
            'chart': chart_data,
            'current_level': water_monitor.current_level,
            'status': 'operational'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/weather')
def get_weather():
    """Get weather data"""
    try:
        weather_data = realtime_monitor.get_sample_weather_data()
        return jsonify({
            'success': True,
            'data': weather_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/water-level')
def get_water_level():
    """Get current water level"""
    try:
        return jsonify({
            'success': True,
            'current_level': water_monitor.current_level,
            'normal_range': water_monitor.normal_range,
            'status': 'normal' if water_monitor.normal_range[0] <= water_monitor.current_level <= water_monitor.normal_range[1] else 'alert',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/early_warning_dashboard')
def early_warning_dashboard():
    """Simplified early warning dashboard"""
    try:
        sample_data = water_monitor.generate_sample_data(90)
        current_level = water_monitor.current_level
        
        # Simple risk assessment
        if current_level > 645:
            risk_level = 'HIGH'
        elif current_level < 615:
            risk_level = 'HIGH'
        elif current_level > 640 or current_level < 620:
            risk_level = 'MODERATE'
        else:
            risk_level = 'LOW'
        
        return jsonify({
            'success': True,
            'current_assessment': {
                'current_water_level': current_level,
                'risk_level': risk_level,
                'status': 'MONITORING',
                'timestamp': datetime.now().isoformat()
            },
            'historical_data': sample_data,
            'system_status': 'operational'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# For local testing
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
