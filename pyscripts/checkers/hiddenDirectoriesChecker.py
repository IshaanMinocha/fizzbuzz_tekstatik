import os
import json
import re

def identify_hidden_directory_vulnerabilities(json_input):
    # Hardcoded payload lists for each status code
    payloads_by_status = {
    '200': [
        '/admin', '/dashboard', '/settings', '/profile', '/api/v1/users', '/api/v1/logout',
        '/api/v1/orders', '/notifications', '/api/v1/register', '/api/v1/login', '/api/v1/products',
        '/api/v1/admin', '/config', '/.htaccess', '/.bash_history', '/.aws/credentials',
        '/api/v1/logs', '/backup.zip', '/debug', '/.git/config', '/phpinfo', '/status', '/env'
    ],
    '301': [
        '/admin', '/old', '/backup', '/redirect', '/moved', '/api/v1', '/secure', '/login', '/signin'
    ],
    '401': [
        '/admin', '/dashboard', '/settings', '/profile', '/api/v1/users', '/private', '/.env',
        '/api/v1/admin', '/api/v1/config', '/restricted', '/api/v1/secure', '/db', '/wp-admin'
    ],
    '403': [
        '/admin', '/dashboard', '/settings', '/profile', '/private', '/hidden', '/secure', '/config',
        '/api/v1/protected', '/.htpasswd', '/forbidden', '/user/settings', '/.git', '/restricted'
    ],
    '404': [
        '/api/v1/orders', '/api/v2/users', '/api/v2/logout', '/api/v2/register', '/api/v2/login',
        '/hidden', '/backup', '/old', '/private', '/.git', '/.env', '/404', '/.svn', '/cgi-bin',
        '/nonexistent', '/void', '/unused', '/api/v1/notfound'
    ],
    '405': [
        '/api/v1/products', '/api/v2/products', '/api/v1/invalid', '/notallowed', '/blocked', 
        '/methodnotallowed', '/wrong/method'
    ],
    '429': [
        '/admin', '/api/v1/orders', '/rate/limit', '/exceeded', '/throttled', '/retry/after',
        '/api/v2/limit', '/flood', '/slowdown'
    ],
    '500': [
        '/api/v1/login', '/api/v1/fault', '/internal/error', '/server/broken', '/crash', 
        '/api/v1/issues', '/malfunction', '/fail', '/error', '/db/error'
    ],
    '502': [
        '/api/v1/logout', '/bad/gateway', '/proxy/error', '/502', '/server/bad', '/gateway/fail',
        '/network/error', '/downstream', '/upstream/fail', '/proxy/fail'
    ],
    '503': [
        '/search', '/maintenance', '/temporarily/down', '/unavailable', '/api/v1/maintenance', 
        '/retry/later', '/busy', '/offline', '/overloaded', '/service/unavailable'
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
