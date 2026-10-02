import csv

input_file = "courses.csv"
output_file = "cleaned_classes.csv"

# Read and filter the CSV
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    cleaned_rows = []
    
    for row in reader:
        course_code = row.get("Course Code", "").strip()
        title = row.get("Title", "").strip()
        description = row.get("Description", "").strip()
        credits = row.get("Credits", "").strip()
        prerequisites = row.get("Prerequisites", "").strip()
        course_types = row.get("Course Types", "").strip()
        
        # Only keep rows where ALL important fields are present
        if course_code and title and description and credits and prerequisites and course_types:
            cleaned_rows.append(row)

# Write only cleaned rows to new file
fieldnames = ["URL", "Course Code", "Title", "Description", "Credits", "Prerequisites", "Course Types", "Previous Course Number"]
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_rows)

print(f"Cleaned CSV created: {output_file}")
print(f"Total cleaned courses: {len(cleaned_rows)}")
