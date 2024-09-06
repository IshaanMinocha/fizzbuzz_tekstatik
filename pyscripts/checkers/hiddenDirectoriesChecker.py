import os
import json
import re

def identify_hidden_directory_vulnerabilities(json_input):
    # Hardcoded payload lists for each status code
    payloads_by_status = {
        '200': [
            '/admin', '/dashboard', '/settings', '/profile', '/api/v1/users', '/api/v1/logout',
            '/api/v1/orders', '/notifications', '/api/v1/register', '/api/v1/login', '/api/v1/products'
        ],
        '301': [
            '/admin'
        ],
        '401': [
            '/admin', '/dashboard', '/settings', '/profile', '/api/v1/users'
        ],
        '403': [
            '/admin', '/dashboard', '/settings', '/profile'
        ],
        '404': [
            '/search', '/dashboard', '/settings', '/profile', '/api/v1/orders', '/notifications',
            '/api/v2/users', '/api/v2/logout', '/api/v2/register', '/api/v2/login', '/api/v2/products',
            '/hidden', '/backup', '/old', '/private', '/.git', '/.env'
        ],
        '405': [
            '/api/v1/products', '/api/v2/products'
        ],
        '429': [
            '/admin', '/api/v1/orders'
        ],
        '500': [
            '/api/v1/login'
        ],
        '502': [
            '/api/v1/logout'
        ],
        '503': [
            '/search'
        ]
    }

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
    for entry in data.get('output', []):
        payload = entry.get('payload', '')
        response = entry.get('response')
        _id = entry.get('_id', {}).get('$oid', '')
        lines = entry.get('lines', 0)
        words = entry.get('words', 0)
        chars = entry.get('chars', 0)

        # Check if the payload matches any known hidden directories
        if any(payload.startswith(item) for item in payloads_by_status.get(response, [])):
            if response in ['200', '301']:
                vulnerabilities.append({
                    'vulnerability': 'Sensitive data exposure or potential misconfiguration',
                    'severity': 'High',
                    'location': f'Path: {payload}',
                    'id': _id,
                    'lines': lines,
                    'words': words,
                    'chars': chars
                })
            elif response in ['403']:
                vulnerabilities.append({
                    'vulnerability': 'Restricted or potentially misconfigured directory',
                    'severity': 'Medium',
                    'location': f'Path: {payload}',
                    'id': _id,
                    'lines': lines,
                    'words': words,
                    'chars': chars
                })
            elif response in ['404', '405']:
                vulnerabilities.append({
                    'vulnerability': 'Endpoint Enumeration or method tampering',
                    'severity': 'Medium',
                    'location': f'Path: {payload}',
                    'id': _id,
                    'lines': lines,
                    'words': words,
                    'chars': chars
                })
            elif response in ['429', '500', '502', '503']:
                vulnerabilities.append({
                    'vulnerability': 'Server error or service unavailability',
                    'severity': 'Low',
                    'location': f'Path: {payload}',
                    'id': _id,
                    'lines': lines,
                    'words': words,
                    'chars': chars
                })

        # Check for potential SQL Injection vulnerabilities
        for pattern in sql_injection_patterns:
            if re.search(pattern, payload, re.IGNORECASE):
                vulnerabilities.append({
                    'vulnerability': 'Potential SQL Injection',
                    'severity': 'High',
                    'location': f'Path: {payload}',
                    'id': _id,
                    'lines': lines,
                    'words': words,
                    'chars': chars
                })
                break

        # Check for potential XSS vulnerabilities
        for pattern in xss_patterns:
            if re.search(pattern, payload, re.IGNORECASE):
                vulnerabilities.append({
                    'vulnerability': 'Potential Cross-Site Scripting (XSS)',
                    'severity': 'High',
                    'location': f'Path: {payload}',
                    'id': _id,
                    'lines': lines,
                    'words': words,
                    'chars': chars
                })
                break

        # Check for potential directory traversal
        if '..' in payload:
            vulnerabilities.append({
                'vulnerability': 'Potential Directory Traversal',
                'severity': 'High',
                'location': f'Path: {payload}',
                'id': _id,
                'lines': lines,
                'words': words,
                'chars': chars
            })

    return {
        "targetUrl": data.get("targetUrl", ""),
        "fuzzType": data.get("fuzzType", ""),
        "vulnerabilities": vulnerabilities
    }

# Read JSON data from file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

# Path to the JSON input file
json_file_path = os.path.join(os.path.dirname(__file__), 'vulnerabilities.json')

# Read the JSON input
json_input = read_json_file(json_file_path)

if json_input:
    # Identifying vulnerabilities
    vulnerabilities_found = identify_hidden_directory_vulnerabilities(json_input)

    # Convert vulnerabilities to JSON format
    vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

    # Print the JSON output
    print(vulnerabilities_json)
