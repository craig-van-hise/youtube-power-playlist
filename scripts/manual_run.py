
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

from src.ingestion.youtube_scraper import YouTubeScraper
from src.publishing.site_generator import SiteGenerator

def run_full_archive():
    """
    Performs a full, exhaustive scrape and generates the site.
    This is for manual runs, not for the regular, scheduled job.
    """
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    if not youtube_api_key:
        raise ValueError("YOUTUBE_API_KEY is not set.")

    scraper = YouTubeScraper(api_key=youtube_api_key)
    
    # Define the exhaustive search parameters
    search_topic = "Steve Gadd drumming"
    start_date = datetime(2005, 1, 1) # Start from near the beginning of YouTube
    end_date = datetime.utcnow()

    print("Starting exhaustive YouTube scrape...")
    scraper.exhaustive_search(search_topic, start_date, end_date)
    print("Exhaustive scrape finished.")

    # Generate the static site
    print("Generating static site...")
    site_generator = SiteGenerator()
    site_generator.generate_static_site(output_dir="public")
    print("Static site generated.")

if __name__ == "__main__":
    run_full_archive()
