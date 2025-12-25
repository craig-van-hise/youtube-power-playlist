import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Force load .env file, overriding system defaults
load_dotenv(override=True)

class FirestoreClient:
    def __init__(self):
        # Debug print to ensure we are using the right project
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        print(f"DEBUG: Initializing Firestore for Project ID: {project_id}")

        if not firebase_admin._apps:
            cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            
            options = {'projectId': project_id}
            
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, options)
            else:
                # Fallback for Cloud environments
                firebase_admin.initialize_app(options=options)
        
        self.db = firestore.client()

    def save_video_data(self, collection_name, document_id, data):
        """Saves or updates a video document."""
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc_ref.set(data, merge=True)
        print(f"Saved data for document: {document_id}")

    def get_all_videos(self, collection_name):
        """Retrieves all documents from a collection as a list."""
        try:
            docs = self.db.collection(collection_name).stream()
            videos = []
            for doc in docs:
                video_data = doc.to_dict()
                video_data['youtube_id'] = doc.id 
                videos.append(video_data)
            return videos
        except Exception as e:
            print(f"WARNING: Firestore access failed ({e}). Returning empty list.")
            return []