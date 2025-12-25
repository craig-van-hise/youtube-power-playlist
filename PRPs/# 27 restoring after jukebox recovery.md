
# Product Requirements Document: Study Mode & Layout Refinement

## 1. Objective

Optimize the **Study Mode** interface for better multitasking by introducing a nested, resizable panel system. Ensure a distinct, clean separation between "Study" and "Jukebox" modes while maintaining a strict 16:9 aspect ratio for the video player.

## 2. Layout & UI Architecture

The application must transition from a static grid to a dynamic, **triple-splitter** layout.

### 2.1 Study Mode Restructuring

* **Left Sidebar (Vertical Splitter):** * Top: Video Table (List of available videos).
* Bottom: **Notes Panel** (Relocated from the right side).
* Control: A horizontal splitter must allow users to adjust the height ratio between the table and notes.


* **Main Stage (Right Side):**
* Top: Video Player.
* Bottom: **Video Header/Metadata** (Relocated "Now Playing" and timestamp controls).
* Control: A horizontal splitter must allow users to adjust the height of the video player relative to the metadata.



### 2.2 Mode Switching (Study vs. Jukebox)

* **Jukebox Mode:** Must trigger a "Hardened" layout.
* Hide all elements tagged `.study-only` (Notes, splitters).
* Force the Jukebox container to `position: absolute` with 100% width/height.
* The "All Videos" table must occupy the full viewport.


* **Study Mode:** Must show all elements tagged `.study-only` and re-initialize the resizing logic.

---

## 3. Functional Requirements

### 3.1 Advanced Resizing Logic

The `makeResizable()` function must be overhauled to manage three concurrent splitters without layout collapse:

1. **`vSplitter`**: Controls the global width distribution between the Sidebar and the Video Stage.
2. **`leftSplitter`**: Controls the vertical height between the Video Table and Notes.
3. **`rightSplitter`**: Controls the vertical height between the Video Player and Metadata.

### 3.2 16:9 Aspect Ratio Constraint

The Video Player must remain functional and visually consistent by locking its proportions.

* **Bi-directional Update**:
* If the user drags the **Vertical Splitter** (changing width), the Video Player height must recalculate to .
* If the user drags the **Right Horizontal Splitter** (changing height), the Sidebar width must recalculate to accommodate the new video dimensions.



---

## 4. Technical Constraints & Performance

* **DOM Integrity**: The HTML hierarchy (`index.html.j2`) must support nested flexboxes to prevent "jumping" when splitters are moved.
* **Error Handling**: Wrap `renderTable` and `makeResizable` initializations in `try-catch` blocks. If a component fails to load, the rest of the UI must remain interactive (No "White Screen of Death").
* **Styling**: Use utility classes (e.g., `.flex-col`) for layout management and distinct border/background colors to define "Zones."

---

## 5. Success Criteria

* [ ] Users can take notes while watching a video without the notes panel overlapping the video list.
* [ ] Resizing the sidebar does not result in black bars (letterboxing) on the video player.
* [ ] Switching to Jukebox mode successfully removes all Study Mode UI clutter.

