We are ready to build the "YouTube Power Playlist" based on the designs provided.

This requires a complete rewrite of `src/publishing/site_generator.py` to support a **Persistent Player Architecture**. The app must switch between "Jukebox Mode" and "Study Mode" without reloading the page (which would stop the video).

### 📋 The Master Task List
Please use this list to track our progress. We are currently executing **Step 1**.

1.  [ ] **Core Architecture (Step 1):** Overwrite `site_generator.py` to generate the "Persistent Shell" HTML. This includes the CSS logic to toggle layouts and the JS logic to inject Firestore data.
2.  [ ] **State Management:** Implement `localStorage` for the "Notes" feature and "Viewed" status.
3.  [ ] **YouTube API:** Connect the IFrame API so the play buttons actually control the persistent player.
4.  [ ] **Visual Polish:** Refine the Tailwind colors to match the specific `#101922` (Background) and `#137fec` (Primary Blue) from the mockups.

---

### ⚠️ ACTION REQUIRED: Step 1 (The Core Rewrite)

Please **COMPLETELY OVERWRITE** `src/publishing/site_generator.py` with the code below.

**Technical Strategy in this Code:**
* **Single HTML File:** Contains *both* layouts.
* **CSS State Machine:** The body tag gets a class `.mode-jukebox` or `.mode-study`. CSS hides/shows panels based on this class.
* **The Player:** The `#player-panel` is a flexible container. In Jukebox mode, it is fixed to the bottom (Footer). In Study mode, it becomes the right-hand column.
* **Data Injection:** We inject `RAW_DATA` directly into the HTML so the JS renders instantly.

**HERE IS THE CODE for `src/publishing/site_generator.py`:**

```python
import os
import json
from src.database.firestore_client import FirestoreClient

class SiteGenerator:
    def __init__(self):
        self.db_client = FirestoreClient()
        self.output_dir = 'public'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_static_site(self):
        print("Fetching data from Firestore...")
        videos = self.db_client.get_all_videos("archive_items")
        
        # Save raw JSON for backup
        json_path = os.path.join(self.output_dir, 'data.json')
        with open(json_path, 'w') as f:
            json.dump(videos, f, indent=4)
        print(f"Successfully generated {json_path}")

        # Generate HTML with injected data
        html_content = self.get_html_template(json.dumps(videos))
        html_path = os.path.join(self.output_dir, 'index.html')
        with open(html_path, 'w') as f:
            f.write(html_content)
        print(f"Successfully generated {html_path}")

    def get_html_template(self, json_data_string):
        return f"""
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Powerlist</title>
    <link href="[https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap)" rel="stylesheet">
    <link href="[https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0](https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0)" rel="stylesheet" />
    <script src="[https://cdn.tailwindcss.com?plugins=forms,container-queries](https://cdn.tailwindcss.com?plugins=forms,container-queries)"></script>
    <script>
        tailwind.config = {{
            darkMode: "class",
            theme: {{
                extend: {{
                    colors: {{
                        "primary": "#137fec",
                        "bg-dark": "#101922",
                        "surface": "#192633",
                        "border": "#233648",
                        "text-sub": "#92adc9"
                    }},
                    fontFamily: {{ sans: ["Inter", "sans-serif"] }}
                }}
            }}
        }}
    </script>
    <style>
        /* SCROLLBARS */
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: #111a22; }}
        ::-webkit-scrollbar-thumb {{ background: #233648; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #324d67; }}
        
        body {{ overflow: hidden; height: 100vh; display: flex; flex-direction: column; }}

        /* --- PERSISTENT SHELL LAYOUT --- */
        #app-container {{
            flex: 1;
            display: flex;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        /* MODE: JUKEBOX (List + Footer Player) */
        .mode-jukebox {{ flex-direction: column; }}
        
        .mode-jukebox #left-panel {{
            flex: 1;
            width: 100%;
            overflow-y: auto;
            border-right: none;
        }}
        
        .mode-jukebox #player-panel {{
            height: 80px; /* Sticky Footer Height */
            width: 100%;
            border-top: 1px solid #233648;
            background: #111a22;
            flex-direction: row; /* Horizontal controls */
            z-index: 50;
        }}

        /* Hide "Study Only" elements in Jukebox mode */
        .mode-jukebox .study-only {{ display: none !important; }}
        .mode-jukebox .jukebox-only {{ display: flex !important; }}
        
        /* Table Column Visibilty */
        .mode-jukebox .col-study-compact {{ display: table-cell; }} /* Show everything */


        /* MODE: STUDY (Sidebar + Right Stage) */
        .mode-study {{ flex-direction: row; }}
        
        .mode-study #left-panel {{
            width: 30%;
            min-width: 320px;
            max-width: 450px;
            border-right: 1px solid #233648;
            overflow-y: auto;
        }}
        
        .mode-study #player-panel {{
            flex: 1;
            display: flex;
            flex-direction: column; /* Vertical stack: Video -> Controls -> Notes */
            background: #101922;
            overflow-y: auto;
        }}

        .mode-study .study-only {{ display: flex !important; }}
        .mode-study .jukebox-only {{ display: none !important; }}
        
        /* Compact Table for Sidebar */
        .mode-study .col-extra {{ display: none; }} 

        /* Active Row Styling */
        .row-active {{ background-color: rgba(19, 127, 236, 0.15) !important; border-left: 3px solid #137fec; }}
    </style>
</head>
<body class="bg-bg-dark text-white font-sans">

    <header class="h-16 flex items-center justify-between px-6 bg-surface border-b border-border shrink-0 z-20">
        <div class="flex items-center gap-3">
            <div class="size-8 rounded bg-primary/20 text-primary flex items-center justify-center">
                <span class="material-symbols-rounded">play_circle</span>
            </div>
            <h1 class="font-bold text-lg hidden md:block tracking-tight">Powerlist</h1>
        </div>

        <div class="flex bg-bg-dark rounded-lg p-1 border border-border">
            <button onclick="setMode('jukebox')" id="btn-jukebox" class="px-4 py-1.5 rounded-md text-sm font-medium transition-all text-white bg-primary shadow">Jukebox</button>
            <button onclick="setMode('study')" id="btn-study" class="px-4 py-1.5 rounded-md text-sm font-medium transition-all text-text-sub hover:text-white">Study Mode</button>
        </div>

        <div class="flex items-center gap-3">
             <div class="size-9 rounded-full bg-surface border border-border"></div> </div>
    </header>

    <div id="app-container" class="mode-jukebox">
        
        <div id="left-panel" class="bg-bg-dark">
            
            <div class="jukebox-only p-4 flex justify-between items-center">
                <h2 class="text-xl font-bold">All Videos</h2>
                <button class="bg-primary hover:bg-blue-600 px-4 py-2 rounded text-sm font-medium">+ Add Video</button>
            </div>

            <table class="w-full text-left border-collapse">
                <thead class="bg-surface sticky top-0 z-10 text-xs uppercase text-text-sub font-semibold tracking-wider shadow-sm">
                    <tr>
                        <th class="px-4 py-3 w-12 text-center">#</th>
                        <th class="px-4 py-3">Title</th>
                        <th class="px-4 py-3 col-extra">Channel</th>
                        <th class="px-4 py-3 col-extra">Tags</th>
                        <th class="px-4 py-3 w-24 text-right">Dur.</th>
                    </tr>
                </thead>
                <tbody id="tableBody" class="divide-y divide-border/50 text-sm text-text-sub">
                    </tbody>
            </table>
        </div>

        <div id="player-panel">
            
            <div id="video-stage" class="w-full shrink-0 bg-black relative group" style="display:none;">
                <div class="aspect-video w-full flex items-center justify-center bg-gray-900 relative">
                     <div id="yt-player" class="w-full h-full"></div>
                </div>
            </div>

            <div class="study-only p-4 border-b border-border bg-surface flex justify-between items-center">
                <div>
                    <h2 id="study-title" class="text-white font-bold text-lg truncate max-w-md">Select a Video</h2>
                    <div class="text-xs text-text-sub mt-1">Now Playing</div>
                </div>
                <div class="flex gap-2">
                     <button onclick="insertTimestamp()" class="bg-border hover:bg-white/10 text-white px-3 py-1.5 rounded text-xs font-bold flex gap-1 items-center">
                        <span class="material-symbols-rounded text-sm">schedule</span> Timestamp
                     </button>
                </div>
            </div>

            <div class="study-only flex-1 flex flex-col p-6 bg-bg-dark min-h-0">
                <div class="flex flex-col h-full bg-surface rounded-xl border border-border overflow-hidden">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-border bg-[#1e2d3d]">
                        <span class="text-xs font-bold uppercase tracking-wider text-white">My Notes</span>
                        <button onclick="saveNotes()" class="text-xs text-primary hover:text-white">Save</button>
                    </div>
                    <textarea id="notes-area" class="flex-1 w-full bg-transparent p-4 text-gray-200 resize-none outline-none font-mono text-sm leading-relaxed" placeholder="Type notes here..."></textarea>
                </div>
            </div>

            <div class="jukebox-only w-full h-full items-center justify-between px-4 gap-4">
                <div class="flex items-center gap-3 w-1/4 min-w-[200px]">
                    <div class="flex flex-col truncate">
                        <span id="footer-title" class="text-white font-bold text-sm truncate">Select a Video</span>
                        <span class="text-xs text-primary">Powerlist Player</span>
                    </div>
                </div>
                
                <div class="flex items-center gap-6 justify-center flex-1">
                    <button class="text-text-sub hover:text-white"><span class="material-symbols-rounded text-2xl">skip_previous</span></button>
                    <button onclick="togglePlay()" class="bg-primary text-white rounded-full p-2 hover:scale-105 shadow-lg shadow-primary/30">
                        <span class="material-symbols-rounded text-2xl">play_arrow</span>
                    </button>
                    <button class="text-text-sub hover:text-white"><span class="material-symbols-rounded text-2xl">skip_next</span></button>
                </div>

                <div class="w-1/4 flex justify-end">
                    <span class="material-symbols-rounded text-text-sub">volume_up</span>
                </div>
            </div>

        </div> 
    </div>

    <script>
        const RAW_DATA = {json_data_string};
        let activeVideoId = null;
        let player = null;

        // --- RENDER LIST ---
        function renderTable() {{
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            
            RAW_DATA.forEach((item, index) => {{
                const vidId = item.youtube_id || 'dQw4w9WgXcQ';
                const title = item.title || 'Untitled';
                const channel = item.channel || 'Unknown Channel';
                const duration = item.duration || '--:--';
                const isActive = (vidId === activeVideoId);

                const tr = document.createElement('tr');
                tr.className = `group hover:bg-surface transition-colors cursor-pointer border-l-2 ${{isActive ? 'row-active' : 'border-transparent'}}`;
                tr.onclick = () => loadVideo(vidId, title);

                tr.innerHTML = `
                    <td class="px-4 py-3 text-center text-text-sub group-hover:text-white">
                        ${{ isActive ? '<span class="material-symbols-rounded text-primary animate-pulse">equalizer</span>' : (index + 1) }}
                    </td>
                    <td class="px-4 py-3">
                        <div class="text-white font-medium truncate">${{title}}</div>
                        <div class="text-text-sub text-xs md:hidden">${{channel}}</div>
                    </td>
                    <td class="px-4 py-3 col-extra">${{channel}}</td>
                    <td class="px-4 py-3 col-extra">
                        <span class="bg-surface border border-border px-2 py-0.5 rounded text-xs">Category</span>
                    </td>
                    <td class="px-4 py-3 text-right font-mono text-xs">${{duration}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // --- PLAYER LOGIC ---
        function loadVideo(id, title) {{
            activeVideoId = id;
            
            // Update UI
            document.getElementById('footer-title').textContent = title;
            document.getElementById('study-title').textContent = title;
            renderTable(); // Refresh active row styling

            // Load Notes
            const savedNote = localStorage.getItem('note_' + id) || '';
            document.getElementById('notes-area').value = savedNote;

            // YouTube API
            if(player && player.loadVideoById) {{
                player.loadVideoById(id);
                player.playVideo();
            }}
        }}

        function togglePlay() {{
            if(!player) return;
            player.getPlayerState() === 1 ? player.pauseVideo() : player.playVideo();
        }}

        // --- MODE SWITCHER ---
        function setMode(mode) {{
            const app = document.getElementById('app-container');
            const vidStage = document.getElementById('video-stage');
            const btnJuke = document.getElementById('btn-jukebox');
            const btnStudy = document.getElementById('btn-study');

            if (mode === 'study') {{
                app.className = 'mode-study';
                vidStage.style.display = 'block'; // Show Video
                
                // Button Styling
                btnStudy.classList.replace('text-text-sub', 'text-white');
                btnStudy.classList.add('bg-primary', 'shadow');
                btnJuke.classList.remove('bg-primary', 'shadow', 'text-white');
                btnJuke.classList.add('text-text-sub');

            }} else {{
                app.className = 'mode-jukebox';
                vidStage.style.display = 'none'; // Hide Video (Keep Audio)
                
                // Button Styling
                btnJuke.classList.replace('text-text-sub', 'text-white');
                btnJuke.classList.add('bg-primary', 'shadow');
                btnStudy.classList.remove('bg-primary', 'shadow', 'text-white');
                btnStudy.classList.add('text-text-sub');
            }}
        }}

        // --- NOTES ---
        const notesArea = document.getElementById('notes-area');
        notesArea.addEventListener('input', () => {{
            if(activeVideoId) localStorage.setItem('note_' + activeVideoId, notesArea.value);
        }});
        
        function insertTimestamp() {{
            if(!player || !activeVideoId) return;
            const time = Math.floor(player.getCurrentTime());
            const min = Math.floor(time / 60);
            const sec = time % 60;
            const stamp = `[${{min}}:${{sec < 10 ? '0'+sec : sec}}]`;
            notesArea.value += `\\n${{stamp}} `;
            localStorage.setItem('note_' + activeVideoId, notesArea.value);
        }}

        // --- YOUTUBE INIT ---
        var tag = document.createElement('script');
        tag.src = "[https://www.youtube.com/iframe_api](https://www.youtube.com/iframe_api)";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        function onYouTubeIframeAPIReady() {{
            player = new YT.Player('yt-player', {{
                height: '100%',
                width: '100%',
                videoId: '',
                playerVars: {{ 'playsinline': 1, 'autoplay': 1 }}
            }});
        }}

        // Start
        renderTable();

    </script>
</body>
</html>
"""

if __name__ == "__main__":
    generator = SiteGenerator()
    generator.generate_static_site()