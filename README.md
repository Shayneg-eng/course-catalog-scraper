# Course Catalog Scraper

Scrapes a university course catalog (SmartCatalog) and cleans it into structured, analyzable
CSV/JSON — course codes, titles, descriptions, and URLs.

## Pipeline
| File | Role |
|---|---|
| `downloadCourseInfo.py` | Pull the raw catalog JSON |
| `individualClassInfo.py` | Fetch per-class detail |
| `parseCoursesCSV.py` / `create_cleaned_courses.py` | Parse → clean tables |
| `filter_courses.py` / `simplify_url_column.py` | Filtering + tidying |

Outputs: `courses.csv`, `cleaned_classes*.csv`, `course_data.json`.

## Run it
```bash
python -m pip install requests beautifulsoup4 pandas
python downloadCourseInfo.py
python create_cleaned_courses.py
```
