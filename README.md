# ResearchArchiveBot

This project is a Python-based automation tool for scraping, analyzing, and archiving YouTube videos on a specific topic.

## Features

- **Exhaustive Scraping:** Overcomes the YouTube Data API's 500-result limit by searching in time-based chunks.
- **AI-Powered Analysis:** Uses the Gemini API to extract structured data from video titles and descriptions.
- **Firestore Integration:** Stores the analyzed data in a NoSQL database.
- **Static Site Generation:** Creates a searchable and sortable HTML table of the archived data.

## Project Structure

- `src/`: Contains the core application logic.
- `scripts/`: Holds utility scripts for one-time tasks and manual runs.
- `config/`: For configuration files.
- `requirements.txt`: Lists the Python dependencies.
- `.env.example`: An example file for environment variables.
