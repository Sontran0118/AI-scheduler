from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import pdfplumber
import sqlite3
import re

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the maximum file upload size to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Set up the folder for storing uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure the 'uploads' folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check if the uploaded file is a PDF
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to extract text from a PDF
def process_pdf(filepath):
    extracted_text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() or ''  # Handle None values
    return extracted_text

# Function to clean and store data in the database
def clean_and_store_data(extracted_text):
    # Extract student information
    student_name = re.search(r"Student name\s+(.+)", extracted_text).group(1)
    student_id = re.search(r"Student ID\s+(\d+)", extracted_text).group(1)
    major = re.search(r"Major\s+(.+)", extracted_text).group(1)

    # Extract credits applied
    credits_applied = int(re.search(r"Credits applied:\s+(\d+)", extracted_text).group(1))

    # Extract SBC classes not taken
    sbc_not_taken = re.findall(r"Still needed: (\d+ Class in [A-Z]+)", extracted_text)
    sbc_not_taken = ", ".join(sbc_not_taken)

    # Extract required courses not taken
    required_courses_not_taken = re.findall(r"Still needed: (\d+ Class in [A-Z]+\s?\d+)", extracted_text)
    required_courses_not_taken = ", ".join(required_courses_not_taken)

    # Connect to the database
    conn = sqlite3.connect('student_audits.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cleaned_student_data (
            student_name TEXT,
            student_id TEXT,
            major TEXT,
            credits_applied INTEGER,
            sbc_classes_not_taken TEXT,
            required_courses_not_taken TEXT
        )
    """)

    # Insert cleaned data into the table
    cursor.execute("""
        INSERT INTO cleaned_student_data (
            student_name, student_id, major, credits_applied,
            sbc_classes_not_taken, required_courses_not_taken
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (student_name, student_id, major, credits_applied, sbc_not_taken, required_courses_not_taken))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Route to handle PDF file upload
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract text from the PDF
        extracted_text = process_pdf(filepath)

        # Clean and store the extracted data in the database
        clean_and_store_data(extracted_text)

        return jsonify({
            "message": "File successfully uploaded and data cleaned",
            "filename": filename,
            "data": extracted_text
        }), 200
    else:
        return jsonify({"error": "Invalid file type. Only PDF allowed."}), 400

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)