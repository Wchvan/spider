import csv

input_file = "teacher.csv"
output_file = "LaGuardia_community_college_teacher.csv"

# Function to capitalize the first letter of a string
def capitalize_first_letter(s):
    return s.capitalize()

# Read the input CSV file and capitalize the first letter of First Name and Last Name
with open(input_file, "r", newline="") as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # Skip the header row
    updated_data = [[capitalize_first_letter(row[0]), capitalize_first_letter(row[1]), row[2]] for row in csv_reader]

# Write the updated data to a new CSV file
with open(output_file, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)
    csv_writer.writerows(updated_data)
