
# YouTube Power Playlist: Project State

## 1. Project Overview
A "Dual-Mode" Single Page Application (SPA) designed for research, music archiving, and active learning. The app features a persistent YouTube IFrame player that stays active across layout shifts.

## 2. Core Architecture
- **Backend:** Python-based static site generator (`src/publishing/site_generator.py`) that fetches data from Firestore and injects it into a standalone HTML shell.
- **Frontend:** A single-file HTML/JS/Tailwind application (`public/index.html`).
- **Data Model:** Firestore `archive_items` collection.
- **Persistence:** Uses `localStorage` to save user notes, watched status, and playlist modifications (Add/Delete/Reorder).

## 3. Current Feature Set
### Layouts
- **Jukebox Mode:** Data table dominates the screen; player is a sticky footer bar.
- **Study Mode:** Split-screen; 30% width playlist on the left, 70% width video player and note-taking area on the right.

### The Player (Persistent Shell)
- **State-Aware:** Swapping modes does not stop the video audio.
- **Transport:** Play/Pause toggle, Next/Prev buttons, and Auto-Advance logic.
- **Volume:** Defaults to 80% (Safe-zone); features a hover-reveal slider.

### Data Table (Power User Features)
- **Interaction:** Single-click to select (grey), Double-click to play (blue).
- **Playlist Management:** Drag-and-drop reordering; Multi-selection (Shift/Cmd/Ctrl).
- **Metadata Automation:** "Add Video" modal uses the Noembed API to auto-fetch Title and Channel from a URL.
- **Data Columns:** Watched (Checkbox), # (Auto-updating), Title, Original Date, Upload Date, Channel, Description, Tags, and Duration.

## 4. Current State & Known Bugs
- **Status:** Functional Prototype.
- **Navigation:** Mode switching, play logic, and note-saving are confirmed working.
- **Known Issue:** Column resizing is visually implemented in headers but requires a more robust JS event handler for full table-column sync.
- **Known Issue:** Sorting logic is implemented but needs verification for Date-specific sorting strings.

## 5. Next Planned Steps
- Refine CSS for vertical column lines and drag-handles.
- Finalize the "Study Mode" resizable panels (Sidebar width and Video height).
- Clean up the `dev.nix` configuration for deployment readiness.