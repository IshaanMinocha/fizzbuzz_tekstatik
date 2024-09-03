import json
import re

def identify_api_vulnerabilities(json_input):
    # List of common API paths that are often vulnerable
    api_paths = ['/api/v1/', '/api/v1/users', '/api/v1/admin', '/api/v1/login', '/api/v1/logout', '/api/v1/register', '/api/v1/reset-password', '/api/v1/verify',
                 '/api/v1/profile', '/api/v1/data', '/api/v1/transactions', '/api/v1/settings', '/api/v1/upload', '/api/v1/download', '/api/v1/report',
                 '/api/v1/admin/settings', '/api/v1/admin/users', '/api/v1/admin/logs', '/api/v1/admin/backup', '/api/v1/admin/database', '/api/v1/admin/reset',
                 '/api/v1/admin/permissions', '/api/v1/products', '/api/v1/orders', '/api/v1/register', '/api/v2/products', '/api/v2/orders', '/api/v2/login',
                 '/api/v2/register', '/api/v2/logout','/admin', '/dashboard', '/settings', '/profile', '/search', '/notifications']

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

# Get JSON input from the user
json_input = input("Enter the JSON input:")

# Identifying vulnerabilities
vulnerabilities_found = identify_api_vulnerabilities(json_input)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
