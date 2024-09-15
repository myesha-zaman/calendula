from ics import Calendar, Event
import csv
from datetime import datetime, timedelta

# Define the CSV content (replace this with reading from your actual CSV file)
csv_data = """
Subject,Start Date,Start Time,End Date,End Time,Location,Description
COMPSCI 2208B LAB,2024-09-02,08:30,2024-09-02,11:30,TBD,INTRO TO COMP ORG & ARCHITECT
ECE 3330A LAB,2024-09-03,08:30,2024-09-03,11:30,TBD,CONTROL SYSTEMS
ECE 3332A TUT,2024-09-04,08:30,2024-09-04,10:30,TBD,ELECTRIC MACHINES
ECE 3331B LEC,2024-09-05,08:30,2024-09-05,09:30,TBD,INTRO TO SIGNAL PROCESSING
"""

# Initialize a calendar object
calendar = Calendar()

# Read CSV data
reader = csv.DictReader(csv_data.strip().splitlines())

# Iterate through CSV rows and create events
for row in reader:
    event = Event()
    event.name = row['Subject']
    event.begin = f"{row['Start Date']} {row['Start Time']}"
    event.end = f"{row['End Date']} {row['End Time']}"
    event.location = row['Location']
    event.description = row['Description']
    calendar.events.add(event)

# Save the calendar to an .ics file
with open('schedule.ics', 'w') as file:
    file.writelines(calendar)

print("ICS file 'schedule.ics' created successfully.")
