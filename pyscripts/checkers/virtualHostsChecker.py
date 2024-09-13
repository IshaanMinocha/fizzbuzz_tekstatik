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
        
        # Check for response code vulnerabilities
        if response == '200' :
            vulnerabilities.append({
                'vulnerability': 'Sensitive data exposure/ Broken Authentication',
                'severity': 'High',
                'payload':payload,
                'id': _id
            })
        elif response == '301' :
            vulnerabilities.append({
                'vulnerability': 'Open Redirect/ Information Disclosure',
                'severity': 'High',
                'payload':payload,
                'id': _id
            })
        elif response == '401' :
            vulnerabilities.append({
                'vulnerability': 'Broken Authentication and Session Management',
                'severity': 'High',
                'payload':payload,
                'id': _id
            })
        elif response == '403' :
            vulnerabilities.append({
                'vulnerability': 'Bypass using HTTP methods',
                'severity': 'High',
                'payload':payload
            })
        elif response == '404' :
            vulnerabilities.append({
                'vulnerability': 'Endpoint Enumeration/ Information Disclosure',
                'severity': 'Medium',
                'payload':payload
            })
        elif response == '405' :
            vulnerabilities.append({
                'vulnerability': 'HTTP Verb Tampering/ Improper Security Configuration',
                'severity': 'Medium',
                'payload': payload
            })
        elif response == '500' :
            vulnerabilities.append({
                'vulnerability': 'Server Misconfiguration or Injection Vulnerabilities',
                'severity': 'Critical',
                'payload': payload
            })
        elif response == '502' :
            vulnerabilities.append({
                'vulnerability': 'Misconfigured Proxies or Gateways or Network-Based Attacks',
                'severity': 'Low',
                'payload': payload
            })
        elif response == '503' :
            vulnerabilities.append({
                'vulnerability': 'Denial of Service',
                'severity': 'High',
                'payload': payload
            })
        elif response == '429' :
            vulnerabilities.append({
                'vulnerability': 'Rate Limiting Bypass or Denial of Service',
                'severity': 'High',
                'payload': payload
            })
 
    return {
        "targetUrl": data.get("targetUrl", ""),
        "fuzzType": data.get("fuzzType", ""),
        "vulnerabilities": vulnerabilities,
        "vulnerabiltity": max(vuln["vulnerability"] for vuln in vulnerabilities) if vulnerabilities else None,
        "severity": max((vuln["severity"] for vuln in vulnerabilities), default=None)
    }

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

json_file_path = os.path.join(os.path.dirname(__file__), 'virtualHosts.json')

json_input = read_json_file(json_file_path)

if json_input:
    vulnerabilities_found = identify_api_endpoint_vulnerabilities(json_input)
    vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)
    print(vulnerabilities_json)
