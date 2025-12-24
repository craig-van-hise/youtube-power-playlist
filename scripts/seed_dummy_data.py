
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Define the project root directory, which is one level up from the 'scripts' directory.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from the .env file located in the project root.
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

# Add the project root to the Python path to allow for absolute imports from 'src'
sys.path.append(project_root)

# Now that the path is set, we can import our modules.
from src.database.firestore_client import FirestoreClient

def seed_data():
    """
    Connects to Firestore and inserts a collection of dummy data
    for testing the site generator.
    """
    try:
        db_client = FirestoreClient()
    except Exception as e:
        print(f"Error connecting to Firestore: {e}")
        print("Please ensure your environment is configured correctly as per SETUP_GUIDE.md")
        return

    collection_name = "archive_items"

    dummy_videos = [
        {
            "youtube_id": "dummy_id_1",
            "title": "Steve Gadd - 'Aja' Drum Solo - Live in '78",
            "url": "https://www.youtube.com/watch?v=fake_video_1",
            "upload_date": "2010-05-15T12:00:00Z",
            "performance_date": "1978-09-20",
            "is_date_estimated": False,
            "primary_artist": "Steely Dan",
            "context": "Live",
            "last_updated": datetime.utcnow().isoformat(),
            "ai_confidence_score": 0.95,
        },
        {
            "youtube_id": "dummy_id_2",
            "title": "Paul Simon - 50 Ways to Leave Your Lover - Steve Gadd",
            "url": "https://www.youtube.com/watch?v=fake_video_2",
            "upload_date": "2012-08-01T18:30:00Z",
            "performance_date": "1975-10-25",
            "is_date_estimated": False,
            "primary_artist": "Paul Simon",
            "context": "Studio",
            "last_updated": datetime.utcnow().isoformat(),
            "ai_confidence_score": 0.98,
        },
        {
            "youtube_id": "dummy_id_3",
            "title": "Chick Corea - Spain - with Steve Gadd on drums",
            "url": "https://www.youtube.com/watch?v=fake_video_3",
            "upload_date": "2015-02-11T09:00:00Z",
            "performance_date": "1992-07-12",
            "is_date_estimated": False,
            "primary_artist": "Chick Corea Elektric Band",
            "context": "Live",
            "last_updated": datetime.utcnow().isoformat(),
            "ai_confidence_score": 0.92,
        },
        {
            "youtube_id": "dummy_id_4",
            "title": "Steve Gadd Band - 'Green Foam' - Studio Rehearsal",
            "url": "https://www.youtube.com/watch?v=fake_video_4",
            "upload_date": "2018-11-30T21:00:00Z",
            "performance_date": "2018-11-28",
            "is_date_estimated": True,
            "primary_artist": "Steve Gadd Band",
            "context": "Rehearsal",
            "last_updated": datetime.utcnow().isoformat(),
            "ai_confidence_score": 0.88,
        },
        {
            "youtube_id": "dummy_id_5",
            "title": "Steve Gadd: Drum Lesson on Mozambique",
            "url": "https://www.youtube.com/watch?v=fake_video_5",
            "upload_date": "2020-03-20T15:00:00Z",
            "performance_date": "2020-03-18",
            "is_date_estimated": True,
            "primary_artist": "Steve Gadd",
            "context": "Lesson",
            "last_updated": datetime.utcnow().isoformat(),
            "ai_confidence_score": 0.90,
        },
         {
            "youtube_id": "dummy_id_6",
            "title": "Eric Clapton - 'Tears in Heaven' (Unplugged) ft. Steve Gadd",
            "url": "https://www.youtube.com/watch?v=fake_video_6",
            "upload_date": "2009-10-27T14:00:00Z",
            "performance_date": "1992-01-16",
            "is_date_estimated": False,
            "primary_artist": "Eric Clapton",
            "context": "Live",
            "last_updated": datetime.utcnow().isoformat(),
            "ai_confidence_score": 0.97,
        }
    ]

    print(f"Seeding {len(dummy_videos)} dummy records into Firestore collection '{collection_name}'...")

    for video in dummy_videos:
        db_client.save_video_data(collection_name, video["youtube_id"], video)

    print("\nSeed complete!")
    print("--------------------------------------------------")
    print("To see the result, run the site generator script:")
    print("python src/publishing/site_generator.py")
    print("--------------------------------------------------")

if __name__ == "__main__":
    seed_data()
