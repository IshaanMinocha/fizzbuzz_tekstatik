function inspectDOM() {
    let vulnerabilities = [];
  
    const scripts = document.querySelectorAll("script[unsafe-inline]");
    if (scripts.length > 0) {
      vulnerabilities.push({
        type: "Unsafe Inline Script",
        description: "Unsafe inline scripts found in the DOM.",
        elements: Array.from(scripts).map(script => script.outerHTML)
      });
    }
  
    if (vulnerabilities.length > 0) {
      chrome.storage.local.get({ vulnerabilities: [] }, function(result) {
        const updatedVulnerabilities = result.vulnerabilities.concat(vulnerabilities);
        chrome.storage.local.set({ vulnerabilities: updatedVulnerabilities });
      });
    }
  }
  
  inspectDOM();
  