import csv

input_file = "teacher.csv"
output_file = "Columbia_teacher.csv"

# Read the input CSV file and store the data in a list
data = []
with open(input_file, "r", newline="") as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # Skip the header row
    for row in csv_reader:
        data.append(row)

# Filter out duplicate rows based on the email column
filtered_data = []
seen_emails = set()
for row in data:
    email = row[2]
    if email not in seen_emails:
        filtered_data.append(row)
        seen_emails.add(email)

# Write the filtered data to a new CSV file
with open(output_file, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)  # Write header row
    csv_writer.writerows(filtered_data)  # Write the filtered data rows
