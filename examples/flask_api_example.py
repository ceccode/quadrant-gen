#!/usr/bin/env python3
"""
Flask API example for quadrant-gen library.

This example demonstrates how to use the quadrant-gen library in a Flask web application
to serve quadrant charts via API endpoints in various formats.
"""

# Set matplotlib backend to non-interactive 'Agg' before importing pyplot
# This is required for running in a web server environment
import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, jsonify, send_file, render_template_string
import io
import base64
import json
from pathlib import Path
import sys

# Add the parent directory to the path so we can import the quadrant_gen package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from quadrant_gen.chart import generate_quadrant_chart, sample_points, csv_to_quadrant_chart

app = Flask(__name__)

# HTML template for the demo page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Quadrant Chart API Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        h2 { color: #444; margin-top: 30px; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow: auto; }
        .endpoint { background: #e9f7fe; padding: 10px; border-left: 4px solid #0099ff; margin-bottom: 20px; }
        img { max-width: 100%; border: 1px solid #ddd; margin: 10px 0; }
        .tabs { display: flex; margin-bottom: 10px; }
        .tab { padding: 10px 20px; cursor: pointer; background: #eee; margin-right: 5px; }
        .tab.active { background: #0099ff; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Quadrant Chart API Demo</h1>
        
        <p>This demo shows how to use the quadrant-gen library in a Flask application.</p>
        
        <div class="tabs">
            <div class="tab active" onclick="showTab('base64')">Base64 Image</div>
            <div class="tab" onclick="showTab('direct')">Direct Image</div>
            <div class="tab" onclick="showTab('pdf')">PDF</div>
            <div class="tab" onclick="showTab('api')">API Docs</div>
        </div>
        
        <div id="base64" class="tab-content active">
            <h2>Base64 Encoded Image</h2>
            <p>This image is loaded via AJAX and embedded as a base64 data URL:</p>
            <img id="chart-base64" src="" alt="Quadrant Chart">
        </div>
        
        <div id="direct" class="tab-content">
            <h2>Direct Image</h2>
            <p>This image is loaded directly from the PNG endpoint:</p>
            <img src="/api/quadrant.png" alt="Quadrant Chart">
        </div>
        
        <div id="pdf" class="tab-content">
            <h2>PDF Version</h2>
            <p>Download the PDF version of the chart:</p>
            <a href="/api/quadrant.pdf" target="_blank" class="button">Download PDF</a>
        </div>
        
        <div id="api" class="tab-content">
            <h2>API Documentation</h2>
            
            <div class="endpoint">
                <h3>GET /api/quadrant</h3>
                <p>Returns a JSON object with a base64-encoded image.</p>
                <h4>Query Parameters:</h4>
                <ul>
                    <li><code>title</code> - Chart title</li>
                    <li><code>x_left</code> - Label for left side of x-axis</li>
                    <li><code>x_right</code> - Label for right side of x-axis</li>
                    <li><code>y_bottom</code> - Label for bottom of y-axis</li>
                    <li><code>y_top</code> - Label for top of y-axis</li>
                </ul>
                <h4>Example Response:</h4>
                <pre>
{
    "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhE...",
    "format": "png"
}
                </pre>
            </div>
            
            <div class="endpoint">
                <h3>POST /api/quadrant</h3>
                <p>Returns a JSON object with a base64-encoded image.</p>
                <h4>Request Body:</h4>
                <pre>
{
    "points": [
        {"label": "Item 1", "x": 0.2, "y": 0.3},
        {"label": "Item 2", "x": 0.7, "y": 0.8}
    ],
    "title": "My Chart",
    "x_left": "Low Cost",
    "x_right": "High Cost",
    "y_bottom": "Low Value",
    "y_top": "High Value"
}
                </pre>
            </div>
            
            <div class="endpoint">
                <h3>GET /api/quadrant.png</h3>
                <p>Returns the chart as a PNG image.</p>
                <p>Accepts the same query parameters as GET /api/quadrant.</p>
            </div>
            
            <div class="endpoint">
                <h3>GET /api/quadrant.pdf</h3>
                <p>Returns the chart as a PDF document.</p>
                <p>Accepts the same query parameters as GET /api/quadrant.</p>
            </div>
        </div>
    </div>
    
    <script>
        // Load base64 image
        fetch('/api/quadrant?title=Sample%20Quadrant&x_left=Low%20Cost&x_right=High%20Cost&y_bottom=Low%20Value&y_top=High%20Value')
            .then(response => response.json())
            .then(data => {
                document.getElementById('chart-base64').src = data.image_data;
            });
            
        // Tab functionality
        function showTab(tabId) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabId).classList.add('active');
            document.querySelector(`.tab[onclick="showTab('${tabId}')"]`).classList.add('active');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Render the demo page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/quadrant', methods=['GET', 'POST'])
def get_quadrant_json():
    """
    Return a JSON object with a base64-encoded image.
    
    GET: Use query parameters
    POST: Use JSON request body
    """
    if request.method == 'POST':
        # Get data from request body
        data = request.json or {}
        points = data.get('points', sample_points())
        title = data.get('title', '')
        x_left = data.get('x_left', '')
        x_right = data.get('x_right', '')
        y_bottom = data.get('y_bottom', '')
        y_top = data.get('y_top', '')
    else:
        # Use query parameters for GET
        points = sample_points()  # Always use sample points for GET
        title = request.args.get('title', '')
        x_left = request.args.get('x_left', '')
        x_right = request.args.get('x_right', '')
        y_bottom = request.args.get('y_bottom', '')
        y_top = request.args.get('y_top', '')
    
    # Generate the chart directly to base64
    base64_image = generate_quadrant_chart(
        points=points,
        title=title,
        x_left=x_left,
        x_right=x_right,
        y_bottom=y_bottom,
        y_top=y_top,
        format="png"
    )
    
    # Extract the actual base64 data (remove the data:image/png;base64, prefix)
    data = base64_image.split(',')[1] if ',' in base64_image else base64_image
    
    return jsonify({
        'image_data': f'data:image/png;base64,{data}',
        'format': 'png'
    })

@app.route('/api/quadrant.png')
def get_quadrant_png():
    """Return the chart as a PNG image."""
    # Get parameters from query string
    points = sample_points()  # Always use sample points for GET
    title = request.args.get('title', '')
    x_left = request.args.get('x_left', '')
    x_right = request.args.get('x_right', '')
    y_bottom = request.args.get('y_bottom', '')
    y_top = request.args.get('y_top', '')
    
    # Generate the chart directly to base64
    base64_image = generate_quadrant_chart(
        points=points,
        title=title,
        x_left=x_left,
        x_right=x_right,
        y_bottom=y_bottom,
        y_top=y_top,
        format="png"
    )
    
    # Extract the actual base64 data and convert back to bytes
    img_data = base64.b64decode(base64_image.split(',')[1] if ',' in base64_image else base64_image)
    buffer = io.BytesIO(img_data)
    buffer.seek(0)
    
    return send_file(buffer, mimetype='image/png')

@app.route('/api/quadrant.pdf')
def get_quadrant_pdf():
    """Return the chart as a PDF document."""
    # Get parameters from query string
    points = sample_points()  # Always use sample points for GET
    title = request.args.get('title', '')
    x_left = request.args.get('x_left', '')
    x_right = request.args.get('x_right', '')
    y_bottom = request.args.get('y_bottom', '')
    y_top = request.args.get('y_top', '')
    
    # Generate the chart directly to base64
    base64_image = generate_quadrant_chart(
        points=points,
        title=title,
        x_left=x_left,
        x_right=x_right,
        y_bottom=y_bottom,
        y_top=y_top,
        format="pdf"
    )
    
    # Extract the actual base64 data and convert back to bytes
    pdf_data = base64.b64decode(base64_image.split(',')[1] if ',' in base64_image else base64_image)
    buffer = io.BytesIO(pdf_data)
    buffer.seek(0)
    
    return send_file(buffer, mimetype='application/pdf')

if __name__ == '__main__':
    print("Starting Flask API example for quadrant-gen")
    print("Visit http://127.0.0.1:5000/ to see the demo")
    app.run(debug=True)
