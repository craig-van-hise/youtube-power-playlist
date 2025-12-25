
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
- **Jukebox Mode:** Data table dominates the screen (scrollable); player is a sticky footer bar.
- **Study Mode:** Split-screen; 30% width playlist on the left, 70% width video player and note-taking area on the right.

### The Player (Persistent Shell)
- **State-Aware:** Swapping modes does not stop video audio.
- **Transport:** Play/Pause, Next/Prev, Auto-Advance.
- **Scrubber:** Interactive progress bar with real-time time display (Current / Duration) in Jukebox Mode.
- **Volume:** Hover-reveal slider (defaults to 80%).

### Data Table (Power User Features)
- **Interaction:** Single-click select, Double-click play.
- **Playlist Management:** Drag-and-drop reordering, Multi-selection.
- **Metadata Automation:** Client-side "AI Analyst" (Gemini 2.5 Flash) automatically enriches videos with TL;DR, Tags, and Original Date upon addition. Auto-fetch Title/Channel via Noembed.
- **Columns:** 
    - **Visibility:** Modal with "Select All" toggle to show/hide columns.
    - **Static Locking:** "Index", "Thumbnail", and "Rating" columns are fixed-width and cannot be resized.
    - **Persistence:** Column visibility and custom widths are saved to localStorage.
- **Backfill:** "Enrich" button allows batch-processing of imported videos missing metadata.

## 4. Current State & Known Bugs
- **Status:** Functional Prototype (Phase 2 Complete).
- **Navigation:** Mode switching, play logic, note-saving, and scrubber are working.
- **Cloud Features:** 
    - Google Auth & Multi-playlist support implemented.
    - Client-Side Enrichment (Gemini 2.5) verified.
    - Power Search (YouTube Data API) active.
- **Known Issue:** Column resizing is implemented but currently causes columns to shrink/squish instead of triggering horizontal scroll (Fix deferred by user).
- **Known Issue:** Sorting logic needs verification for Date-specific strings.
- **Resolved:** Vertical scrolling in Jukebox mode restored (CSS Fix).
- **Resolved:** Enrichment "missing model" errors fixed by upgrading to Gemini 2.5.

## 5. Next Planned Steps
- Refine CSS for vertical column lines and drag-handles.
- Finalize the "Study Mode" resizable panels (Sidebar width and Video height).
- Clean up the `dev.nix` configuration for deployment readiness.