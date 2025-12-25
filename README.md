
# YouTube Powerlist Player 🎧🎬

A high-performance, **Dual-Mode Single Page Application (SPA)** designed for researchers, musicians, and power users who need to organize, archive, and study YouTube content with zero friction.

## 🚀 The Core Concept: "One App, Two Views"

Unlike a standard playlist, the **YouTube Powerlist Player** features a persistent "Persistent Shell" architecture. You can switch between layouts without stopping the video audio, turning your browser into a dedicated command center.

* **Jukebox Mode:** A management-first view where the data table dominates the screen and the player is a sticky footer. Best for bulk organizing, sorting, and background listening.
* **Study Mode:** A focus-first view with a split-screen layout. Features a large video player on the right with integrated note-taking and a compact playlist on the left.

---

## ✨ Key Features

### 🛠 Power-User Data Table

* **Persistent Shell:** Video playback is never interrupted when switching between Jukebox and Study modes.
* **Double-Click to Play:** Prevents accidental playback; single-click selects a row, double-click triggers the player.
* **Multi-Selection:** Full support for `Shift + Click` (range) and `Cmd/Ctrl + Click` (individual) selections.
* **Drag-and-Drop Reordering:** Manually reorder your playlist by dragging rows; indices update automatically.
* **Interactive Columns:** Sortable headers, resizable widths, and visible vertical separators.

### 🤖 Automation & Intelligence

* **Auto-Metadata Fetching:** Paste a YouTube URL in the "Add Video" modal; the app uses the oEmbed API to automatically fetch the **Title** and **Channel Name**.
* **Smart Transport:** Integrated "Auto-Advance" logic plays the next video in your sorted list when the current one ends. Includes a visual scrubber in Jukebox mode for precise seeking.
* **Note-Taking with Timestamps:** Take rich text notes in Study Mode. A single click grabs the current video time and injects a clickable timestamp into your notes.

### 💾 Persistence & Storage

* **Local-First State:** All modifications (added videos, deleted rows, custom reordering, and notes) are saved to `localStorage`.
* **Firestore Integration:** The base library is synced from a central Firestore database.

---

## 🛠 Tech Stack

* **Backend:** Python Site Generator (Builds the static shell and injects database state).
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript.
* **Database:** Google Firestore.
* **API:** YouTube IFrame API & Noembed (Metadata).

---

## 📂 Project Structure

```text
├── public/
│   ├── index.html          # The generated SPA (Persistent Shell)
│   └── data.json           # Local copy of Firestore data
├── src/
│   ├── database/
│   │   ├── firestore_client.py   # Connection to Google Firestore
│   │   └── seed_real_data.py     # Utility to inject curated test videos
│   └── publishing/
│       └── site_generator.py     # The "Engine" that builds the app
├── PROJECT_STATE.md        # Technical roadmap and current progress
└── dev.nix                 # Project IDX environment configuration

```

---

## ⚙️ Setup & Development

### 1. Initialize Environment

Ensure your Python virtual environment is active and dependencies are installed:

```bash
source .venv/bin/activate
pip install -r requirements.txt

```

### 2. Generate the Site

Build the latest version of the application from your database:

```bash
export PYTHONPATH=$PYTHONPATH:. && python src/publishing/site_generator.py

```

### 3. Local Preview

Start a local server to view the app:

```bash
python -m http.server 8000 --directory public

```

---

## 📝 Usage Tips

* **Volume Control:** Hover over the volume icon in Jukebox mode to reveal the slider. It defaults to a safe **80%** to prevent audio peaks.
* **Column Visibility:** Click the 'Columns' button to toggle specific data fields or use 'Select All' for a full view.
* **Deletion:** Select a row and hit `Backspace` or `Delete` to remove a video from your local session.
* **Resizing:** In Study Mode, drag the vertical bar between the playlist and player to adjust your workspace.

---

**Current Status:** Functional Prototype / Beta.
**Last Updated:** December 2025.

---
