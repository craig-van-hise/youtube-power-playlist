I see the `.env.example` file, but I don't have the API keys or the Service Account JSON yet, and I'm not sure where to find them.

Please generate a file called `SETUP_GUIDE.md` that is a beginner-friendly, step-by-step tutorial on how to get them.

Please include:
1.  **Project ID:** How to find my current Google Cloud Project ID inside this environment (Project IDX/Firebase).
2.  **YouTube API Key:** A direct link to the Google Cloud Console "Credentials" page and steps to generate a free "API Key" for YouTube Data API v3.
3.  **Service Account:** Steps to go to "IAM & Admin" > "Service Accounts", create a new account called "archivist", and download the JSON key file.
4.  **Filing the .env:** Explicit instructions on where to save that JSON file in my project folder and how to paste the path into the `.env` file.

Once you have generated this guide, please also generate a script called `scripts/verify_env.py` that I can run to test if my keys are valid before I try any actual scraping.