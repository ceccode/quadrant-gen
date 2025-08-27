#!/usr/bin/env python3
"""
Quadrant Chart Example App

This example demonstrates how to use the quadrant-gen library to create
quadrant charts from CSV data and get base64 encoded output.
"""

# Set matplotlib backend to non-interactive 'Agg' to avoid GUI issues
import matplotlib
matplotlib.use('Agg')

from quadrant_gen.chart import csv_to_quadrant_chart, generate_quadrant_chart, sample_points
import webbrowser
import tempfile
import os

# Example CSV data
SAMPLE_CSV = """
name,description,x,y
Product A,High quality,0.18,0.75
Product B,Low cost,0.35,0.25
Product C,Innovative,0.80,0.68
Product D,Traditional,0.65,0.40
""".strip()

def example_from_csv_string():
    """Example using CSV string input"""
    print("\n1. Creating chart from CSV string...")
    
    # Generate chart from CSV string
    base64_image = csv_to_quadrant_chart(
        csv_string=SAMPLE_CSV,
        title="Product Positioning",
        x_left="Low Cost", 
        x_right="High Cost",
        y_bottom="Low Value", 
        y_top="High Value",
        format="png"
    )
    
    print(f"Base64 image generated (length: {len(base64_image)} characters)")
    print(f"Data URL starts with: {base64_image[:60]}...")
    
    # Create a simple HTML file to display the image
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quadrant Chart from CSV</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .chart {{ max-width: 800px; margin: 20px 0; }}
            pre {{ background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>Quadrant Chart from CSV</h1>
        
        <h2>Input CSV:</h2>
        <pre>{SAMPLE_CSV}</pre>
        
        <h2>Generated Chart:</h2>
        <img class="chart" src="{base64_image}" alt="Quadrant Chart">
        
        <p>The chart was generated using the quadrant-gen library.</p>
    </body>
    </html>
    """
    
    # Save HTML to a temporary file and open in browser
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html)
        temp_path = f.name
    
    print(f"\nOpening chart in your default web browser...")
    webbrowser.open('file://' + os.path.realpath(temp_path))
    return temp_path

def example_from_sample_data():
    """Example using sample data points"""
    print("\n2. Creating chart from sample data points...")
    
    # Get sample data points
    points = sample_points()
    
    # Generate chart from data points
    base64_image = generate_quadrant_chart(
        points=points,
        title="Sample Quadrant Chart",
        x_left="Low Priority", 
        x_right="High Priority",
        y_bottom="Low Impact", 
        y_top="High Impact",
        format="png"
    )
    
    print(f"Base64 image generated (length: {len(base64_image)} characters)")
    print(f"Data URL starts with: {base64_image[:60]}...")
    
    # Create a simple HTML file to display the image
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quadrant Chart from Sample Data</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .chart {{ max-width: 800px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>Quadrant Chart from Sample Data</h1>
        <img class="chart" src="{base64_image}" alt="Quadrant Chart">
        <p>The chart was generated using the quadrant-gen library with sample data points.</p>
    </body>
    </html>
    """
    
    # Save HTML to a temporary file and open in browser
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html)
        temp_path = f.name
    
    print(f"\nOpening chart in your default web browser...")
    webbrowser.open('file://' + os.path.realpath(temp_path))
    return temp_path

def main():
    print("Quadrant Chart Generator Example")
    print("===============================\n")
    print("This example demonstrates how to use the quadrant-gen library")
    print("to create quadrant charts from CSV data and get base64 encoded output.")
    
    # Run examples
    csv_example_path = example_from_csv_string()
    sample_example_path = example_from_sample_data()
    
    print("\nExample files created:")
    print(f"1. CSV Example: {csv_example_path}")
    print(f"2. Sample Data Example: {sample_example_path}")
    print("\nCheck your web browser for the generated charts!")

if __name__ == "__main__":
    main()