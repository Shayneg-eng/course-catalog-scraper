import csv

csv_file = "courses.csv"

# Read the CSV
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Filter: Only keep rows where all important fields are filled
# Important fields: Course Code, Title, Description, Credits, Prerequisites, Course Types
filtered_rows = []
for row in rows:
    course_code = row.get("Course Code", "").strip()
    title = row.get("Title", "").strip()
    description = row.get("Description", "").strip()
    credits = row.get("Credits", "").strip()
    prerequisites = row.get("Prerequisites", "").strip()
    course_types = row.get("Course Types", "").strip()
    
    # Keep only if all important fields are present
    if course_code and title and description and credits and prerequisites and course_types:
        filtered_rows.append(row)

# Write filtered data back to CSV
fieldnames = ["URL", "Course Code", "Title", "Description", "Credits", "Prerequisites", "Course Types", "Previous Course Number"]
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered_rows)

print(f"Filtered courses.csv")
print(f"Original rows: {len(rows)}")
print(f"Filtered rows: {len(filtered_rows)}")
print(f"Removed: {len(rows) - len(filtered_rows)}")
