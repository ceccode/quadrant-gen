# Quadrant Chart Generator - Flask CSV App

A simple Flask web application that allows you to generate quadrant charts from CSV data.

## Features

- Upload CSV data directly in the browser
- Customize chart title and axis labels
- Generate charts in PNG or PDF format
- View charts in the browser or download them

## Installation

1. Make sure you have the quadrant-gen library installed:
   ```bash
   pip install -e /path/to/quadrant-gen
   ```

2. Install Flask if you don't have it:
   ```bash
   pip install flask
   ```

## Running the App

From the `flask_csv_app` directory:

```bash
python app.py
```

Then open your browser to http://127.0.0.1:5000/

## CSV Format

Your CSV data should have the following columns:
- `name`: Name of the data point
- `description`: Description of the data point (optional)
- `x`: X-coordinate (0.0 to 1.0)
- `y`: Y-coordinate (0.0 to 1.0)

Example:
```csv
name,description,x,y
Product A,High quality,0.2,0.8
Product B,Low cost,0.7,0.3
```

## Usage

1. Enter your CSV data in the text area
2. Set the chart title and axis labels
3. Choose the output format (PNG or PDF)
4. Click "Generate Chart" to view in the browser
5. Click "Generate & Download" to download the file
