
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from firebase_admin import credentials, initialize_app

def verify_env_variables():
    """Checks for the presence of all required environment variables."""
    print("1. Verifying presence of environment variables...")
    required_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "YOUTUBE_API_KEY",
        "GEMINI_API_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS"
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"   FAILED: Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not os.path.exists(creds_path):
        print(f"   FAILED: Service Account JSON file not found at path: {creds_path}")
        return False

    print("   SUCCESS: All required environment variables are set.")
    return True

def verify_youtube_api_key():
    """Tests the YouTube API key by making a simple request."""
    print("\n2. Verifying YouTube Data API v3 key...")
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("   SKIPPED: YOUTUBE_API_KEY not set.")
        return

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(part="snippet", q="test", maxResults=1)
        request.execute()
        print("   SUCCESS: YouTube API key is valid.")
    except HttpError as e:
        error_details = e.content.decode('utf-8')
        print(f"   FAILED: YouTube API key is invalid or the API is not enabled.")
        print(f"   DETAILS: {error_details}")

def verify_gemini_api_key():
    """Tests the Gemini API key."""
    print("\n3. Verifying Gemini API key...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("   SKIPPED: GEMINI_API_KEY not set.")
        return
    
    try:
        genai.configure(api_key=api_key)
        genai.list_models()
        print("   SUCCESS: Gemini API key is valid.")
    except Exception as e:
        print(f"   FAILED: Gemini API key is invalid or the Vertex AI API is not enabled.")
        print(f"   DETAILS: {e}")

def verify_service_account():
    """Tests the Service Account by initializing the Firebase Admin SDK."""
    print("\n4. Verifying Firebase Admin SDK (Service Account)...")
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not creds_path or not project_id:
        print("   SKIPPED: GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT not set.")
        return

    try:
        cred = credentials.Certificate(creds_path)
        initialize_app(cred, {
            'projectId': project_id,
        })
        print("   SUCCESS: Firebase Admin SDK initialized successfully.")
    except Exception as e:
        print(f"   FAILED: Could not initialize Firebase Admin SDK.")
        print(f"   DETAILS: {e}")


def main():
    """Runs all verification steps."""
    print("--- Environment Verification Script ---")
    load_dotenv()
    
    if not verify_env_variables():
        print("\nAborting due to missing variables or files. Please check your .env setup.")
        sys.exit(1)
    
    verify_youtube_api_key()
    verify_gemini_api_key()
    verify_service_account()
    
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    main()
