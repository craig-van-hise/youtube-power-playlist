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
        
        json_path = os.path.join(self.output_dir, 'data.json')
        with open(json_path, 'w') as f:
            json.dump(videos, f, indent=4)
        print(f"Successfully generated {json_path}")

        html_content = self.get_html_template()
        html_path = os.path.join(self.output_dir, 'index.html')
        with open(html_path, 'w') as f:
            f.write(html_content)
        print(f"Successfully generated {html_path}")

    def get_html_template(self):
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Archive</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0" />
    
    <style>
        body { padding: 20px; background-color: #f0f2f5; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        .table-container { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); overflow-x: auto; }
        
        th, td { 
            border-bottom: 1px solid #e0e0e0; 
            border-right: 1px solid #ccc; 
            padding: 12px 10px; 
            vertical-align: middle; 
            overflow: hidden; 
            text-overflow: ellipsis;
        }
        
        td { white-space: nowrap; }
        td.wrap-text { white-space: normal; line-height: 1.4; font-size: 0.9rem; color: #555; }
        
        /* Header Styling & Sorting */
        th { background-color: #f8f9fa; position: relative; user-select: none; font-weight: 600; color: #444; cursor: pointer; }
        th:hover { background-color: #e9ecef; }
        th:last-child, td:last-child { border-right: none; } 
        
        .sort-icon { display: inline-block; width: 12px; margin-left: 5px; opacity: 0.3; font-size: 0.8rem; }
        th.sorted-asc .sort-icon::after { content: '▲'; opacity: 1; }
        th.sorted-desc .sort-icon::after { content: '▼'; opacity: 1; }

        /* Resizer */
        .resizer { position: absolute; top: 0; right: 0; width: 8px; cursor: col-resize; user-select: none; height: 100%; z-index: 10; }
        .resizer:hover { background-color: rgba(26, 115, 232, 0.2); }

        .btn-watch { 
            display: inline-flex; align-items: center; gap: 4px; 
            background-color: #e8f0fe; color: #1a73e8; border: none; 
            padding: 6px 12px; border-radius: 16px; font-weight: 600; font-size: 0.9rem; text-decoration: none; 
        }
        .btn-watch:hover { background-color: #d2e3fc; color: #174ea6; }

        .viewed-check { transform: scale(1.3); cursor: pointer; accent-color: #1a73e8; }
        .row-viewed { opacity: 0.6; background-color: #fafafa; }
        .empty-text { color: #999; font-style: italic; }
        
        #debugArea { display: none; background: #333; color: #0f0; padding: 15px; margin-top: 20px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; }
    </style>
</head>
<body>

<div class="container-fluid table-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="m-0 d-flex align-items-center gap-2">
            <span class="material-symbols-rounded text-primary">table_chart</span>
            Research Archive
        </h3>
        <div>
            <button class="btn btn-sm btn-outline-secondary me-2" onclick="toggleDebug()">🛠️ Debug</button>
            <button class="icon-btn" onclick="openModal()" title="Customize Columns">
                <span class="material-symbols-rounded">visibility</span>
            </button>
        </div>
    </div>

    <table id="archiveTable">
        <thead>
            <tr id="tableHeaders"></tr>
        </thead>
        <tbody id="tableBody"></tbody>
    </table>
    
    <div id="debugArea"></div>
</div>

<div class="modal fade" id="columnModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title d-flex align-items-center gap-2">Customize View</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body" id="columnCheckboxes"></div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
    const columns = [
        { key: ['viewed'], label: 'Done', type: 'checkbox', width: '60px', sortable: false },
        { key: ['url', 'video_url', 'link'], label: 'Watch', type: 'link', width: '110px', sortable: false },
        { key: ['title', 'video_title'], label: 'Title', width: '250px', sortable: true },
        // Both dates use type 'date' for unified formatting
        { key: ['performance_date', 'date'], label: 'Perf. Date', type: 'date', width: '120px', sortable: true },
        { key: ['published_at', 'upload_date', 'dateUploaded'], label: 'Upload Date', type: 'date', width: '120px', sortable: true },
        { key: ['description', 'desc', 'snippet'], label: 'Description', type: 'text-wrap', width: '450px', sortable: true }
    ];

    let allData = [];
    let sortState = { colIndex: -1, direction: 'asc' };

    fetch('data.json')
        .then(res => res.json())
        .then(data => {
            allData = data;
            renderTable();
            initModal();
        });

    function getValue(item, keys) {
        if (Array.isArray(keys)) {
            for (let k of keys) {
                if (item[k] !== undefined && item[k] !== null) return item[k];
            }
            return null;
        }
        return item[keys];
    }

    // Unified Date Formatter: YYYY-MM-DD
    function formatDate(isoString) {
        if (!isoString) return '';
        const date = new Date(isoString);
        if (isNaN(date.getTime())) return isoString;
        return date.toISOString().split('T')[0];
    }

    function handleSort(colIndex) {
        // Toggle direction if same column, else reset to asc
        if (sortState.colIndex === colIndex) {
            sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
        } else {
            sortState.colIndex = colIndex;
            sortState.direction = 'asc';
        }

        const col = columns[colIndex];
        
        allData.sort((a, b) => {
            let valA = getValue(a, col.key) || '';
            let valB = getValue(b, col.key) || '';

            // Handle Strings vs Numbers vs Dates
            if (col.type === 'date') {
                valA = new Date(valA).getTime() || 0;
                valB = new Date(valB).getTime() || 0;
            } else if (typeof valA === 'string') {
                valA = valA.toLowerCase();
                valB = valB.toLowerCase();
            }

            if (valA < valB) return sortState.direction === 'asc' ? -1 : 1;
            if (valA > valB) return sortState.direction === 'asc' ? 1 : -1;
            return 0;
        });

        renderTable();
    }

    function renderTable() {
        const thead = document.getElementById('tableHeaders');
        const tbody = document.getElementById('tableBody');
        thead.innerHTML = '';
        tbody.innerHTML = '';

        // 1. Headers
        columns.forEach((col, index) => {
            const th = document.createElement('th');
            th.style.width = col.width;
            th.dataset.colIndex = index;
            
            // Sorting Logic
            if (col.sortable) {
                th.onclick = () => handleSort(index);
                if (sortState.colIndex === index) {
                    th.classList.add(sortState.direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
                }
            } else {
                th.style.cursor = 'default';
            }

            // Header Content
            th.innerHTML = `<span>${col.label}</span>${col.sortable ? '<span class="sort-icon"></span>' : ''}`;

            // Resizer (with stopPropagation to prevent sorting when resizing)
            const resizer = document.createElement('div');
            resizer.classList.add('resizer');
            resizer.addEventListener('mousedown', (e) => {
                e.stopPropagation(); // Don't sort when clicking resize handle
                initResize(e, th);
            });
            th.appendChild(resizer);
            
            thead.appendChild(th);
        });

        // 2. Rows
        allData.forEach(item => {
            const uniqueId = item.youtube_id || item.id || Math.random().toString(36);
            const isViewed = localStorage.getItem('viewed_' + uniqueId) === 'true';
            const tr = document.createElement('tr');
            if(isViewed) tr.classList.add('row-viewed');

            columns.forEach((col, index) => {
                const td = document.createElement('td');
                td.dataset.colIndex = index;
                let val = getValue(item, col.key);

                if (col.type === 'checkbox') {
                    td.innerHTML = `<input type="checkbox" class="viewed-check" ${isViewed ? 'checked' : ''} onclick="toggleViewed('${uniqueId}', this.closest('tr'), this.checked)">`;
                    td.style.textAlign = 'center';
                } else if (col.type === 'link') {
                    td.innerHTML = `<a href="${val || '#'}" target="_blank" class="btn-watch"><span class="material-symbols-rounded" style="font-size:16px">play_circle</span> Watch</a>`;
                } else if (col.type === 'date') {
                    td.textContent = val ? formatDate(val) : '';
                } else if (col.type === 'text-wrap') {
                    td.classList.add('wrap-text');
                    if (val) { td.textContent = val; td.title = val; } 
                    else { td.innerHTML = '<span class="empty-text">No description available</span>'; }
                } else {
                    td.textContent = val || '';
                    td.title = val || '';
                }
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        applyVisibility();
    }

    function toggleViewed(id, row, isChecked) {
        localStorage.setItem('viewed_' + id, isChecked);
        if (isChecked) row.classList.add('row-viewed'); else row.classList.remove('row-viewed');
    }

    function toggleDebug() {
        const d = document.getElementById('debugArea');
        d.style.display = (d.style.display === 'block') ? 'none' : 'block';
        if (d.style.display === 'block') {
            d.innerHTML = "<strong>RAW DATA (First Item):</strong>\\n" + JSON.stringify(allData[0], null, 2);
        }
    }
    
    // Resizing Logic
    let startX, startWidth, resizableCol;
    function initResize(e, th) {
        resizableCol = th; startX = e.pageX; startWidth = th.offsetWidth;
        document.addEventListener('mousemove', doResize); document.addEventListener('mouseup', stopResize);
    }
    function doResize(e) { resizableCol.style.width = (startWidth + e.pageX - startX) + 'px'; }
    function stopResize() { document.removeEventListener('mousemove', doResize); document.removeEventListener('mouseup', stopResize); }
    
    // Visibility Logic
    function initModal() {
        const container = document.getElementById('columnCheckboxes');
        columns.forEach((col, index) => {
            container.innerHTML += `<div class="form-check"><input class="form-check-input" type="checkbox" value="${index}" checked onchange="applyVisibility()"><label class="form-check-label">${col.label}</label></div>`;
        });
    }
    function applyVisibility() {
        const checkboxes = document.querySelectorAll('#columnCheckboxes input');
        checkboxes.forEach(box => {
            const display = box.checked ? '' : 'none';
            document.querySelectorAll(`[data-col-index="${box.value}"]`).forEach(el => el.style.display = display);
        });
    }
    const modalObj = new bootstrap.Modal(document.getElementById('columnModal'));
    function openModal() { modalObj.show(); }
</script>
</body>
</html>
'''

if __name__ == "__main__":
    generator = SiteGenerator()
    generator.generate_static_site()