document.getElementById('highlightBtn').addEventListener('click', function() {

  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      function: highlightRequestGeneratingElements
    });
  });
});



// Function to highlight elements likely to generate GET, PUT, POST, or DELETE requests
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

