import csv

input_file = "cleaned_classes.csv"
output_file = "cleaned_classes_simplified.csv"

# Read and process the CSV
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    simplified_rows = []
    
    for row in reader:
        url = row.get("URL", "").strip()
        
        # Extract course name from URL (last part after final /)
        course_name = url.split('/')[-1] if url else ""
        
        # Replace URL with course name
        row["URL"] = course_name
        simplified_rows.append(row)

# Write to new file
fieldnames = ["URL", "Course Code", "Title", "Description", "Credits", "Prerequisites", "Course Types", "Previous Course Number"]
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(simplified_rows)

print(f"Simplified CSV created: {output_file}")
print(f"Total courses: {len(simplified_rows)}")
print(f"Sample course names extracted from URLs")
