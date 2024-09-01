import json
import re

def identify_hidden_directory_vulnerabilities(json_input):
    # List of hidden or sensitive directories that signify high-risk vulnerabilities
    hidden_directories = [
        '/.git/', '/.svn/', '/CVS/', '/.env', '/.htaccess', '/.htpasswd', '/.gitignore',
        '/.idea/', '/.vscode/', '/.config/', '/.well-known/', '/.DS_Store', '/.metadata',
        '/backup/', '/old/', '/temp/', '/tmp/', '/logs/', '/private/', '/secure/',
        '/test/', '/staging/', '/dev/', '/debug/', '/config/', '/admin/', '/hidden/',
        '/secret/', '/assets/', '/uploads/', '/files/', '/archive/', '/bkp/', '/dump/',
        '/debug.log', '/error.log', '/access.log', '/.backup', '/backup.zip', '/.bak',
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
        response_body = entry.get('response_body', '')
        headers = entry.get('headers', {})

        # Check for hidden directories
        if any(hidden_dir in path for hidden_dir in hidden_directories):
            vulnerabilities.append({
                'vulnerability': 'Exposed hidden or sensitive directory',
                'severity': 'High',
                'location': f'Hidden Directory: {path}',
                'url': url
            })

        # Check for status code vulnerabilities
        if status == 200 and any(hidden_dir in path for hidden_dir in hidden_directories):
            vulnerabilities.append({
                'vulnerability': 'Sensitive information exposure in hidden directory',
                'severity': 'High',
                'location': f'Accessible Hidden Directory: {path}',
                'url': url
            })
        elif status == 403 and any(hidden_dir in path for hidden_dir in hidden_directories):
            vulnerabilities.append({
                'vulnerability': 'Restricted hidden directory - potential misconfiguration',
                'severity': 'Medium',
                'location': f'Restricted Hidden Directory: {path}',
                'url': url
            })
        elif status == 500:
            vulnerabilities.append({
                'vulnerability': 'Server Misconfiguration or Error',
                'severity': 'Medium',
                'location': f'Path causing server error: {path}',
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
    "path": "/.git/config",
    "status": 200,
    "size": 54321,
    "words": 234,
    "lines": 12,
    "duration": "0.234s",
    "url": "http://example.com/.git/config"
  },
  {
    "path": "/backup.zip",
    "status": 403,
    "size": 67890,
    "words": 456,
    "lines": 20,
    "duration": "0.456s",
    "url": "http://example.com/backup.zip"
  },
  {
    "path": "/logs/error.log",
    "status": 200,
    "size": 5678,
    "words": 123,
    "lines": 5,
    "duration": "0.234s",
    "url": "http://example.com/logs/error.log"
  },
  {
    "path": "/.env",
    "status": 403,
    "size": 1234,
    "words": 10,
    "lines": 2,
    "duration": "0.345s",
    "url": "http://example.com/.env"
  },
  {
    "path": "/../../etc/passwd",
    "status": 403,
    "size": 1234,
    "words": 10,
    "lines": 2,
    "duration": "0.345s",
    "url": "http://example.com/../../etc/passwd"
  }
]
'''

# Identifying vulnerabilities
vulnerabilities_found = identify_hidden_directory_vulnerabilities(json_input)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
