/**
 * Global Toast Notification System
 * Usage: showToast('Message here', 'success' | 'error' | 'info' | 'warning')
 */

function showToast(message, type = "success") {
  let container = document.getElementById("toast-container");

  // Create container if it doesn't exist (safety check)
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;

  // Icons based on type
  let icon = "";
  switch (type) {
    case "success":
      icon = "✅";
      break; // Or use SVG
    case "error":
      icon = "⚠️";
      break;
    case "info":
      icon = "ℹ️";
      break;
    case "warning":
      icon = "🔔";
      break;
    default:
      icon = "";
  }

  // Allow HTML in message if needed, or stick to textContent for safety
  toast.innerHTML = `
        <div class="toast-icon">${icon}</div>
        <p class="toast-message">${message}</p>
    `;

  container.appendChild(toast);

  // Trigger animation
  requestAnimationFrame(() => {
    toast.classList.add("show");
  });

  // Remove after 3 seconds
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => {
      if (container.contains(toast)) {
        container.removeChild(toast);
      }
    }, 300);
  }, 3000);
}

// Check for URL parameters for messages (e.g. ?message=Login+required)
document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const message = urlParams.get("message");
  const type = urlParams.get("type") || "info"; // Support ?type=error
  if (message) {
    showToast(message, type);

    // Clean up URL without reload
    const newUrl = window.location.pathname;
    window.history.replaceState({}, document.title, newUrl);
  }
});
