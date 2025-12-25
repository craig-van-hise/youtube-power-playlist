

# Product Requirements Prompt (PRP): Phase 2 - Cloud & Power Features

**Role:** Senior Full-Stack Architect & AI Automation Specialist
**Project Phase:** Phase 2 - "The Cloud Upgrade"
**Context:** We have a functional Jukebox/Study interface. Now we need to implement the backend "Power User" features: Authentication, Multi-Playlist Management, Advanced YouTube Scraping ("Power Search"), and Smart History Management.

**Objective:**
Implement the 4 core features described below. You must manage this complexity by maintaining a **Master Task List** and checking off items as you complete them. You are responsible for both the **Frontend UI** (Modals, Buttons) and the **Backend Logic** (Firestore Schema, API Scripts).

---

## 📋 The Master Plan (Your Feature List)

### 1. 🔐 Google Authentication

* **Goal:** Allow users to sign in with their Google Account.
* **UI:** Replace the placeholder "Circle" in the top right with the user's actual Google Avatar.
* **Logic:**
* Integrate `Firebase Authentication` (Google Provider).
* On successful login, fetch the user's Google Playlists (via YouTube Data API scope).
* Store the user's profile in a Firestore `users` collection.



### 2. 💾 Multi-Playlist Persistence (Load/Save)

* **Goal:** The app must manage *multiple* playlists, not just one.
* **Schema Change:** Move from a single `videos` collection to a hierarchy: `users/{userId}/playlists/{playlistId}/videos`.
* **UI:**
* **"Load Playlist" Button:** Opens a Modal listing all playlists saved to the user's account.
* **"Save Playlist" Button:** (Auto-save is preferred, but manual "Save As" for new searches).
* **Playlist Name:** Editable field (defaults to Search Topic or YouTube Playlist Name).


* **Persistence:** The app must remember the last active playlist and load it upon login.

### 3. ⚡ Power Search (The "Smart Scraper")

* **Goal:** A tool to build self-updating playlists based on criteria.
* **UI:** "Power Search" Button -> Opens Configuration Modal.
* **Inputs:** Topic, Keywords, Channel ID, Date Range (Start/End), Max Videos (Toggle for "Unlimited").
* **Action:** "Start Search" Button.


* **Backend Logic:**
* **Immediate:** Fetch the first 25 results via YouTube Data API immediately and render them.
* **Scheduled Capable:** The search logic must be written as a reusable script (`src/processing/power_search.py`) that can be triggered by a Cron job or Scheduler to fetch subsequent batches later, respecting API quotas.
* **Deduplication:** Never add a video that is already in the playlist.



### 4. 👻 Smart "Delete Watched" (The Ghost Record)

* **Goal:** Allow users to clear their view without breaking the "Smart Scraper."
* **The Problem:** If I delete a video I watched, the Scraper might find it again next week and re-add it.
* **The Solution:**
* **UI:** Button "Clear Watched".
* **Action:** Removes the video from the *visible* playlist.
* **Backend:** Adds the `video_id` to a separate Firestore collection: `users/{userId}/watched_history` (The "Ghost Record").
* **Logic Update:** Update the **Power Search** logic to *always* check `watched_history` before adding a new video. If it's in history, ignore it.



---

## 🛠️ Execution Instructions (How to proceed)

**Step 1: The Checklist**
Before writing any code, generate a **Markdown Checkbox List** of every file you need to touch (e.g., `src/publishing/template/index.html.j2`, `src/processing/power_search.py`, `firestore_rules`). Keep this list visible and update it in every response.

**Step 2: Architecture First**
Define the new **Firestore Data Model** clearly. Show me the JSON structure for a `User`, a `Playlist`, and the `WatchedHistory` before you implement it.

**Step 3: Implementation Order**

1. **Auth & Avatar:** Get the user logged in first.
2. **Schema Migration:** Ensure we can save/load empty playlists.
3. **Power Search UI:** Build the Modals.
4. **Power Search Logic:** Connect the YouTube API.
5. **Smart Delete:** Implement the Ghost Record logic.

**Step 4: Testing**
For each feature, define a "User Success Test" (e.g., "User logs in, avatar appears. User creates search 'Jazz', playlist populates.").

**Please begin by acknowledging these requirements and presenting your Master Task List and Proposed Firestore Schema.**