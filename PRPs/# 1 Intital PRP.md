I need you to scaffold a Python-based automation project called "ResearchArchiveBot". This project has two distinct goals:
1. Exhaustively scrape YouTube for a specific topic (e.g., "Steve Gadd drumming") using the YouTube Data API, overcoming the 500-result limit by slicing searches by time windows.
2. Use an LLM (Gemini API) to analyze video metadata and extract the *actual* performance date, artist, and context, storing this "Source of Truth" in Firebase Firestore.
3. Generate a static HTML/JSON export of this data that can be hosted on GitHub Pages or Wix as a sortable, searchable table.

Please set up the project with the following specifications:

### 1. Tech Stack
* **Language:** Python 3.11+
* **Cloud:** Google Cloud Functions (for the daily scraper) + Cloud Scheduler.
* **Database:** Firebase Firestore (NoSQL).
* **AI:** Google Gemini API (`google-generativeai`) for metadata extraction.
* **APIs:** YouTube Data API v3 (`google-api-python-client`).
* **Frontend Export:** A script to generate a static `index.html` with DataTables.js (for easy sorting/filtering).

### 2. Directory Structure
Create a file structure that looks like this:
/research-archive-bot
  /src
    /ingestion
      __init__.py
      youtube_scraper.py   # Handles time-window search logic
      ai_analyst.py        # Handles Gemini API prompts for date extraction
    /database
      firestore_client.py  # Handles DB connection and duplicate checking
    /publishing
      site_generator.py    # Fetches DB data and builds static HTML/JSON
    main.py                # Entry point for Cloud Function
  /scripts
    one_time_auth.py       # For generating initial OAuth refresh tokens
    manual_run.py          # For testing locally
  /config
    settings.py
  requirements.txt
  .env.example
  README.md

### 3. Key Function Requirements

**A. The Ingestion Engine (`youtube_scraper.py` & `ai_analyst.py`)**
* Implement a loop that accepts a start_date and end_date.
* The scraper must search in small chunks (e.g., 30 days) to ensure deep retrieval.
* For every video found, pass the Title and Description to the `ai_analyst`.
* The `ai_analyst` must use the Gemini API to extract:
    * `performance_date` (ISO format, estimated if necessary)
    * `is_date_estimated` (boolean)
    * `primary_artist`
    * `context` (Live, Studio, Interview, etc.)
* Store the result in Firestore collection `archive_items`. Document ID should be the YouTube Video ID.

**B. The Data Model (Firestore)**
* Collection: `archive_items`
* Fields: `youtube_id`, `title`, `url`, `upload_date` (from YouTube), `performance_date` (from AI), `artist`, `context`, `ai_confidence_score`, `last_updated`.
* Collection: `system_status`
* Fields: `last_search_window_end_date` (to track progress through history).

**C. The Publisher (`site_generator.py`)**
* Write a function that queries Firestore for ALL items.
* Generate a `public/data.json` file.
* Generate a `public/index.html` file that loads that JSON into a simple HTML table using a library like DataTables.js or Grid.js so users can sort by `performance_date`.

### 4. Dependencies
Please create a `requirements.txt` including:
* `firebase-admin`
* `google-api-python-client`
* `google-auth-oauthlib`
* `google-generativeai`
* `python-dotenv`
* `jinja2` (for HTML templating)

Now, please generate the directory structure and the code for `requirements.txt`, `src/ingestion/youtube_scraper.py`, `src/ingestion/ai_analyst.py`, and `src/publishing/site_generator.py`.