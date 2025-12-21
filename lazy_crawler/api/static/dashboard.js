let currentCollection = '';
let currentPage = 1;
const pageSize = 10;

async function fetchCollections() {
    try {
        const res = await fetch('/collections');
        const data = await res.json();
        const list = document.getElementById('collection-list');
        list.innerHTML = '';
        data.collections.forEach(col => {
            const li = document.createElement('li');
            li.className = 'collection-item';
            li.textContent = col;
            li.onclick = () => selectCollection(col);
            list.appendChild(li);
        });
        if (data.collections.length > 0 && !currentCollection) {
            selectCollection(data.collections[0]);
        }
    } catch (err) {
        console.error("Failed to fetch collections:", err);
    }
}

async function selectCollection(name) {
    currentCollection = name;
    currentPage = 1;
    document.querySelectorAll('.collection-item').forEach(el => {
        el.classList.toggle('active', el.textContent === name);
    });
    fetchData();
}

async function fetchData() {
    if (!currentCollection) return;

    const search = document.getElementById('search-input').value;
    const loader = document.getElementById('loader');
    const table = document.getElementById('data-table-container');

    loader.style.display = 'flex';
    table.style.opacity = '0.3';

    try {
        const res = await fetch(`/data/${currentCollection}?page=${currentPage}&page_size=${pageSize}&q=${search}`);
        const data = await res.json();

        renderTable(data.items);
        updatePagination(data);
    } catch (err) {
        console.error("Failed to fetch data:", err);
    } finally {
        loader.style.display = 'none';
        table.style.opacity = '1';
    }
}

function renderTable(items) {
    const head = document.getElementById('table-head');
    const body = document.getElementById('table-body');

    head.innerHTML = '';
    body.innerHTML = '';

    if (!items || items.length === 0) {
        body.innerHTML = '<tr><td colspan="5" class="text-center">No data found in this collection.</td></tr>';
        return;
    }

    const keys = Object.keys(items[0]).filter(k => k !== '_id');
    keys.forEach(key => {
        const th = document.createElement('th');
        th.textContent = key.charAt(0).toUpperCase() + key.slice(1);
        head.appendChild(th);
    });

    items.forEach(item => {
        const tr = document.createElement('tr');
        keys.forEach(key => {
            const td = document.createElement('td');
            let val = item[key];
            if (typeof val === 'object') val = JSON.stringify(val).substring(0, 50) + '...';
            td.textContent = (val === null || val === undefined) ? '' : val;
            tr.appendChild(td);
        });
        body.appendChild(tr);
    });
}

function updatePagination(data) {
    document.getElementById('page-info').textContent = `Page ${data.page} of ${data.total_pages}`;
    document.getElementById('prev-btn').disabled = data.page <= 1;
    document.getElementById('next-btn').disabled = data.page >= data.total_pages;
}

document.getElementById('prev-btn').onclick = () => {
    if (currentPage > 1) {
        currentPage--;
        fetchData();
    }
};

document.getElementById('next-btn').onclick = () => {
    currentPage++;
    fetchData();
};

let searchTimeout;
document.getElementById('search-input').oninput = () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        currentPage = 1;
        fetchData();
    }, 500);
};

// Initial Load
fetchCollections();
