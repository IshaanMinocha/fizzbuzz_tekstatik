document.addEventListener('DOMContentLoaded', function() {
  chrome.storage.local.get('vulnerabilities', function(data) {
    const reportDiv = document.getElementById('report');
    
    if (data.vulnerabilities && data.vulnerabilities.length > 0) {
      data.vulnerabilities.forEach(vuln => {
        const vulnElement = document.createElement('div');
        vulnElement.classList.add('vuln-item');
        vulnElement.innerHTML = `
          <h3>${vuln.type}</h3>
          <p>${vuln.description}</p>
          <p><strong>Location:</strong> ${vuln.url || vuln.elements}</p>
        `;
        reportDiv.appendChild(vulnElement);
      });
    } else {
      reportDiv.innerHTML = '<p>No vulnerabilities found.</p>';
    }
  });
});
