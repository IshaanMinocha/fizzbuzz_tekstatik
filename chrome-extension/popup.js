// Popup script
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('highlightBtn').addEventListener('click', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        function: highlightRequestGeneratingElements
      });
    });
  });

  document.getElementById('logRequestsBtn').addEventListener('click', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        function: injectNetworkLogger
      });
    });
  });
});

// Function to be injected into the page
function highlightRequestGeneratingElements() {
  const elements = document.querySelectorAll('a, form, input[type="submit"], button[type="submit"], button, input[type="button"], input[type="image"]');

  elements.forEach(element => {
    const tagName = element.tagName.toLowerCase();

    if (tagName === 'a') {
      if (element.href && (element.href.startsWith('http') || element.href.startsWith('/'))) {
        element.style.border = '2px solid red';
        element.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
      }
    } else if (tagName === 'form') {
      const method = element.method.toLowerCase();
      if (['get', 'post', 'put', 'delete'].includes(method)) {
        element.style.border = '2px solid red';
        element.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
      }
    } else if (['input', 'button'].includes(tagName)) {
      const type = element.type.toLowerCase();
      if (type === 'submit' || type === 'button' || type === 'image') {
        const form = element.closest('form');
        if (form) {
          const method = form.method.toLowerCase();
          if (['get', 'post', 'put', 'delete'].includes(method)) {
            element.style.border = '2px solid red';
            element.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
          }
        } else {
          element.style.border = '2px solid red';
          element.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
        }
      }
    }
  });
}

// Function to be injected into the page
function injectNetworkLogger() {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    entries.forEach(entry => {
      if (entry.initiatorType === 'xmlhttprequest') {
        chrome.runtime.sendMessage({
          type: 'xmlhttprequest',
          url: entry.name,
          initiatorType: entry.initiatorType
        });
      }
    });
  });

  observer.observe({ entryTypes: ["resource"] });

  // Also log existing network requests (before the observer was set up)
  window.performance.getEntriesByType('resource').forEach(entry => {
    if (entry.initiatorType === 'xmlhttprequest') {
      chrome.runtime.sendMessage({
        type: 'xmlhttprequest',
        url: entry.name,
        initiatorType: entry.initiatorType
      });
    }
  });
}

// Listen for messages from the injected script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'xmlhttprequest') {
    const tableBody = document.querySelector('#requestsTable tbody');
    if (tableBody) {
      const row = document.createElement('tr');
      const requestCell = document.createElement('td');
      const typeCell = document.createElement('td');
      const link = document.createElement('a');
      link.href = message.url;
      link.textContent = message.url;
      link.target = '_blank';
      requestCell.appendChild(link);

      typeCell.textContent = message.initiatorType;

      row.appendChild(requestCell);
      row.appendChild(typeCell);
      tableBody.appendChild(row);
    }
  }
});