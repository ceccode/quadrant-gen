#!/usr/bin/env python3
"""
Integration Example for Quadrant Generator

This example demonstrates how to integrate the quadrant-gen library
into your Python applications.
"""

# Set matplotlib backend to non-interactive 'Agg' to avoid GUI issues
import matplotlib
matplotlib.use('Agg')

# Add the parent directory to the path so we can import the quadrant_gen package
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from quadrant_gen.chart import csv_to_quadrant_chart, generate_quadrant_chart, sample_points
import base64
import os

def example_with_csv_string():
    """Example using CSV string input"""
    print("\n1. Creating chart from CSV string...")
    
    # Sample CSV data
    csv_data = """
name,description,x,y
Feature A,High impact low effort,0.25,0.75
Feature B,High impact high effort,0.75,0.75
Feature C,Low impact low effort,0.25,0.25
Feature D,Low impact high effort,0.75,0.25
    """.strip()
    
    # Generate chart from CSV string
    base64_image = csv_to_quadrant_chart(
        csv_string=csv_data,
        title="Feature Prioritization",
        x_left="Low Effort", 
        x_right="High Effort",
        y_bottom="Low Impact", 
        y_top="High Impact",
        format="png"
    )
    
    print(f"Base64 image generated (length: {len(base64_image)} characters)")
    
    # Save the base64 image to an HTML file for viewing
    save_to_html(base64_image, "csv_example.html", "Feature Prioritization from CSV", csv_data)
    
    return base64_image

def example_with_data_points():
    """Example using data points directly"""
    print("\n2. Creating chart from data points...")
    
    # Create custom data points
    points = [
        {"label": "Product A\n(High margin)", "x": 0.2, "y": 0.8},
        {"label": "Product B\n(New market)", "x": 0.7, "y": 0.9},
        {"label": "Product C\n(Legacy)", "x": 0.3, "y": 0.3},
        {"label": "Product D\n(Competitor)", "x": 0.8, "y": 0.4},
    ]
    
    # Generate chart from data points
    base64_image = generate_quadrant_chart(
        points=points,
        title="Product Portfolio",
        x_left="Low Investment", 
        x_right="High Investment",
        y_bottom="Low Return", 
        y_top="High Return",
        format="png"
    )
    
    print(f"Base64 image generated (length: {len(base64_image)} characters)")
    
    # Save the base64 image to an HTML file for viewing
    save_to_html(base64_image, "points_example.html", "Product Portfolio from Data Points")
    
    return base64_image

def example_with_sample_data():
    """Example using the built-in sample data"""
    print("\n3. Creating chart from sample data...")
    
    # Get sample data points
    points = sample_points()
    
    # Generate chart from sample data
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
    
    # Save the base64 image to an HTML file for viewing
    save_to_html(base64_image, "sample_example.html", "Sample Data Quadrant Chart")
    
    return base64_image

def save_to_html(base64_image, filename, title, csv_data=None):
    """Save the base64 image to an HTML file for easy viewing"""
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .chart {{ max-width: 800px; margin: 20px 0; }}
            pre {{ background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        
        {"<h2>Input CSV:</h2><pre>" + csv_data + "</pre>" if csv_data else ""}
        
        <h2>Generated Chart:</h2>
        <img class="chart" src="{base64_image}" alt="Quadrant Chart">
        
        <p>Generated using quadrant-gen library</p>
    </body>
    </html>
    """
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save HTML file
    output_path = output_dir / filename
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"Saved HTML file: {output_path.resolve()}")

def main():
    """Run all examples"""
    print("Quadrant Generator Integration Examples")
    print("======================================")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Run examples
    example_with_csv_string()
    example_with_data_points()
    example_with_sample_data()
    
    print("\nAll examples completed. Check the 'output' directory for HTML files.")

if __name__ == "__main__":
    main()
