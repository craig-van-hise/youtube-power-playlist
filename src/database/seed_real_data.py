import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def seed_real_data():
    if not firebase_admin._apps:
        # Use default credential if available, otherwise just init
        firebase_admin.initialize_app()
    
    db = firestore.client()
    collection_name = "archive_items"

    # Reliable VODs (No Live Streams)
    real_videos = [
        {
            "youtube_id": "H7c8In27QyY",
            "title": "Steve Gadd - '50 Ways To Leave Your Lover' Lesson",
            "channel": "Drumeo",
            "published_at": "2020-03-24",
            "duration": "14:52",
            "description": "Steve Gadd breaks down his most famous beat. Perfect for taking timestamped notes."
        },
        {
            "youtube_id": "RzPZvU0097w",
            "title": "Herbie Hancock - 'Cantaloupe Island' (Live at Jazz à Vienne)",
            "channel": "Herbie Hancock",
            "published_at": "2018-12-14",
            "duration": "11:05",
            "description": "A masterclass in modern jazz improvisation from the legend himself."
        },
        {
            "youtube_id": "8V94_X_yX_M",
            "title": "KNOWER - 'Overtime' (Live Sesh)",
            "channel": "Louis Cole",
            "published_at": "2017-06-22",
            "duration": "04:02",
            "description": "High-energy house/funk fusion. Great for testing rapid-fire playback."
        },
        {
            "youtube_id": "t_VpBeX3UeI",
            "title": "Louis Cole - 'F it Up' (Live Sesh)",
            "channel": "Louis Cole",
            "published_at": "2018-09-25",
            "duration": "05:14",
            "description": "An incredible display of rhythm and performance energy."
        },
        {
            "youtube_id": "X_mE5uPZf-M",
            "title": "Herbie Hancock & Chick Corea - 'Cantelope Island' (Live)",
            "channel": "Jazz Video",
            "published_at": "2014-07-10",
            "duration": "12:35",
            "description": "Two titans of jazz piano together on stage."
        }
    ]

    print(f"Seeding {len(real_videos)} reliable videos...")
    for video in real_videos:
        db.collection(collection_name).document(video['youtube_id']).set(video)
        print(f"Saved: {video['title']}")

if __name__ == "__main__":
    seed_real_data()