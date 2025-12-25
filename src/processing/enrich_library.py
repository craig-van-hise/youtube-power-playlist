
import os
import json
import time
from src.database.firestore_client import FirestoreClient
from src.ingestion.ai_analyst import AIAlyst

def enrich_library():
    print("--- Starting Enrichment Agent ---")
    
    # Init Clients
    db_client = FirestoreClient()
    ai_analyst = AIAlyst()
    
    # 1. Fetch from Firestore (Source of Truth)
    print("Fetching videos from Firestore ('archive_items')...")
    videos = db_client.get_all_videos("archive_items")
    print(f"Found {len(videos)} videos.")
    
    updates_count = 0
    enriched_videos = []

    for video in videos:
        # Check if enrichment is needed
        tldr = video.get('tldr', '')
        needs_tldr = not tldr or "Analysis failed" in tldr
        
        needs_date = not video.get('original_date')
        # We can also check tags if empty
        needs_tags = not video.get('tags') or len(video.get('tags', [])) == 0
        
        if needs_tldr or needs_date or needs_tags:
            print(f"\nEnriching: {video.get('title', 'Unknown Title')}")
            
            # Call AI
            metadata = ai_analyst.analyze_video_metadata(
                title=video.get('title', ''),
                description=video.get('description', '')
            )
            
            # Update fields if AI returned them
            if metadata.get('tldr'): video['tldr'] = metadata['tldr']
            if metadata.get('original_date'): video['original_date'] = metadata['original_date']
            if metadata.get('tags'): video['tags'] = metadata['tags']
            
            # Write back to Firestore IMMEDIATELY
            db_client.save_video_data("archive_items", video['youtube_id'], video)
            updates_count += 1
            
            # Rate limit slightly to be nice to API
            time.sleep(1)
        else:
            print(f"Skipping (Already Enriched): {video.get('title')}")
            
        enriched_videos.append(video)

    print(f"\nEnrichment Complete. Updated {updates_count} videos.")
    
    # 2. Update Cache (data/playlist.json)
    output_dir = 'data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'playlist.json')
    with open(output_path, 'w') as f:
        json.dump(enriched_videos, f, indent=2)
        
    print(f"Cache updated: {output_path}")

if __name__ == "__main__":
    enrich_library()
