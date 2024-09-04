import json
import re

def read_payloads(hidden_directories):
    try:
        with open(hidden_directories, 'r') as file:
            # Read each line, strip newline characters, and store it in a list
            payloads = [line.strip() for line in file.readlines()]
        return payloads
    except FileNotFoundError:
        print(f"File {hidden_directories} not found.")
        return []

def identify_hidden_directory_vulnerabilities(json_input, hidden_directories):
    # Read API paths from the specified .txt file
    hidden_directories = read_payloads(hidden_directories)

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

        if any(hidden_dir in payload for hidden_dir in hidden_directories):
            vulnerabilities.append({
                'vulnerability': 'Exposed or Misconfigured hidden directories',
                'severity': 'High',
                'location': f'hidden Directory: {payload}',
                'id': _id
            })

        # Check for response code vulnerabilities
        if response == '200' and any(hidden_dir in payload for hidden_dir in hidden_directories):
            vulnerabilities.append({
                'vulnerability': 'Sensitive data exposure in hidden directory',
                'severity': 'High',
                'location': f'Accessible Hidden Directory {payload}',
                'id': _id
            })
        elif response == '403' and any(hidden_dir in payload for hidden_dir in hidden_directories):
            vulnerabilities.append({
                'vulnerability': 'Restricted hidden directory - potential misconfiguration',
                'severity': 'Medium',
                'location': f'Restricted Hidden Directory: {payload}',
                'id': _id
            })
        elif response == '500':
            vulnerabilities.append({
                'vulnerability': 'Server Misconfiguration or Error in hidden directories',
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
                'vulnerability': 'Potential Directory Traversal',
                'severity': 'High',
                'location': f'Path: {payload}',
                'id': _id
            })

    return vulnerabilities


# Get JSON input from the user
json_input = input("Enter the JSON input:")

# Specify the path to the .txt file containing dir paths
hidden_directories = '../../payloads/Directories_All.wordlist.txt'  # Replace with your actual file path

# Identifying vulnerabilities
vulnerabilities_found = identify_hidden_directory_vulnerabilities(json_input, hidden_directories)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
