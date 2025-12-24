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
        
        json_string = json.dumps(videos)
        html_content = self.get_html_template().replace('__INJECT_DATA__', json_string)
        
        html_path = os.path.join(self.output_dir, 'index.html')
        with open(html_path, 'w') as f:
            f.write(html_content)
        print(f"Successfully generated {html_path}")

    def get_html_template(self):
        return '''
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Powerlist</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: { "primary": "#137fec", "bg-dark": "#101922", "surface": "#192633", "border": "#233648", "text-sub": "#92adc9" },
                    fontFamily: { sans: ["Inter", "sans-serif"] }
                }
            }
        }
    </script>
    <style>
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #111a22; }
        ::-webkit-scrollbar-thumb { background: #233648; border-radius: 4px; }
        
        body { overflow: hidden; height: 100vh; display: flex; flex-direction: column; }
        #app-container { flex: 1; display: flex; overflow: hidden; transition: all 0.3s ease; }

        /* Jukebox Mode */
        .mode-jukebox { flex-direction: column; }
        .mode-jukebox #left-panel { flex: 1; width: 100%; overflow-y: auto; }
        .mode-jukebox #player-panel { height: 80px; width: 100%; border-top: 1px solid #233648; background: #111a22; flex-direction: row; z-index: 50; }
        .mode-jukebox .study-only { display: none !important; }
        .mode-jukebox .jukebox-only { display: flex !important; }
        .mode-jukebox .col-compact-hide { display: table-cell; } /* Show all cols in Jukebox */

        /* Study Mode */
        .mode-study { flex-direction: row; }
        .mode-study #left-panel { width: 30%; min-width: 350px; border-right: 1px solid #233648; overflow-y: auto; }
        .mode-study #player-panel { flex: 1; display: flex; flex-direction: column; background: #101922; overflow-y: auto; }
        .mode-study .study-only { display: flex !important; }
        .mode-study .jukebox-only { display: none !important; }
        .mode-study .col-compact-hide { display: none; } /* Hide details in Sidebar */

        /* Row States */
        .row-selected { background-color: #233648; } 
        .row-active { background-color: rgba(19, 127, 236, 0.15) !important; border-left: 3px solid #137fec; } 
        
        /* Volume Slider */
        .vol-container:hover .vol-slider { display: block; }
        .vol-slider { display: none; width: 80px; margin-left: 10px; accent-color: #137fec; }

        /* Tags */
        .tag-pill { background: #233648; color: #92adc9; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-right: 4px; display: inline-block; border: 1px solid #233648; white-space: nowrap; }

        /* Modal */
        dialog::backdrop { background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(2px); }
        .input-dark { width: 100%; background: #101922; border: 1px solid #233648; border-radius: 4px; padding: 8px; margin-bottom: 16px; color: white; font-size: 14px; outline: none; }
        .input-dark:focus { border-color: #137fec; }
        .input-disabled { background: #192633; color: #92adc9; cursor: not-allowed; }
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
            <button onclick="setMode('jukebox')" id="btn-jukebox" class="px-4 py-1.5 rounded-md text-sm font-medium text-white bg-primary shadow">Jukebox</button>
            <button onclick="setMode('study')" id="btn-study" class="px-4 py-1.5 rounded-md text-sm font-medium text-text-sub hover:text-white">Study Mode</button>
        </div>
        <div class="flex items-center gap-3"><div class="size-9 rounded-full bg-surface border border-border"></div></div>
    </header>

    <div id="app-container" class="mode-jukebox">
        <div id="left-panel" class="bg-bg-dark" tabindex="0">
            <div class="jukebox-only p-4 flex justify-between items-center">
                <h2 class="text-xl font-bold">All Videos</h2>
                <button onclick="openAddModal()" class="bg-primary hover:bg-blue-600 px-4 py-2 rounded text-sm font-medium flex items-center gap-2">
                    <span class="material-symbols-rounded text-sm">add</span> Add Video
                </button>
            </div>
            <table class="w-full text-left border-collapse">
                <thead class="bg-surface sticky top-0 z-10 text-xs uppercase text-text-sub font-semibold tracking-wider shadow-sm">
                    <tr>
                        <th class="px-4 py-3 w-12 text-center">#</th>
                        <th class="px-4 py-3 w-12 text-center col-compact-hide">Watched</th>
                        <th class="px-4 py-3">Title</th>
                        <th class="px-4 py-3 col-compact-hide">Original Date</th>
                        <th class="px-4 py-3 col-compact-hide">Upload Date</th>
                        <th class="px-4 py-3">Channel</th>
                        <th class="px-4 py-3 col-compact-hide">Tags</th>
                        <th class="px-4 py-3 w-24 text-right">Dur.</th>
                    </tr>
                </thead>
                <tbody id="tableBody" class="divide-y divide-border/50 text-sm text-text-sub"></tbody>
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
                    <button onclick="playPrev()" class="text-text-sub hover:text-white"><span class="material-symbols-rounded text-2xl">skip_previous</span></button>
                    <button onclick="togglePlay()" class="bg-primary text-white rounded-full p-2 hover:scale-105 shadow-lg shadow-primary/30">
                        <span id="play-icon" class="material-symbols-rounded text-2xl">play_arrow</span>
                    </button>
                    <button onclick="playNext()" class="text-text-sub hover:text-white"><span class="material-symbols-rounded text-2xl">skip_next</span></button>
                </div>

                <div class="w-1/4 flex justify-end items-center vol-container">
                    <span class="material-symbols-rounded text-text-sub">volume_up</span>
                    <input type="range" id="vol-slider" min="0" max="100" value="80" class="vol-slider" oninput="setVolume(this.value)">
                </div>
            </div>
        </div> 
    </div>

    <dialog id="addModal" class="bg-surface border border-border rounded-xl p-6 shadow-2xl backdrop:bg-black/80 text-white w-96">
        <h3 class="text-lg font-bold mb-4">Add YouTube Video</h3>
        <input type="text" id="newUrl" oninput="debounceFetch()" placeholder="Paste YouTube URL..." class="input-dark">
        <input type="text" id="newTitle" placeholder="Video Title" class="input-dark">
        <input type="text" id="newChannel" placeholder="Channel Name" class="input-dark input-disabled" readonly>
        
        <label class="text-xs text-text-sub uppercase font-bold tracking-wider mb-1 block">Tags (comma separated)</label>
        <input type="text" id="newTags" placeholder="e.g. Jazz, Study, Drum Solo" class="input-dark">

        <div class="flex justify-end gap-2 mt-4">
            <button onclick="closeAddModal()" class="px-4 py-2 text-sm text-text-sub hover:text-white">Cancel</button>
            <button onclick="submitAddVideo()" class="px-4 py-2 bg-primary rounded text-sm font-medium hover:bg-blue-600">Add to List</button>
        </div>
    </dialog>

    <script>
        const INJECTED_DATA = __INJECT_DATA__;
        // Data Structure Update: Ensure new fields exist
        let playlist = JSON.parse(localStorage.getItem('my_playlist_v3')) || INJECTED_DATA.map(v => ({
            ...v,
            tags: v.tags || [],
            original_date: v.published_at || '', 
            watched: false
        }));

        let activeVideoId = null;
        let selectedIndex = -1;
        let currentIndex = -1;
        let player = null;
        let fetchTimeout = null;

        function renderTable() {
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            
            playlist.forEach((item, index) => {
                const vidId = item.youtube_id;
                const isActive = (vidId === activeVideoId);
                const isSelected = (index === selectedIndex);

                const tr = document.createElement('tr');
                let classes = "group transition-colors cursor-pointer border-l-2 ";
                if (isActive) classes += "row-active ";
                else if (isSelected) classes += "row-selected ";
                else classes += "hover:bg-surface border-transparent ";
                
                tr.className = classes;
                tr.onclick = () => selectRow(index);
                tr.ondblclick = () => loadVideoByIndex(index);

                // --- NEW COLUMN RENDERING ---
                tr.innerHTML = `
                    <td class="px-4 py-3 text-center text-text-sub group-hover:text-white">
                        ${isActive ? '<span class="material-symbols-rounded text-primary animate-pulse">equalizer</span>' : (index + 1)}
                    </td>
                    <td class="px-4 py-3 text-center col-compact-hide">
                        <input type="checkbox" ${item.watched ? 'checked' : ''} onclick="toggleWatched(event, ${index})" class="rounded bg-bg-dark border-border text-primary focus:ring-0 cursor-pointer">
                    </td>
                    <td class="px-4 py-3">
                        <div class="text-white font-medium truncate">${item.title}</div>
                    </td>
                    <td class="px-4 py-3 text-xs text-text-sub font-mono col-compact-hide">${item.original_date || '-'}</td>
                    <td class="px-4 py-3 text-xs text-text-sub font-mono col-compact-hide">${item.published_at || '-'}</td>
                    <td class="px-4 py-3 text-sm text-text-sub">${item.channel || ''}</td>
                    <td class="px-4 py-3 col-compact-hide">
                        ${(item.tags || []).map(t => `<span class="tag-pill">${t}</span>`).join('')}
                    </td>
                    <td class="px-4 py-3 text-right font-mono text-xs">${item.duration || '--:--'}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        // --- NEW LOGIC: WATCHED TOGGLE ---
        function toggleWatched(e, index) {
            e.stopPropagation(); // Stop click from selecting row
            playlist[index].watched = !playlist[index].watched;
            savePlaylist();
        }

        // --- FETCH METADATA ---
        function debounceFetch() { clearTimeout(fetchTimeout); fetchTimeout = setTimeout(fetchMetadata, 500); }

        async function fetchMetadata() {
            const url = document.getElementById('newUrl').value;
            if (url.length < 10) return;
            document.getElementById('newTitle').placeholder = "Fetching...";
            
            try {
                const res = await fetch(`https://noembed.com/embed?url=${url}`);
                const data = await res.json();
                if (data.title) {
                    document.getElementById('newTitle').value = data.title;
                    document.getElementById('newChannel').value = data.author_name;
                }
            } catch (e) { console.error(e); }
        }

        // --- PLAYLIST MANAGEMENT ---
        const modal = document.getElementById('addModal');
        function openAddModal() { modal.showModal(); }
        function closeAddModal() { modal.close(); }

        function submitAddVideo() {
            const url = document.getElementById('newUrl').value;
            const title = document.getElementById('newTitle').value || 'New Video';
            const channel = document.getElementById('newChannel').value || 'User';
            const tagsRaw = document.getElementById('newTags').value;
            
            let vidId = '';
            if (url.includes('v=')) vidId = url.split('v=')[1].split('&')[0];
            else if (url.includes('youtu.be/')) vidId = url.split('youtu.be/')[1];

            if (vidId) {
                const newVideo = {
                    youtube_id: vidId,
                    title: title,
                    channel: channel,
                    duration: 'VOD',
                    published_at: new Date().toISOString().split('T')[0],
                    tags: tagsRaw ? tagsRaw.split(',').map(t=>t.trim()) : [],
                    watched: false
                };
                playlist.push(newVideo);
                savePlaylist();
                renderTable();
                closeAddModal();
                // Clear
                document.getElementById('newUrl').value = '';
                document.getElementById('newTitle').value = '';
                document.getElementById('newChannel').value = '';
                document.getElementById('newTags').value = '';
            } else { alert('Invalid URL'); }
        }

        function deleteSelected() {
            if (selectedIndex === -1) return;
            if (confirm('Delete selected video?')) {
                playlist.splice(selectedIndex, 1);
                selectedIndex = -1; 
                savePlaylist();
                renderTable();
            }
        }

        function savePlaylist() {
            // Updated Key to 'v3' to reset structure safely
            localStorage.setItem('my_playlist_v3', JSON.stringify(playlist));
        }

        // --- PLAYER LOGIC ---
        function selectRow(index) { selectedIndex = index; renderTable(); }
        
        function loadVideoByIndex(index) {
            if (index < 0 || index >= playlist.length) return;
            currentIndex = index; selectedIndex = index;
            const item = playlist[index];
            activeVideoId = item.youtube_id;
            
            document.getElementById('footer-title').textContent = item.title;
            document.getElementById('study-title').textContent = item.title;
            renderTable();

            const savedNote = localStorage.getItem('note_' + activeVideoId) || '';
            document.getElementById('notes-area').value = savedNote;

            if(player && player.loadVideoById) player.loadVideoById(activeVideoId);
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Delete' || e.key === 'Backspace') {
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
                deleteSelected();
            }
        });

        function playNext() { loadVideoByIndex(currentIndex + 1); }
        function playPrev() { loadVideoByIndex(currentIndex - 1); }
        function togglePlay() { if(player) player.getPlayerState() === 1 ? player.pauseVideo() : player.playVideo(); }
        function setVolume(val) { if(player) player.setVolume(val); }
        function updatePlayIcon(isPlaying) { document.getElementById('play-icon').textContent = isPlaying ? 'pause' : 'play_arrow'; }
        
        function setMode(mode) {
            const app = document.getElementById('app-container');
            const vidStage = document.getElementById('video-stage');
            const btnJuke = document.getElementById('btn-jukebox');
            const btnStudy = document.getElementById('btn-study');

            if (mode === 'study') {
                app.className = 'mode-study';
                document.body.classList.add('mode-study');
                vidStage.style.display = 'block'; 
                btnStudy.classList.replace('text-text-sub', 'text-white');
                btnStudy.classList.add('bg-primary', 'shadow');
                btnJuke.classList.remove('bg-primary', 'shadow', 'text-white');
                btnJuke.classList.add('text-text-sub');
            } else {
                app.className = 'mode-jukebox';
                document.body.classList.remove('mode-study');
                vidStage.style.display = 'none';
                btnJuke.classList.replace('text-text-sub', 'text-white');
                btnJuke.classList.add('bg-primary', 'shadow');
                btnStudy.classList.remove('bg-primary', 'shadow', 'text-white');
                btnStudy.classList.add('text-text-sub');
            }
        }

        const notesArea = document.getElementById('notes-area');
        notesArea.addEventListener('input', () => { if(activeVideoId) localStorage.setItem('note_' + activeVideoId, notesArea.value); });
        function insertTimestamp() {
            if(!player || !activeVideoId) return;
            const time = Math.floor(player.getCurrentTime());
            const min = Math.floor(time / 60);
            const sec = time % 60;
            const stamp = `[${min}:${sec < 10 ? '0'+sec : sec}]`;
            notesArea.value += `\n${stamp} `;
            localStorage.setItem('note_' + activeVideoId, notesArea.value);
        }

        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        function onYouTubeIframeAPIReady() {
            player = new YT.Player('yt-player', {
                height: '100%', width: '100%', videoId: '',
                playerVars: { 'playsinline': 1, 'autoplay': 1 },
                events: { 'onReady': (e) => e.target.setVolume(80), 'onStateChange': (e) => {
                    if (e.data == YT.PlayerState.PLAYING) updatePlayIcon(true);
                    else updatePlayIcon(false);
                    if (e.data == YT.PlayerState.ENDED) playNext();
                }}
            });
        }

        renderTable();
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    generator = SiteGenerator()
    generator.generate_static_site()
