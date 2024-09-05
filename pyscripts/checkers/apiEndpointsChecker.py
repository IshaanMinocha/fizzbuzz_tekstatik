import json
import re

def read_payloads(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read each line, strip newline characters, and store it in a list
            payloads = [line.strip() for line in file.readlines()]
        return payloads
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    except IOError:
        print(f"Error reading file {file_path}.")
        return []

def identify_api_vulnerabilities(data, api_path_file):
    # Check if fuzz_type is 'apiendpoint'
    if data.get("fuzzType") != "apiendpoint":
        print("Fuzz type is not 'apiendpoint'. No vulnerabilities identified.")
        return {
            "targetUrl": data.get("targetUrl", ""),
            "fuzzType": data.get("fuzzType", ""),
            "vulnerabilities": []
        }

    api_paths = read_payloads(api_path_file)

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

    # Extracting targetUrl and fuzzType from input data
    target_url = data.get("targetUrl", "")
    fuzz_type = data.get("fuzzType", "")
    results = data.get("results", [])

    # Analyzing each entry in the results data
    for entry in results:
        payload = entry.get('payload', '')
        response = entry.get('response')
        _id = entry.get('_id', '')

        # Check if the payload contains any API path
        contains_api_path = any(payload.startswith(api_path) for api_path in api_paths)

        # Check for exposed API paths
        if contains_api_path:
            vulnerabilities.append({
                'vulnerability': 'Exposed or Misconfigured API Endpoint',
                'severity': 'High',
                'location': f'API Endpoint: {payload}',
                'id': _id
            })

        # Check for response code vulnerabilities
        if response == '200' and contains_api_path:
            vulnerabilities.append({
                'vulnerability': 'Sensitive data exposure/ Broken Authentication',
                'severity': 'High',
                'location': f'Accessible API Endpoint: {payload}',
                'id': _id
            })
        if response == '301' and contains_api_path:
            vulnerabilities.append({
                'vulnerability': 'Open Redirect/ Information Disclosure',
                'severity': 'High',
                'location': f'Accessible API Endpoint: {payload}',
                'id': _id
            })
        elif response == '401' and contains_api_path:
            vulnerabilities.append({
                'vulnerability': 'Broken Authentication and Session Management',
                'severity': 'High',
                'location': f'Restricted API Endpoint: {payload}',
                'id': _id
            })
        elif response == '403' and contains_api_path:
            vulnerabilities.append({
                'vulnerability': 'Bypass using HTTP methods',
                'severity': 'High',
                'location': f'Restricted API Endpoint: {payload}',
                'id': _id
            })
        elif response == '404' and contains_api_path:
            vulnerabilities.append({
                'vulnerability': 'Endpoint Enumeration/ Information Disclosure',
                'severity': 'Medium',
                'location': f'Restricted API Endpoint: {payload}',
                'id': _id
            })
        elif response == '405' and contains_api_path:
            vulnerabilities.append({
                'vulnerability': 'HTTP Verb Tampering/ Improper Security Configuration',
                'severity': 'Medium',
                'location': f'Restricted API Endpoint: {payload}',
                'id': _id
            })
        elif response == '500':
            vulnerabilities.append({
                'vulnerability': 'Server Misconfiguration or Injection Vulnerabilities',
                'severity': 'Critical',
                'location': f'Path causing server error: {payload}',
                'id': _id
            })
        elif response == '502':
            vulnerabilities.append({
                'vulnerability': 'Misconfigured Proxies or Gateways or Network-Based Attacks',
                'severity': 'Low',
                'location': f'Path causing server error: {payload}',
                'id': _id
            })
        elif response == '503':
            vulnerabilities.append({
                'vulnerability': 'Denial of Service',
                'severity': 'High',
                'location': f'Path causing server error: {payload}',
                'id': _id
            })
        elif response == '429':
            vulnerabilities.append({
                'vulnerability': 'Rate Limiting Bypass or Denial of Service',
                'severity': 'High',
                'location': f'Path causing server error: {payload}',
                'id': _id
            })

        # Check for potential SQL Injection vulnerabilities
        for pattern in sql_injection_patterns:
            if re.search(pattern, payload, re.IGNORECASE):
                vulnerabilities.append({
                    'vulnerability': 'Potential SQL Injection',
                    'severity': 'High',
                    'location': f'Path: {payload}',
                    'id': _id
                })
                break

        # Check for potential XSS vulnerabilities
        for pattern in xss_patterns:
            if re.search(pattern, payload, re.IGNORECASE):
                vulnerabilities.append({
                    'vulnerability': 'Potential Cross-Site Scripting (XSS)',
                    'severity': 'High',
                    'location': f'Path: {payload}',
                    'id': _id
                })
                break

        # Check for potential directory traversal
        if '..' in payload:
            vulnerabilities.append({
                'vulnerability': 'Potential Directory Traversal',
                'severity': 'High',
                'location': f'Path: {payload}',
                'id': _id
            })

    return {
        "targetUrl": target_url,
        "fuzzType": fuzz_type,
        "vulnerabilities": vulnerabilities
    }

# Get JSON input from the user
json_input =input("enter input")
try:
    # Load JSON input from the user
    data = json.loads(json_input)
except json.JSONDecodeError:
    print("Invalid JSON input. Please provide valid JSON.")
    data = {}

# Specify the path to the .txt file containing API paths
api_path_file = 'api_payl0ads.txt'  # Replace with your actual file path

# Identifying vulnerabilities
vulnerabilities_found = identify_api_vulnerabilities(data, api_path_file)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
