let currentCollection = "";
let currentPage = 1;
const pageSize = 10;

async function fetchAllCollections() {
  try {
    const projectListSidebar = document.getElementById("project-list-sidebar");

    // Only keep the "# All Projects" item in sidebar
    projectListSidebar.innerHTML =
      '<li class="collection-item active" id="btn-projects-view"># All Projects</li>';
    document.getElementById("btn-projects-view").onclick = () =>
      showView("projects-view");

    // By default, if no active collection, show the projects view
    if (!currentCollection) {
      showView("projects-view");
    }
  } catch (err) {
    console.error("Failed to initialize dashboard:", err);
  }
}

async function selectCollection(collectionName, displayName) {
  currentCollection = collectionName;
  currentPage = 1;
  showView("data-view");
  document.querySelectorAll(".collection-item").forEach((el) => {
    el.classList.toggle("active", el.dataset.collection === collectionName);
  });
  fetchData();
}

async function fetchData() {
  if (!currentCollection) return;

  const search = document.getElementById("search-input").value;
  const loader = document.getElementById("loader");
  const table = document.getElementById("data-table-container");

  loader.style.display = "flex";
  table.style.opacity = "0.3";

  try {
    const res = await fetch(
      `/data/${currentCollection}?page=${currentPage}&page_size=${pageSize}&q=${search}`,
    );
    const data = await res.json();

    renderTable(data.items);
    updatePagination(data);
  } catch (err) {
    console.error("Failed to fetch data:", err);
  } finally {
    loader.style.display = "none";
    table.style.opacity = "1";
  }
}

function renderTable(items) {
  const head = document.getElementById("table-head");
  const body = document.getElementById("table-body");

  head.innerHTML = "";
  body.innerHTML = "";

  if (!items || items.length === 0) {
    body.innerHTML =
      '<tr><td colspan="5" class="text-center">No data found in this collection.</td></tr>';
    return;
  }

  const keys = Object.keys(items[0]).filter((k) => k !== "_id");
  keys.forEach((key) => {
    const th = document.createElement("th");
    th.textContent = key.charAt(0).toUpperCase() + key.slice(1);
    head.appendChild(th);
  });

  items.forEach((item) => {
    const tr = document.createElement("tr");
    keys.forEach((key) => {
      const td = document.createElement("td");
      let val = item[key];
      if (typeof val === "object")
        val = JSON.stringify(val).substring(0, 50) + "...";
      td.textContent = val === null || val === undefined ? "" : val;
      tr.appendChild(td);
    });
    body.appendChild(tr);
  });
}

function updatePagination(data) {
  document.getElementById("page-info").textContent =
    `Page ${data.page} of ${data.total_pages}`;
  document.getElementById("prev-btn").disabled = data.page <= 1;
  document.getElementById("next-btn").disabled = data.page >= data.total_pages;
}

document.getElementById("prev-btn").onclick = () => {
  if (currentPage > 1) {
    currentPage--;
    fetchData();
  }
};

document.getElementById("next-btn").onclick = () => {
  currentPage++;
  fetchData();
};

let searchTimeout;
document.getElementById("search-input").oninput = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    currentPage = 1;
    fetchData();
  }, 500);
};

// --- View Switching ---
function showView(viewId) {
  document.getElementById("data-view").style.display =
    viewId === "data-view" ? "block" : "none";
  document.getElementById("projects-view").style.display =
    viewId === "projects-view" ? "block" : "none";

  // Inactive all sidebar items
  document
    .querySelectorAll(".collection-item")
    .forEach((el) => el.classList.remove("active"));

  if (viewId === "projects-view") {
    document.getElementById("btn-projects-view").classList.add("active");
    loadProjects();
  }
}

document.getElementById("btn-projects-view").onclick = () =>
  showView("projects-view");

// --- Project Management ---
const projectModal = document.getElementById("project-modal");
const newProjectBtn = document.getElementById("new-project-btn");
const closeProjectModal = document.getElementById("close-project-modal");
const projectForm = document.getElementById("project-form");

if (newProjectBtn) {
  newProjectBtn.onclick = () => {
    projectModal.style.display = "block";
  };
}

if (closeProjectModal) {
  closeProjectModal.onclick = () => {
    projectModal.style.display = "none";
  };
}

window.onclick = (event) => {
  if (event.target == projectModal) {
    projectModal.style.display = "none";
  }
};

if (projectForm) {
  projectForm.onsubmit = async (e) => {
    e.preventDefault();

    const payload = {
      name: document.getElementById("proj-name").value,
      urls: document.getElementById("proj-urls").value,
      data_type: document.getElementById("proj-data-type").value,
      output_format: document.getElementById("proj-format").value,
      project_type: document.getElementById("proj-type").value,
      description: "",
    };

    try {
      const res = await fetch("/api/projects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        showToast("Project created successfully!", "success");
        projectModal.style.display = "none";
        projectForm.reset();
        loadProjects();
      } else {
        const err = await res.json();
        showToast(
          "Error: " + (err.detail || "Failed to create project"),
          "error",
        );
      }
    } catch (err) {
      console.error("Project creation error:", err);
      showToast("An unexpected error occurred", "error");
    }
  };
}

async function loadProjects() {
  const tableBody = document.getElementById("projects-table-body");

  // Show skeleton loaders
  tableBody.innerHTML = "";
  for (let i = 0; i < 3; i++) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
            <td><div class="skeleton" style="height: 20px; width: 150px; margin-bottom: 8px;"></div><div class="skeleton" style="height: 12px; width: 80px;"></div></td>
            <td><div class="skeleton" style="height: 24px; width: 100px; border-radius: 9999px;"></div></td>
            <td><div class="skeleton" style="height: 16px; width: 120px; margin-bottom: 4px;"></div><div class="skeleton" style="height: 12px; width: 60px;"></div></td>
            <td><div class="skeleton" style="height: 16px; width: 100px;"></div></td>
            <td style="text-align: right;"><div class="skeleton" style="height: 36px; width: 100px; border-radius: 6px;"></div></td>
        `;
    tableBody.appendChild(tr);
  }

  try {
    const res = await fetch("/api/projects");
    const projects = await res.json();

    // Calculate Stats
    const total = projects.length;
    const processing = projects.filter((p) => p.status === "Processing").length;
    const completed = projects.filter((p) => p.status === "Completed").length;
    const successRate = total > 0 ? Math.round((completed / total) * 100) : 0;

    document.getElementById("stat-total-projects").textContent = total;
    document.getElementById("stat-running-projects").textContent = processing;
    document.getElementById("stat-success-rate").textContent =
      `${successRate}%`;

    tableBody.innerHTML = "";
    if (projects.length === 0) {
      tableBody.innerHTML =
        '<tr><td colspan="5" class="text-center" style="padding: 3.5rem; color: #64748b;">No projects found. Create one to get started!</td></tr>';
      return;
    }

    projects.forEach((proj) => {
      const tr = document.createElement("tr");

      // Status Badge Class
      let statusClass = "status-pill status-pending";
      if (proj.status === "Completed")
        statusClass = "status-pill status-completed";
      else if (proj.status === "Processing")
        statusClass = "status-pill status-processing";
      else if (proj.status === "Failed")
        statusClass = "status-pill status-failed";

      tr.innerHTML = `
                <td>
                    <span class="project-name">${proj.name}</span>
                    <span class="project-meta">ID: #${proj.id}</span>
                </td>
                <td><span class="${statusClass}">${proj.status}</span></td>
                <td>
                    <div style="font-weight: 500;">${proj.data_type}</div>
                    <div style="font-size: 0.75rem; color: #64748b;">${proj.project_type} • ${proj.output_format}</div>
                </td>
                <td>
                    <div style="font-weight: 500;">${new Date(proj.created_at).toLocaleDateString()}</div>
                    <div style="font-size: 0.75rem; color: #64748b;">${new Date(proj.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</div>
                </td>
                <td style="text-align: right;">
                    ${
                      proj.status === "Completed"
                        ? `<button class="action-btn" onclick="selectCollection('${proj.mongo_collection}', '${proj.name}')">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                            View Data
                        </button>`
                        : '<span style="font-size: 0.75rem; color: #94a3b8; font-weight: 500; padding-right: 1rem;">Work in progress...</span>'
                    }
                </td>
            `;
      tableBody.appendChild(tr);
    });
  } catch (err) {
    console.error("Failed to load projects:", err);
    tableBody.innerHTML =
      '<tr><td colspan="5" class="text-center" style="color: #ef4444; padding: 2rem;">Error loading projects. Please try again.</td></tr>';
  }
}

// Helper to show toast (matching existing site style)
function showToast(message, type = "success") {
  if (window.showToast) {
    window.showToast(message, type);
  } else {
    alert(message);
  }
}

// Initial Load
fetchAllCollections();

// --- Mobile Sidebar Toggle ---
const sidebarToggle = document.getElementById("sidebar-toggle");
const sidebar = document.getElementById("dashboard-sidebar");

if (sidebarToggle && sidebar) {
  sidebarToggle.onclick = () => {
    sidebar.classList.toggle("active");
  };

  // Close sidebar when clicking outside on mobile
  document.addEventListener("click", (e) => {
    if (window.innerWidth <= 768) {
      if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
        sidebar.classList.remove("active");
      }
    }
  });

  // Close sidebar when selecting a collection or project view on mobile
  document.addEventListener("click", (e) => {
    if (
      window.innerWidth <= 768 &&
      (e.target.classList.contains("collection-item") ||
        e.target.id === "btn-projects-view")
    ) {
      sidebar.classList.remove("active");
    }
  });
}

// --- File Upload ---
const uploadBtn = document.getElementById("upload-btn");
const fileInput = document.getElementById("file-upload");

if (uploadBtn) {
  uploadBtn.onclick = () => {
    fileInput.click();
  };
}

if (fileInput) {
  fileInput.onchange = async () => {
    if (fileInput.files.length === 0) return;

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const loader = document.getElementById("loader");
    loader.style.display = "flex";
    document.getElementById("data-table-container").style.opacity = "0.3";

    try {
      const res = await fetch("/datasets/upload", {
        method: "POST",
        body: formData,
        credentials: "include",
      });
      const data = await res.json();

      if (res.ok) {
        showToast(`Success: ${data.message}`);
        await fetchAllCollections();
        if (data.datasets && data.datasets.length > 0) {
          selectCollection(
            data.datasets[0].collection_name,
            data.datasets[0].filename,
          );
        } else if (data.collection_name) {
          selectCollection(
            data.collection_name,
            data.filename || data.collection_name,
          );
        }
      } else {
        if (res.status === 401) {
          showToast("Session expired. Please log in.", "error");
          window.location.href = "/login";
          return;
        }
        showToast(`Error: ${data.detail || "Upload failed"}`, "error");
      }
    } catch (err) {
      console.error("Upload error:", err);
      showToast("Unexpected error during upload", "error");
    } finally {
      loader.style.display = "none";
      document.getElementById("data-table-container").style.opacity = "1";
      fileInput.value = "";
    }
  };
}
