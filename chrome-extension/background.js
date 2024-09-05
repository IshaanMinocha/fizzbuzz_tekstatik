// Listen for when the extension's popup is opened
chrome.action.onClicked.addListener((tab) => {
  // Send a message to the content script to highlight input fields
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content-script.js']
  });
});

// Optional: Listen for updates in storage and handle them
chrome.storage.onChanged.addListener(function(changes, area) {
  if (area === 'local') {
    console.log('Storage updated:', changes);
  }
});

// Example function to clear vulnerabilities from storage
function clearVulnerabilities() {
  chrome.storage.local.set({ vulnerabilities: [] }, function() {
    console.log('Vulnerabilities cleared');
  });
}

// Listen for commands from the popup or other parts of the extension
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.command === 'clearVulnerabilities') {
    clearVulnerabilities();
    sendResponse({ status: 'success' });
  }
});

let backendUrl = '';

fetch(chrome.runtime.getURL('config.json'))
  .then(response => response.json())
  .then(config => {
    backendUrl = config.BACKEND_URL;
    console.log('Backend URL:', backendUrl);
  })
  .catch(error => console.error('Error loading config:', error));
