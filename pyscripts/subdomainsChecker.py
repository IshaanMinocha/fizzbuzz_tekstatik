import json
import re
import requests

def identify_subdomain_vulnerabilities(json_input):
    # Expanded list of common vulnerable subdomains
    vulnerable_subdomains = [
        'admin', 'test', 'dev', 'staging', 'backup', 'old', 'legacy',
        'api', 'cms', 'db', 'config', 'shop', 'mail', 'ftp', 'webmail',
        'docs', 'portal', 'secure', 'login', 'register', 'profile',
        'support', 'store', 'billing', 'manager', 'stats', 'review', 'internal',
        'app', 'mobile', 'dashboard', 'reports', 'analytics', 'testing', 'sandbox',
        'news', 'events', 'forum', 'wiki', 'community', 'docs', 'files', 'media',
        'resources', 'server', 'uat', 'devops', 'ops', 'monitoring', 'tools',
        'notifications', 'api-v1', 'api-v2', 'api-dev', 'api-test', 'api-stage', 'www',
        'blog', 'test', 'shop', 'images', 'static', 'admin-panel', 'user'
    ]

    # Status codes to check
    status_code_checks = {
        200: 'Sensitive information exposure',
        403: 'Restricted area - potential misconfiguration',
        404: 'Not found - potential orphaned subdomain',
        500: 'Server misconfiguration or error'
    }

    vulnerabilities = []

    # Load the JSON input
    data = json.loads(json_input)

    # Analyzing each entry in the JSON data
    for entry in data:
        subdomain = entry.get('subdomain', '')
        status = entry.get('status')
        url = entry.get('url', '')

        # Check for common vulnerable subdomains
        if any(vuln_subdomain in subdomain for vuln_subdomain in vulnerable_subdomains):
            vulnerabilities.append({
                'vulnerability': 'Common Vulnerable Subdomain',
                'severity': 'High',
                'location': f'Subdomain: {subdomain}',
                'url': url
            })

        # Check for status code vulnerabilities
        if status in status_code_checks:
            vulnerabilities.append({
                'vulnerability': status_code_checks[status],
                'severity': 'High' if status == 200 else 'Medium',
                'location': f'Subdomain: {subdomain}',
                'url': url
            })

    return vulnerabilities

# Sample JSON input
json_input = '''
[
  {
    "subdomain": "admin.example.com",
    "status": 200,
    "url": "http://admin.example.com"
  },
  {
    "subdomain": "test.example.com",
    "status": 403,
    "url": "http://test.example.com"
  },
  {
    "subdomain": "ftp.example.com",
    "status": 404,
    "url": "http://ftp.example.com"
  },
  {
    "subdomain": "old.example.com",
    "status": 500,
    "url": "http://old.example.com"
  },
  {
    "subdomain": "api.example.com",
    "status": 200,
    "url": "http://api.example.com"
  },
  {
    "subdomain": "support.example.com",
    "status": 403,
    "url": "http://support.example.com"
  }
]
'''

# Identifying vulnerabilities
vulnerabilities_found = identify_subdomain_vulnerabilities(json_input)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
