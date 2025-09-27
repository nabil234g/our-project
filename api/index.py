# api/index.py - Vercel Serverless Entry Point for GERD Monitoring System

import os
import sys
import warnings
from pathlib import Path

# Add the root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Suppress warnings for cleaner deployment
warnings.filterwarnings('ignore')

# Import the Flask app from the main file
try:
    from complete_gerd_system import app
except ImportError:
    # If direct import fails, try importing components
    import cv2
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.dates as mdates
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import seaborn as sns
    import io
    import base64
    from flask import Flask, request, jsonify, render_template_string, send_from_directory
    from flask_cors import CORS
    import json
    from datetime import datetime, timedelta
    import random
    import warnings
    from typing import Dict, List, Optional, Tuple
    import logging
    import asyncio
    import aiohttp
    from concurrent.futures import ThreadPoolExecutor
    import time
    import requests

    # Machine Learning imports
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, IsolationForest
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.cluster import KMeans, DBSCAN
    from skimage import filters, segmentation, measure
    from scipy import ndimage, signal
    from scipy.stats import pearsonr

    # Plotly imports for real-time dashboard
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    from plotly.utils import PlotlyJSONEncoder

    # Create Flask app if import failed
    app = Flask(__name__)
    CORS(app)
    
    # Import all the classes and functionality from the original file
    exec(open(str(root_dir / 'complete_gerd_system.py')).read())

# Configure Flask for Vercel
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Add route to serve static files from public directory
@app.route('/')
def index():
    """Serve the main index page"""
    try:
        with open(os.path.join(root_dir, 'public', 'gerd_solutions_center.html'), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to API info if HTML not found
        return jsonify({
            'message': 'GERD Complete Advanced Monitoring System - DEPLOYED ON VERCEL',
            'version': '6.0.0',
            'status': 'operational',
            'endpoints': {
                '/': 'Main dashboard',
                '/realtime': 'Real-time monitoring',
                '/sidebar': 'Sidebar interface',
                '/api/dashboard': 'Real-time API dashboard',
                '/api/weather': 'Weather data',
                '/health': 'System health check'
            }
        })

@app.route('/realtime')
def realtime():
    """Serve the real-time monitoring page"""
    try:
        with open(os.path.join(root_dir, 'public', 'realtime_monitoring.html'), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({'error': 'Real-time monitoring page not found'}), 404

@app.route('/sidebar')
def sidebar():
    """Serve the sidebar interface page"""
    try:
        with open(os.path.join(root_dir, 'public', 'gerd_with_botpress_sidebar.html'), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({'error': 'Sidebar interface page not found'}), 404

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from public directory"""
    try:
        return send_from_directory(os.path.join(root_dir, 'public'), filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

# Vercel serverless handler
def handler(request):
    """Vercel serverless handler function"""
    return app(request.environ, request.start_response)

# For local testing
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)