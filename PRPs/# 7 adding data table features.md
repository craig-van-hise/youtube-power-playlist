Great, Sorting works. Now we are moving to **Step 3: Drag and Drop Reordering**.

Please read `src/publishing/template/index.html.j2` and modify the JavaScript and HTML to enable row reordering.

**Requirements:**
1.  **HTML Update:** Update `renderTable()` so that every row (`<tr>`) has `draggable="true"`.
2.  **State Tracking:** Add a variable `let draggedItemIndex = null;` to track the source row.
3.  **Event Handlers:** Add these functions:
    * `handleDragStart(e, index)`: Set `draggedItemIndex`, set effectAllowed to 'move'.
    * `handleDragOver(e, index)`: Prevent default behavior to allow dropping. Add a visual class (e.g., `drop-target`) to the row being hovered over to show where the item will land.
    * `handleDragLeave(e, index)`: Remove the visual class.
    * `handleDrop(e, index)`: 
        * Remove the item from `draggedItemIndex` in the `playlist` array.
        * Insert it at the new `index`.
        * **Important:** Reset `sortState = { col: null, asc: true }` (because manual ordering overrides sorting).
        * Call `savePlaylist()` and `renderTable()`.
4.  **CSS:** Add a `.drop-target` class in the `<style>` section (e.g., `border-top: 2px solid #137fec;`) so the user sees where the row is going.

**Please implement these changes in the template file.**