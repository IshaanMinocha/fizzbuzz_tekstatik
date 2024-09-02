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

document.getElementById("fuzzBtn").addEventListener('click', function() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        let activeTab = tabs[0].id;
        chrome.tabs.sendMessage(activeTab, { action:"fuzz"});
    });
})

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


function injectNetworkLogger() {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();

    entries.forEach(entry => {
      if (entry.initiatorType === 'xmlhttprequest') {
        chrome.runtime.sendMessage({
          type: 'xmlhttprequest',
          url: entry.name,
          initiatorType: entry.initiatorType,
          status : entry.responseStatus
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
        initiatorType: entry.initiatorType,
        status : entry.responseStatus
      });
    }
  });
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if(message.action === "fuzzResponse") {
    console.log(message)
    document.getElementById("fuzzLink").innerHTML = message.link;  
  }
})

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'xmlhttprequest' && message.status !== 0) {  
    const tableBody = document.querySelector('#requestsTable tbody');
    if (tableBody) {
      const row = document.createElement('tr');
      const requestCell = document.createElement('td');
      const typeCell = document.createElement('td');
      const link = document.createElement('a');
      const statusCell = document.createElement('td');
      link.href = message.url;
      link.textContent = message.url;
      link.target = '_blank';
      link.title = message.url;
      requestCell.appendChild(link);
      statusCell.textContent = message.status;
      typeCell.textContent = message.initiatorType;

      row.appendChild(requestCell);
      row.appendChild(typeCell);
      row.appendChild(statusCell);
      tableBody.appendChild(row);
    }
  }
});
