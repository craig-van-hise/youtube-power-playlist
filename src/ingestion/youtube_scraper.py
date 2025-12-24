
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime, timedelta

# Import other project modules
from src.ingestion.ai_analyst import AIAlyst
from src.database.firestore_client import FirestoreClient

class YouTubeScraper:
    def __init__(self, api_key):
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
        self.ai_analyst = AIAlyst()
        self.db_client = FirestoreClient()

    def search_by_topic_and_time_window(self, topic, start_date, end_date, max_results=50):
        """
        Searches for videos on a specific topic within a given time window.
        """
        # Format dates for the YouTube API
        published_after = start_date.isoformat("T") + "Z"
        published_before = end_date.isoformat("T") + "Z"

        request = self.youtube.search().list(
            part="snippet",
            q=topic,
            type="video",
            publishedAfter=published_after,
            publishedBefore=published_before,
            maxResults=max_results
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            upload_date = item["snippet"]["publishedAt"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Get AI analysis of the video metadata
            ai_data = self.ai_analyst.analyze_video_metadata(title, description)

            # Prepare data for Firestore
            document_data = {
                "youtube_id": video_id,
                "title": title,
                "url": video_url,
                "upload_date": upload_date,
                **ai_data,  # Add AI-extracted data
                "last_updated": datetime.utcnow().isoformat()
            }

            # Save to Firestore, using the YouTube video ID as the document ID
            self.db_client.save_video_data("archive_items", video_id, document_data)

    def exhaustive_search(self, topic, overall_start_date, overall_end_date, chunk_days=30):
        """
        Performs an exhaustive search by breaking the time range into smaller chunks.
        """
        current_start_date = overall_start_date
        while current_start_date < overall_end_date:
            current_end_date = current_start_date + timedelta(days=chunk_days)
            if current_end_date > overall_end_date:
                current_end_date = overall_end_date

            print(f"Searching from {current_start_date} to {current_end_date}...")
            self.search_by_topic_and_time_window(topic, current_start_date, current_end_date)

            # Move to the next time window
            current_start_date = current_end_date

if __name__ == "__main__":
    # Example usage (requires API_KEY to be set as an environment variable)
    API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable not set.")

    scraper = YouTubeScraper(api_key=API_KEY)
    
    # Define the search topic and the overall time range
    search_topic = "Steve Gadd drumming"
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 1, 1)

    scraper.exhaustive_search(search_topic, start_date, end_date)
