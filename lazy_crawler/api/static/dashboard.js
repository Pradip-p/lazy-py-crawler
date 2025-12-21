let currentCollection = '';
let currentPage = 1;
const pageSize = 10;

async function fetchAllCollections() {
    try {
        // Fetch scraped collections
        const resCol = await fetch('/collections');
        const dataCol = await resCol.json();

        // Fetch user uploads
        const resUp = await fetch('/datasets/list', {
            credentials: 'include'
        });
        const dataUp = await resUp.json();

        const uploadsList = document.getElementById('uploads-list');
        const collectionList = document.getElementById('collection-list');

        uploadsList.innerHTML = '';
        collectionList.innerHTML = '';

        // Render Uploads
        dataUp.forEach(dataset => {
            const li = document.createElement('li');
            li.className = 'collection-item';
            li.textContent = dataset.filename;
            li.dataset.collection = dataset.mongo_collection_name;
            li.onclick = () => selectCollection(dataset.mongo_collection_name, dataset.filename);
            uploadsList.appendChild(li);
        });

        // Render Scraped Collections
        dataCol.collections.forEach(col => {
            const li = document.createElement('li');
            li.className = 'collection-item';
            li.textContent = col;
            li.dataset.collection = col;
            li.onclick = () => selectCollection(col, col);
            collectionList.appendChild(li);
        });

        if (!currentCollection) {
            if (dataUp.length > 0) {
                selectCollection(dataUp[0].mongo_collection_name, dataUp[0].filename);
            } else if (dataCol.collections.length > 0) {
                selectCollection(dataCol.collections[0], dataCol.collections[0]);
            }
        }
    } catch (err) {
        console.error("Failed to fetch collections:", err);
    }
}

async function selectCollection(collectionName, displayName) {
    currentCollection = collectionName;
    currentPage = 1;
    document.querySelectorAll('.collection-item').forEach(el => {
        el.classList.toggle('active', el.dataset.collection === collectionName);
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
fetchAllCollections();

// --- Mobile Sidebar Toggle ---
const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebar = document.getElementById('dashboard-sidebar');

if (sidebarToggle && sidebar) {
    sidebarToggle.onclick = () => {
        sidebar.classList.toggle('active');
    };

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        }
    });

    // Close sidebar when selecting a collection on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && e.target.classList.contains('collection-item')) {
            sidebar.classList.remove('active');
        }
    });
}

// --- File Upload ---
const uploadBtn = document.getElementById('upload-btn');
const fileInput = document.getElementById('file-upload');

uploadBtn.onclick = () => {
    fileInput.click();
};

fileInput.onchange = async () => {
    if (fileInput.files.length === 0) return;

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const loader = document.getElementById('loader');
    loader.style.display = 'flex';
    document.getElementById('data-table-container').style.opacity = '0.3';

    try {
        const res = await fetch('/datasets/upload', {
            method: 'POST',
            body: formData,
            credentials: 'include'  // Include cookies for authentication
        });
        const data = await res.json();

        if (res.ok) {
            alert(`Success: ${data.message}`);
            // Refresh collections
            await fetchAllCollections();
            // Select the new collection (first sheet if multiple)
            if (data.datasets && data.datasets.length > 0) {
                selectCollection(data.datasets[0].collection_name, data.datasets[0].filename);
            } else if (data.collection_name) {
                selectCollection(data.collection_name, data.filename || data.collection_name);
            }
        } else {
            // Check for authentication error
            if (res.status === 401) {
                alert('Your session has expired. Please log in again.');
                window.location.href = '/login';
                return;
            }
            alert(`Error: ${data.detail || "Upload failed"}`);
        }
    } catch (err) {
        console.error("Upload error:", err);
        alert("An unexpected error has occurred. Please check your connection and try again.");
    } finally {
        loader.style.display = 'none';
        document.getElementById('data-table-container').style.opacity = '1';
        fileInput.value = ''; // Reset input
    }
};

// --- AI Features ---
const chatToggleBtn = document.getElementById('chat-toggle-btn');
const chatWindow = document.getElementById('chat-window');
const closeChatBtn = document.getElementById('close-chat');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');
const aiModelSelector = document.getElementById('ai-model-selector');
const ollamaSettings = document.getElementById('ollama-settings');
const ollamaTemperature = document.getElementById('ollama-temperature');
const temperatureValue = document.getElementById('temperature-value');
const ollamaStreaming = document.getElementById('ollama-streaming');
const checkOllamaHealthBtn = document.getElementById('check-ollama-health');
const chatStatus = document.getElementById('chat-status');
const chatSubmitBtn = document.getElementById('chat-submit-btn');

const visualizeBtn = document.getElementById('visualize-btn');
const chartContainer = document.getElementById('chart-container');
const closeChartBtn = document.getElementById('close-chart');
let currentChart = null;
let selectedAIModel = 'gemini';

// Update temperature display
ollamaTemperature.addEventListener('input', (e) => {
    temperatureValue.textContent = parseFloat(e.target.value).toFixed(1);
});

// AI Model Selector
aiModelSelector.addEventListener('change', (e) => {
    selectedAIModel = e.target.value;
    ollamaSettings.style.display = selectedAIModel === 'ollama' ? 'block' : 'none';
    chatStatus.textContent = '';
});

// Check Ollama Health
checkOllamaHealthBtn.onclick = async () => {
    checkOllamaHealthBtn.disabled = true;
    checkOllamaHealthBtn.textContent = '⏳...';

    try {
        const res = await fetch('/api/ai/ollama/health');
        const data = await res.json();

        if (data.healthy) {
            chatStatus.style.color = 'var(--slack-green)';
            chatStatus.textContent = '✓ Ollama is healthy and ready';
        } else {
            chatStatus.style.color = '#ff6b6b';
            chatStatus.textContent = '✗ Ollama is offline';
        }
    } catch (err) {
        chatStatus.style.color = '#ff6b6b';
        chatStatus.textContent = '✗ Cannot connect to Ollama';
    } finally {
        checkOllamaHealthBtn.disabled = false;
        checkOllamaHealthBtn.textContent = 'Check';
    }
};

// Chat UI Toggles
chatToggleBtn.onclick = () => {
    chatWindow.style.display = chatWindow.style.display === 'flex' ? 'none' : 'flex';
};
closeChatBtn.onclick = () => {
    chatWindow.style.display = 'none';
};

// Add Message to Chat
function addMessage(text, isUser = false, isStreaming = false) {
    const div = document.createElement('div');
    div.style.padding = '0.8rem';
    div.style.borderRadius = '8px';
    div.style.maxWidth = '80%';
    div.style.wordWrap = 'break-word';
    div.style.lineHeight = '1.4';

    if (isUser) {
        div.style.alignSelf = 'flex-end';
        div.style.background = 'var(--slack-blue)';
        div.style.color = 'white';
    } else {
        div.style.alignSelf = 'flex-start';
        div.style.background = '#e0e0e0';
        div.style.color = 'black';
        if (isStreaming) {
            div.id = 'streaming-message';
        }
    }
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
}

// Chat Submission with Ollama Support
chatForm.onsubmit = async (e) => {
    e.preventDefault();
    const msg = chatInput.value.trim();
    if (!msg) return;

    addMessage(msg, true);
    chatInput.value = '';
    chatSubmitBtn.disabled = true;

    const context = `User is looking at collection: ${currentCollection}. Query: ${document.getElementById('search-input').value}.`;

    try {
        if (selectedAIModel === 'ollama') {
            // Use Ollama API
            const temperature = parseFloat(ollamaTemperature.value);
            const stream = ollamaStreaming.checked;

            // Add streaming indicator
            let responseDiv = addMessage('', false);

            if (stream) {
                // Streaming response
                const res = await fetch('/api/ai/ollama/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: msg,
                        temperature: temperature,
                        stream: true
                    }),
                    credentials: 'include'
                });

                const reader = res.body.getReader();
                const decoder = new TextDecoder();
                let fullResponse = '';

                while (true) {
                    const {done, value} = await reader.read();
                    if (done) break;

                    const text = decoder.decode(value);
                    const lines = text.split('\n');

                    for (const line of lines) {
                        if (line.trim()) {
                            try {
                                const data = JSON.parse(line);
                                if (data.token) {
                                    fullResponse += data.token;
                                    responseDiv.textContent = fullResponse;
                                    chatMessages.scrollTop = chatMessages.scrollHeight;
                                } else if (data.error) {
                                    responseDiv.textContent = `Error: ${data.error}`;
                                    responseDiv.style.background = '#ffebee';
                                }
                            } catch (e) {
                                // Ignore parsing errors
                            }
                        }
                    }
                }
            } else {
                // Non-streaming response
                const res = await fetch('/api/ai/ollama/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: msg,
                        temperature: temperature,
                        stream: false
                    }),
                    credentials: 'include'
                });

                const data = await res.json();
                responseDiv.textContent = data.response || "Sorry, I couldn't process that.";
            }
        } else {
            // Use Gemini API (existing)
            const res = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg, context: context }),
                credentials: 'include'
            });
            const data = await res.json();
            addMessage(data.response || "Sorry, I couldn't process that.");
        }
    } catch (err) {
        addMessage(`Error: ${err.message || 'Failed to get response'}`);
    } finally {
        chatSubmitBtn.disabled = false;
    }
};

// Chart Visualization
visualizeBtn.onclick = async () => {
    if (!currentCollection) {
        alert("Please select a collection first.");
        return;
    }

    const description = prompt("What would you like to visualize? (e.g., 'Bar chart of prices', 'Distribution of categories')");
    if (!description) return;

    chartContainer.style.display = 'block';

    // Get visible rows data for context
    const tableBody = document.getElementById('table-body');
    const rows = Array.from(tableBody.querySelectorAll('tr'));

    if (rows.length === 0 || rows[0].cells.length <= 1) {
        alert("No data to visualize.");
        chartContainer.style.display = 'none';
        return;
    }

    // Extract headers
    const head = document.getElementById('table-head');
    const headers = Array.from(head.querySelectorAll('th')).map(th => th.textContent);

    // Extract first 10 rows of data as sample
    const sampleData = rows.slice(0, 10).map(tr => {
        const cells = Array.from(tr.querySelectorAll('td'));
        let obj = {};
        headers.forEach((h, i) => obj[h] = cells[i]?.textContent);
        return obj;
    });

    const dataSummary = `Headers: ${headers.join(', ')}. Sample Data (first 10 rows): ${JSON.stringify(sampleData)}`;

    try {
        if (selectedAIModel === 'ollama') {
            // Use Ollama to generate chart description first
            const chartDescriptionPrompt = `Based on the following data, suggest a Chart.js configuration for: "${description}"

Data Summary:
${dataSummary}

Respond ONLY with a valid JSON object following this structure (replace X with actual labels/data):
{
  "type": "bar|line|pie|doughnut",
  "data": {
    "labels": ["X", "Y", ...],
    "datasets": [{"label": "Dataset 1", "data": [X, Y, ...], "backgroundColor": ["#FF6384", ...], ...}]
  },
  "options": {"responsive": true, "plugins": {"title": {"text": "Chart Title", "display": true}}}
}`;

            const res = await fetch('/api/ai/ollama/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt: chartDescriptionPrompt,
                    temperature: 0.3,
                    stream: false
                }),
                credentials: 'include'
            });

            const data = await res.json();
            let config;

            try {
                // Extract JSON from response (in case there's extra text)
                const jsonMatch = data.response.match(/\{[\s\S]*\}/);
                config = JSON.parse(jsonMatch ? jsonMatch[0] : data.response);
            } catch (e) {
                alert("Failed to parse chart configuration from Ollama. Please try again.");
                chartContainer.style.display = 'none';
                return;
            }

            const ctx = document.getElementById('dataChart').getContext('2d');
            if (currentChart) currentChart.destroy();
            currentChart = new Chart(ctx, config);
        } else {
            // Use Gemini API (existing)
            const res = await fetch('/api/ai/chart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description: description, data_summary: dataSummary }),
                credentials: 'include'
            });
            const config = await res.json();

            if (config.error) {
                alert(config.error);
                return;
            }

            const ctx = document.getElementById('dataChart').getContext('2d');
            if (currentChart) currentChart.destroy();
            currentChart = new Chart(ctx, config);
        }

    } catch (err) {
        console.error(err);
        alert("Failed to generate chart.");
        chartContainer.style.display = 'none';
    }
};

closeChartBtn.onclick = () => {
    chartContainer.style.display = 'none';
    if (currentChart) {
        currentChart.destroy();
        currentChart = null;
    }
};
