
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

from src.ingestion.youtube_scraper import YouTubeScraper
from src.publishing.site_generator import SiteGenerator

def main():
    """
    Main function to run the complete archival process.
    """
    # 1. Scrape YouTube for new videos
    # Get the YouTube API key from environment variables
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    if not youtube_api_key:
        raise ValueError("YOUTUBE_API_KEY environment variable not set.")

    scraper = YouTubeScraper(api_key=youtube_api_key)

    # Define search parameters
    search_topic = "Steve Gadd drumming"
    # For a recurring job, you'd likely want to search for videos in the last day or week.
    start_date = datetime.utcnow() - timedelta(days=7)
    end_date = datetime.utcnow()

    print("Starting YouTube scrape...")
    # We'll do a targeted search for recent videos rather than an exhaustive one.
    scraper.search_by_topic_and_time_window(search_topic, start_date, end_date)
    print("YouTube scrape finished.")

    # 2. Generate the static site
    print("Generating static site...")
    site_generator = SiteGenerator()
    site_generator.generate_static_site(output_dir="public")
    print("Static site generation finished.")

if __name__ == "__main__":
    main()
