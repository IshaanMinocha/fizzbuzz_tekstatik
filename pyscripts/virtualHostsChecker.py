import json
import re

def read_payloads(vhosts):
    try:
        with open(vhosts, 'r') as file:
            # Read each line, strip newline characters, and store it in a list
            payloads = [line.strip() for line in file.readlines()]
        return payloads
    except FileNotFoundError:
        print(f"File {vhosts} not found.")
        return []

def vhosts_vulnerabilities(json_input, vhosts):
    # Read API paths from the specified .txt file
    api_paths = read_payloads(vhosts)

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
        payload = entry.get('payload', '')
        response = entry.get('response')
        _id = entry.get('_id', '')

        if any(vh_path in payload for vh_path in vhosts):
            vulnerabilities.append({
                'vulnerability': 'Exposed or Misconfigured virtual host',
                'severity': 'High',
                'location': f'virtual host: {payload}',
                'id': _id
            })

        # Check for response code vulnerabilities
        if response == '200' and any(vh_path in payload for vh_path in vhosts):
            vulnerabilities.append({
                'vulnerability': 'Sensitive data exposure in virtual host',
                'severity': 'High',
                'location': f'Accessible virtual host {payload}',
                'id': _id
            })
        elif response == '403' and any(vh_path in payload for vh_path in vhosts):
            vulnerabilities.append({
                'vulnerability': 'Restricted virtual host - potential misconfiguration',
                'severity': 'Medium',
                'location': f'Restricted virtual host: {payload}',
                'id': _id
            })
        elif response == '500':
            vulnerabilities.append({
                'vulnerability': 'Server Misconfiguration or Error in virtual host',
                'severity': 'Medium',
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
                'vulnerability': 'Potential virtual host Traversal',
                'severity': 'High',
                'location': f'Path: {payload}',
                'id': _id
            })

    return vulnerabilities


# Get JSON input from the user
json_input = input("Enter the JSON input:")

# Specify the path to the .txt file containing virtual hosts paths
vhosts = 'vhosts.txt'  # Replace with your actual file path

# Identifying vulnerabilities
vulnerabilities_found = vhosts_vulnerabilities(json_input, vhosts)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
