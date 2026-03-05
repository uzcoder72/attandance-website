import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from checker.models import Student, Attendance

class Command(BaseCommand):
    help = 'Imports attendance data from CSV'

    def handle(self, *args, **kwargs):
        # We need the exact path to your CSV file
        csv_file_path = 'tasks/Computer Literacy __ Ramziddin Khusanov - ELT-127-ATT.csv'
        
        with open(csv_file_path, newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            headers = next(reader) # Read the first row (the dates)
            
            # The dates start at column index 2 and end before the "Points" column
            # In your file, index 2 is "7-Oct-25". We only want the date columns.
            date_columns = {}
            for index, header_text in enumerate(headers):
                if "-25" in header_text or "-26" in header_text: 
                    # Convert string '7-Oct-25' into a real Python Date object
                    date_obj = datetime.strptime(header_text.strip(), '%d-%b-%y').date()
                    date_columns[index] = date_obj

            for row in reader:
                # If there's an empty line at the end, skip it
                if not row or row[0].strip() == '':
                    continue
                
                name = row[0].strip()
                surname = row[1].strip()

                # Get or Create the student in the database
                student, created = Student.objects.get_or_create(name=name, surname=surname)

                # Now loop through every date column for this student
                for col_index, date_obj in date_columns.items():
                    val = row[col_index].strip()
                    # If empty string, we assume they were absent
                    is_present = True if val == '1' else False
                    
                    Attendance.objects.update_or_create(
                        student=student,
                        date=date_obj,
                        defaults={'is_present': is_present}
                    )
            
        self.stdout.write(self.style.SUCCESS("Successfully imported student attendance!"))
