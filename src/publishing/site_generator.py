import os
import json
from jinja2 import Environment, FileSystemLoader
from src.database.firestore_client import FirestoreClient

from dotenv import load_dotenv

# Force load .env
load_dotenv(override=True)

class SiteGenerator:
    def __init__(self):
        self.db_client = FirestoreClient()
        self.output_dir = 'public'
        self.template_dir = 'src/publishing/templates'
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_static_site(self):
        print("Fetching data from Firestore...")
        videos = self.db_client.get_all_videos("archive_items")
        
        # Serialize for JS injection
        json_string = json.dumps(videos)
        
        # Setup Jinja2
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('index.html.j2')
        
        # Render
        html_content = template.render(
            videos_json=json_string,
            gemini_api_key=self.gemini_api_key,
            firebase_config={
                "apiKey": os.getenv("FIREBASE_API_KEY"),
                "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
                "projectId": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
                "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
                "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
                "appId": os.getenv("FIREBASE_APP_ID")
            }
        )
        
        html_path = os.path.join(self.output_dir, 'index.html')
        with open(html_path, 'w') as f:
            f.write(html_content)
        print(f"Successfully generated {html_path}")

if __name__ == "__main__":
    generator = SiteGenerator()
    generator.generate_static_site()
