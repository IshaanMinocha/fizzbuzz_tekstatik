import json
import re

def read_payloads(file_path):
    """
    Reads payloads (API paths) from a .txt file specified by file_path.
    
    :param file_path: Path to the .txt file containing API paths.
    :return: A list of API paths.
    """
    try:
        with open(file_path, 'r') as file:
            # Read each line, strip newline characters, and store it in a list
            payloads = [line.strip() for line in file.readlines()]
        return payloads
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def identify_api_vulnerabilities(json_input, api_path_file):
    """
    Identifies vulnerabilities in API endpoints based on predefined API paths
    and other patterns, using the API paths read from a .txt file.
    
    :param json_input: JSON input containing API details.
    :param api_path_file: Path to the .txt file containing API paths.
    :return: A list of detected vulnerabilities.
    """
    # Read API paths from the specified .txt file
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

# Specify the path to the .txt file containing API paths
api_path_file = 'api_payloads.txt'  # Replace with your actual file path

# Identifying vulnerabilities
vulnerabilities_found = identify_api_vulnerabilities(json_input, api_path_file)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
