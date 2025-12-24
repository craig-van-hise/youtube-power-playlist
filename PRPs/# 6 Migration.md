I need to upgrade the Data Table in this project to support Power User features. 

**Your Task:**
Please read `src/publishing/template/index.html.j2` and modify the HTML and JavaScript to implement **Sorting** and **Multi-Row Selection**.

**Requirements:**
1. **State Variables:** Add `let sortState = { col: null, asc: true };` and `let selectedIndices = new Set();` to the top of the `<script>` section.
2. **Sorting Logic:** - Create a `sortPlaylist(key)` function that sorts the `playlist` array.
   - It should toggle between Ascending and Descending if the same column is clicked twice.
   - It must call `renderTable()` after sorting.
3. **Multi-Selection Logic:**
   - Create a `handleRowClick(event, index)` function.
   - **Single Click:** Clears selection and selects the row.
   - **Cmd/Ctrl + Click:** Toggles individual row selection.
   - **Shift + Click:** Selects a range of rows from the last selected index.
4. **Update `renderTable()`:**
   - Update the `<th>` elements to include `onclick="sortPlaylist('column_name')"`.
   - Update the `<tr>` elements to use `onclick="handleRowClick(event, index)"`.
   - Ensure the `row-selected` CSS class is applied to rows in the `selectedIndices` Set.

**Important:** Maintain the existing Jinja2 syntax (like `{{ videos_json }}`) and the double-click playback logic (`ondblclick="loadVideoByIndex(index)"`). Do not overwrite the entire file if you can apply a clean edit.