import os
import time
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.database.firestore_client import FirestoreClient
from src.ingestion.ai_analyst import AIAlyst

def enrich_cloud_playlists():
    print("--- Starting Cloud Playlist Enrichment ---")
    
    # Init Clients
    try:
        db_client = FirestoreClient()
        db = db_client.db
        ai_analyst = AIAlyst()
    except Exception as e:
        print(f"Failed to initialize clients: {e}")
        return

    print("Traversing 'users' -> 'playlists' -> 'videos' manually...")
    
    # DEBUG: Check connection
    print(f"DEBUG: Connected to Project: {db.project}")
    collections = db.collections()
    print(f"DEBUG: Root Collections found: {[c.id for c in collections]}")

    users = db.collection('users').stream()
    
    count = 0
    updated = 0
    
    for user in users:
        print(f"Checking User: {user.id}")
        playlists = db.collection('users').document(user.id).collection('playlists').stream()
        
        for playlist in playlists:
            playlist_data = playlist.to_dict()
            print(f"  Checking Playlist: {playlist_data.get('name', playlist.id)}")
            
            videos = db.collection('users').document(user.id).collection('playlists').document(playlist.id).collection('videos').stream()
            
            for doc in videos:
                count += 1
                video = doc.to_dict()
                video_id = video.get('youtube_id') or doc.id
                title = video.get('title', 'Unknown Title')
                
                # Check if enrichment is needed
                tldr = video.get('tldr', '')
                needs_tldr = not tldr or "Analysis failed" in tldr
                
                # We check tags too
                tags = video.get('tags')
                needs_tags = tags is None or len(tags) == 0
                
                if needs_tldr or needs_tags:
                    print(f"\n[{count}] Enriching: {title} ({video_id})")
                    
                    try:
                        # Call AI
                        metadata = ai_analyst.analyze_video_metadata(
                            title=title,
                            description=video.get('description', '') or title # Use title if desc missing
                        )
                        
                        updates = {}
                        if metadata.get('tldr'): updates['tldr'] = metadata['tldr']
                        if metadata.get('original_date'): updates['original_date'] = metadata['original_date']
                        if metadata.get('tags'): updates['tags'] = metadata['tags']
                        
                        if updates:
                            doc.reference.set(updates, merge=True)
                            print(f"   -> Updated: {list(updates.keys())}")
                            updated += 1
                            time.sleep(1) # Rate limit
                        else:
                            print("   -> No meaningful updates from AI.")
                            
                    except Exception as e:
                        print(f"   -> Error processing {video_id}: {e}")
                        
                else:
                    # print(f"[{count}] Skipping (Enriched): {title}")
                    pass

    print(f"\n--- Enrichment Complete ---")
    print(f"Scanned: {count} videos")
    print(f"Enriched: {updated} videos")

if __name__ == "__main__":
    enrich_cloud_playlists()
