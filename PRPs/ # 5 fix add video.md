I am building the **YouTube Power Playlist**.

**Context & Architecture:**
1.  **The Stack:** This is a Python-based Static Site Generator. The file `src/publishing/site_generator.py` fetches data from Firestore and generates a single `index.html` file.
2.  **The App:** It is a Single Page Application (SPA) contained entirely within a Python string in `site_generator.py`.
3.  **Key Feature:** It uses a "Persistent Shell" architecture. The YouTube IFrame exists in a container that never reloads. We toggle CSS classes (`.mode-jukebox` vs `.mode-study`) to change the layout around the video.
4.  **Current State:** The app works. We can add videos (via auto-metadata fetch), play them, and switch modes.
5.  **Data Storage:** We use `localStorage` to persist the playlist and notes.

---

**The Task: Add Sorting & Multi-Selection**

I need you to modify the JavaScript inside `src/publishing/site_generator.py` to add "Power User" list features.

Please read `src/publishing/site_generator.py` and apply the following changes to the **JavaScript section only**:

**1. Add State Variables:**
   Add `let sortState = { col: null, asc: true };` and `let selectedIndices = new Set();` to the top of the script.

**2. Implement `sortPlaylist(key)`:**
   - It should sort the global `playlist` array based on the provided key (e.g., 'title', 'duration').
   - It needs to toggle Ascending/Descending if the same header is clicked twice.
   - It must call `savePlaylist()` and `renderTable()` after sorting.

**3. Implement `handleRowClick(e, index)`:**
   - **Single Click:** Clears selection and selects the clicked row.
   - **Shift + Click:** Selects a range of rows from the `lastSelectedIndex` to current.
   - **Cmd/Ctrl + Click:** Toggles selection of the specific row without clearing others.
   - Note: Clicking a row does *not* play the video (that's already handled by `ondblclick`, which calls `loadVideoByIndex`).

**4. Update `renderTable()`:**
   - Update the table headers (`<th>`) to include `onclick="sortPlaylist('key')"` and show a visual arrow (▲/▼) if active.
   - Update the table rows (`<tr>`) to use `onclick="handleRowClick(event, index)"`.
   - Apply a CSS class `.row-selected` to rows present in the `selectedIndices` Set.

**Important Constraint:**
Do NOT overwrite the entire file. Please analyze the existing code and provide the specific JavaScript modifications needed to achieve this.