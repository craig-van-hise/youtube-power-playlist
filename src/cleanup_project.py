import os
import shutil

def cleanup_project():
    print("Cleaning up Project Directory...")
    
    # 1. Remove Backup Files
    backups = [f for f in os.listdir('.') if f.endswith('.bak') or f.endswith('.tmp')]
    for b in backups:
        os.remove(b)
        print(f"Removed backup: {b}")

    # 2. Ensure Data Dirs exist
    os.makedirs('data/thumbnails', exist_ok=True)
    os.makedirs('data/scraped_content', exist_ok=True)

    print("Cleanup Complete. Project is ready for Phase 3.")

if __name__ == "__main__":
    cleanup_project()
