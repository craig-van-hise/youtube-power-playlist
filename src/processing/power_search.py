import os
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.database.firestore_client import FirestoreClient
from datetime import datetime

# Usage: python src/processing/power_search.py --uid <USER_ID> --playlist <PLAYLIST_ID> --topic "Jazz" --max 25

def power_search(user_id, playlist_id, topic, max_results=25):
    print(f"Starting Power Search for User: {user_id}, Playlist: {playlist_id}")
    print(f"Topic: {topic}, Max: {max_results}")

    # 1. Init Firestore
    db_client = FirestoreClient()
    db = db_client.db

    # 2. Init YouTube API
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in environment.")
        return

    youtube = build('youtube', 'v3', developerKey=api_key)

    # 3. Search YouTube
    try:
        search_response = youtube.search().list(
            q=topic,
            part='snippet',
            maxResults=max_results,
            type='video',
            order='relevance' # or date
        ).execute()

        new_videos = []
        for item in search_response.get('items', []):
            vid_id = item['id']['videoId']
            title = item['snippet']['title']
            
            # 4. Check De-duplication (Local Playlist & Watched History)
            # Check Playlist
            doc_ref = db.collection(f"users/{user_id}/playlists/{playlist_id}/videos").document(vid_id)
            if doc_ref.get().exists:
                print(f"Skipping (Already in Playlist): {title}")
                continue

            # Check Watched History (Ghost Record)
            history_ref = db.collection(f"users/{user_id}/watched_history").document(vid_id)
            if history_ref.get().exists:
                print(f"Skipping (In Watched History): {title}")
                continue

            # 5. Add to Firestore
            video_data = {
                "youtube_id": vid_id,
                "title": title,
                "channel": item['snippet']['channelTitle'],
                "thumbnail_url": item['snippet']['thumbnails']['high']['url'],
                "duration": "-", # Requires separate details fetch
                "published_at": item['snippet']['publishedAt'].split('T')[0],
                "addedAt": datetime.now().isoformat(),
                "watched": False,
                "tldr": "-",
                "tags": [topic],
                "rating": 0
            }

            doc_ref.set(video_data)
            print(f"Added: {title}")
            new_videos.append(video_data)

        print(f"Search Complete. Added {len(new_videos)} videos.")

    except HttpError as e:
        print(f"An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Power Search for a User Playlist')
    parser.add_argument('--uid', required=True, help='Firebase User ID')
    parser.add_argument('--playlist', required=True, help='Playlist Document ID')
    parser.add_argument('--topic', required=True, help='Search Topic')
    parser.add_argument('--max', type=int, default=25, help='Max results')
    
    args = parser.parse_args()
    
    power_search(args.uid, args.playlist, args.topic, args.max)
