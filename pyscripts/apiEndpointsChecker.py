import json
import re

def identify_api_vulnerabilities(json_input):
    # List of common API paths that are often vulnerable
    api_paths = [
        '/api/v1/', '/api/v1/users', '/api/v1/admin', '/api/v1/login', '/api/v1/logout',
        '/api/v1/register', '/api/v1/reset-password', '/api/v1/verify', '/api/v1/profile',
        '/api/v1/data', '/api/v1/transactions', '/api/v1/settings', '/api/v1/upload',
        '/api/v1/download', '/api/v1/report', '/api/v1/admin/settings', '/api/v1/admin/users',
        '/api/v1/admin/logs', '/api/v1/admin/backup', '/api/v1/admin/database',
        '/api/v1/admin/reset', '/api/v1/admin/permissions',
        # Add more paths if needed
    ]

    # Regular expressions for identifying potential vulnerabilities
    sql_injection_patterns = [
        r"'.*--",
        r"union.*select",
        r"insert.*into",
        r"delete.*from",
        r"drop.*table"
    ]

    xss_patterns = [
        r"<script>",
        r"javascript:",
        r"onerror=",
        r"onload="
    ]

    vulnerabilities = []

    # Load the JSON input
    data = json.loads(json_input)

    # Analyzing each entry in the JSON data
    for entry in data:
        path = entry.get('path', '')
        status = entry.get('status')
        url = entry.get('url', '')
        headers = entry.get('headers', {})

        # Check for exposed API paths
        if any(api_path in path for api_path in api_paths):
            vulnerabilities.append({
                'vulnerability': 'Exposed or Misconfigured API Endpoint',
                'severity': 'High',
                'location': f'API Endpoint: {path}',
                'url': url
            })

        # Check for status code vulnerabilities
        if status == 200 and any(api_path in path for api_path in api_paths):
            vulnerabilities.append({
                'vulnerability': 'Sensitive data exposure in API endpoint',
                'severity': 'High',
                'location': f'Accessible API Endpoint: {path}',
                'url': url
            })
        elif status == 403 and any(api_path in path for api_path in api_paths):
            vulnerabilities.append({
                'vulnerability': 'Restricted API endpoint - potential misconfiguration',
                'severity': 'Medium',
                'location': f'Restricted API Endpoint: {path}',
                'url': url
            })
        elif status == 500:
            vulnerabilities.append({
                'vulnerability': 'Server Misconfiguration or Error in API Endpoint',
                'severity': 'Medium',
                'location': f'Path causing server error: {path}',
                'url': url
            })

        # Check for Server Information Exposure
        if 'server' in headers:
            vulnerabilities.append({
                'vulnerability': 'Server Information Exposure',
                'severity': 'Low',
                'location': f'Server Header: {headers["server"]}',
                'url': url
            })

        # Check for SQL Injection vulnerabilities
        for pattern in sql_injection_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                vulnerabilities.append({
                    'vulnerability': 'Potential SQL Injection',
                    'severity': 'High',
                    'location': f'Path: {path}',
                    'url': url
                })
                break

        # Check for XSS vulnerabilities
        for pattern in xss_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                vulnerabilities.append({
                    'vulnerability': 'Potential Cross-Site Scripting (XSS)',
                    'severity': 'High',
                    'location': f'Path: {path}',
                    'url': url
                })
                break

        # Check for potential directory traversal
        if '..' in path:
            vulnerabilities.append({
                'vulnerability': 'Potential Directory Traversal',
                'severity': 'High',
                'location': f'Path: {path}',
                'url': url
            })

    return vulnerabilities

# Sample JSON input
json_input = '''
[
  {
    "path": "/api/v1/admin/users",
    "status": 200,
    "size": 54321,
    "words": 234,
    "lines": 12,
    "duration": "0.234s",
    "url": "http://example.com/api/v1/admin/users",
    "headers": {
      "server": "Apache/2.4.41"
    }
  },
  {
    "path": "/api/v1/login?user=admin'--",
    "status": 500,
    "size": 67890,
    "words": 456,
    "lines": 20,
    "duration": "0.456s",
    "url": "http://example.com/api/v1/login?user=admin'--",
    "headers": {
      "server": "nginx/1.18.0"
    }
  },
  {
    "path": "/api/v1/profile?callback=<script>alert('XSS')</script>",
    "status": 200,
    "size": 5678,
    "words": 123,
    "lines": 5,
    "duration": "0.234s",
    "url": "http://example.com/api/v1/profile?callback=<script>alert('XSS')</script>",
    "headers": {
      "server": "Apache"
    }
  },
  {
    "path": "/api/v1/reset-password",
    "status": 403,
    "size": 1234,
    "words": 10,
    "lines": 2,
    "duration": "0.345s",
    "url": "http://example.com/api/v1/reset-password",
    "headers": {
      "server": "nginx"
    }
  },
  {
    "path": "/../../etc/passwd",
    "status": 403,
    "size": 1234,
    "words": 10,
    "lines": 2,
    "duration": "0.345s",
    "url": "http://example.com/../../etc/passwd",
    "headers": {
      "server": "Apache"
    }
  }
]
'''

# Identifying vulnerabilities
vulnerabilities_found = identify_api_vulnerabilities(json_input)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
