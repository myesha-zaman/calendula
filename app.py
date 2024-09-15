from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pdfplumber
import csv
import os
import glob
from openai import OpenAI
from ics import Calendar, Event
from datetime import datetime, timedelta
import io

# Initialize a calendar object
calendar = Calendar()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api_key = "INSERT API KEY"

client = OpenAI(api_key=api_key)

def find_most_recent_pdf(directory):
    pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
    if not pdf_files:
        return None
    most_recent_file = max(pdf_files, key=os.path.getmtime)
    return most_recent_file

def extract_text_from_pdf(pdf_path):
    text_content = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_content += page.extract_text() or ''
            text_content += '\n'
    return text_content

def convert_text_to_html(text):
    html_content = f"<html><body><p>{text.replace('\n', '<br>')}</p></body></html>"
    return html_content

def save_html_to_csv(html_content, filename, pdf_path):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['PDF Path', 'HTML Content'])
        writer.writerow([pdf_path, html_content])

@app.route('/upload', methods=['POST'])
def upload():
    downloads_path = request.args.get('path', os.path.expanduser('~/Downloads'))  # Adjust the default if necessary

    pdf_path = find_most_recent_pdf(downloads_path)
    if pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path)
        html_content = convert_text_to_html(extracted_text)
        
        csvText = callGPT(html_content)
        print(csvText)
        ics_data = createICS(csvText)
        
        return send_file(
            io.BytesIO(ics_data), 
            as_attachment=True, 
            download_name='schedule.ics', 
            mimetype='text/calendar'
        )
    else:
        return jsonify({'message': 'No PDF files found in the specified directory.'}), 404
    
def callGPT(text):
    prompt = 'without any other placeholder text give me a csv in text with columns: [Subject, Start Date, End Date, Start Time, End Time, Location, Description] for: """' + text + '""" JUST GIVE ME THE RESULT AND NOTHING ELSE AND NO MARKDOWN AND TIME VALUE SHOULD BE IN ISO 8601'
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return None

def createICS(csvText):
    # Read CSV data
    reader = csv.DictReader(csvText.strip().splitlines())

    # Initialize a new Calendar object to avoid global state issues
    calendar = Calendar()

    # Iterate through CSV rows and create events
    for row in reader:
        event = Event()
        event.name = row['Subject']
        event.begin = f"{row['Start Date']} {row['Start Time']}"
        event.end = f"{row['End Date']} {row['End Time']}"
        event.location = row['Location']
        event.description = row['Description']
        calendar.events.add(event)

    # Save the calendar to an .ics file in memory
    ics_file = io.StringIO()
    ics_file.writelines(calendar)
    ics_file.seek(0)  # Reset file pointer to the beginning

    return ics_file.read().encode('utf-8')  # Return as bytes for send_file

if __name__ == '__main__':
    app.run(debug=True, port=5000)
