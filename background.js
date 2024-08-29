
chrome.storage.onChanged.addListener(function(changes, area) {
  if (area === 'local') {
    console.log('Storage updated:', changes);
  
  }
});

function clearVulnerabilities() {
  chrome.storage.local.set({ vulnerabilities: [] }, function() {
    console.log('Vulnerabilities cleared');
  });
}

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.command === 'clearVulnerabilities') {
    clearVulnerabilities();
    sendResponse({ status: 'success' });
  }
});
