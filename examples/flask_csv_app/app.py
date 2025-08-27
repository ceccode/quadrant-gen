#!/usr/bin/env python3
"""
Simple Flask App for Quadrant Chart Generation

This app accepts CSV input and generates quadrant charts in PNG or PDF format.
"""

# Set matplotlib backend to non-interactive 'Agg' before importing pyplot
import matplotlib
matplotlib.use('Agg')

import sys
from pathlib import Path
import os

# Add the parent directory to the path so we can import the quadrant_gen package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import io
import base64
from quadrant_gen.chart import csv_to_quadrant_chart

app = Flask(__name__)
app.secret_key = 'quadrant-gen-secret-key'  # Required for flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page with form for CSV input and chart generation"""
    chart_image = None
    csv_data = request.form.get('csv_data', '')
    
    if request.method == 'POST':
        # Get form data
        csv_data = request.form.get('csv_data', '')
        title = request.form.get('title', 'Quadrant Chart')
        x_left = request.form.get('x_left', 'Low X')
        x_right = request.form.get('x_right', 'High X')
        y_bottom = request.form.get('y_bottom', 'Low Y')
        y_top = request.form.get('y_top', 'High Y')
        output_format = request.form.get('format', 'png')
        
        if not csv_data:
            flash('Please enter CSV data', 'error')
        else:
            try:
                # Generate chart from CSV
                chart_image = csv_to_quadrant_chart(
                    csv_string=csv_data,
                    title=title,
                    x_left=x_left,
                    x_right=x_right,
                    y_bottom=y_bottom,
                    y_top=y_top,
                    format=output_format
                )
                
                # If download is requested, return the file
                if request.form.get('download'):
                    # Extract the base64 data and convert to bytes
                    img_data = base64.b64decode(chart_image.split(',')[1] if ',' in chart_image else chart_image)
                    buffer = io.BytesIO(img_data)
                    buffer.seek(0)
                    
                    # Return as downloadable file
                    mimetype = 'application/pdf' if output_format == 'pdf' else 'image/png'
                    return send_file(
                        buffer,
                        mimetype=mimetype,
                        as_attachment=True,
                        download_name=f'quadrant_chart.{output_format}'
                    )
            except Exception as e:
                flash(f'Error generating chart: {str(e)}', 'error')
    
    # Sample CSV data for the placeholder
    sample_csv = """name,description,x,y
Product A,High quality,0.2,0.8
Product B,Low cost,0.7,0.3
Product C,Innovative,0.8,0.7
Product D,Traditional,0.3,0.2"""
    
    return render_template(
        'index.html',
        chart_image=chart_image,
        csv_data=csv_data or sample_csv
    )

if __name__ == '__main__':
    print("Starting Quadrant Chart Generator App")
    print("Visit http://127.0.0.1:5001/ to use the app")
    app.run(debug=True, port=5001)
