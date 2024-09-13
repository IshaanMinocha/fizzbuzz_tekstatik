import os
import json
import re

def identify_api_endpoint_vulnerabilities(json_input):
    vulnerabilities = []

    # Load the JSON input
    data = json.loads(json_input)

    # Analyze each entry in the JSON data
    for entry in data.get('output', []):
        response = entry.get('response')
        lines = entry.get('lines', 0)
        words = entry.get('words', 0)
        chars = entry.get('chars', 0)
        payload = entry.get('payload', '')
        _id = entry.get('_id', {})
        
        # print(f"Processing API endpoint payload: {payload}, response: {response}")

        # Assess vulnerabilities based on response codes
        if response == '200':
            vulnerabilities.append({
                'vulnerability': 'Sensitive data exposure or misconfigured public API',
                'severity': 'High',
                'payload': payload,
                
            })
        elif response == '301':
            vulnerabilities.append({
                'vulnerability': 'Potential open redirect or deprecated API endpoint',
                'severity': 'Medium',
                'payload': payload,
                
            })
        elif response == '401':
            vulnerabilities.append({
                'vulnerability': 'Unauthorized access to protected API endpoint',
                'severity': 'High',
                'payload': payload,
               
            })
        elif response == '403':
            vulnerabilities.append({
                'vulnerability': 'Forbidden API access or permissions misconfiguration',
                'severity': 'Medium',
                'payload': payload,
               
            })
        elif response == '404':
            vulnerabilities.append({
                'vulnerability': 'API endpoint enumeration or incorrect endpoint handling',
                'severity': 'Low',
                'payload': payload,
               
            })
        elif response == '500':
            vulnerabilities.append({
                'vulnerability': 'Internal server error, potential API misconfiguration',
                'severity': 'High',
                'payload': payload,
               
            })
        elif response == '502' or response == '503':
            vulnerabilities.append({
                'vulnerability': 'API server instability or unavailability',
                'severity': 'Low',
                'payload': payload,
               
            })

        # Check for potential directory traversal
        if '..' in payload:
            vulnerabilities.append({
                'vulnerability': 'Potential Directory Traversal',
                'severity': 'High',
                'payload': payload,
                
            })

    return {
        "targetUrl": data.get("targetUrl", ""),
        "fuzzType": data.get("fuzzType", ""),
        "vulnerabilities": vulnerabilities,
        "vulnerabiltity": max(vuln["vulnerability"] for vuln in vulnerabilities) if vulnerabilities else None,
        "severity": max((vuln["severity"] for vuln in vulnerabilities), default=None)
    }

# Function to read the JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

# Path to the JSON input file
json_file_path = os.path.join(os.path.dirname(__file__), 'api_endpoints.json')

# Read the JSON input
json_input = read_json_file(json_file_path)

if json_input:
    # Identify API endpoint vulnerabilities
    vulnerabilities_found = identify_api_endpoint_vulnerabilities(json_input)

    # Convert vulnerabilities to JSON format
    vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

    # Print the JSON output
    print(vulnerabilities_json)
