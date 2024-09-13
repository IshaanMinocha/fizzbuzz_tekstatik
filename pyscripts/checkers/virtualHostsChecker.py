# import json
# import re

# def read_payloads(vhosts):
#     try:
#         with open(vhosts, 'r') as file:
#             # Read each line, strip newline characters, and store it in a list
#             payloads = [line.strip() for line in file.readlines()]
#         return payloads
#     except FileNotFoundError:
#         print(f"File {vhosts} not found.")
#         return []

# def vhosts_vulnerabilities(data, vhosts):
#     if data.get("fuzzType") != "virtualHosts":
#         print("Fuzz type is not 'virtualHosts'. No vulnerabilities identified.")
#         return {
#             "targetUrl": data.get("targetUrl", ""),
#             "fuzzType": data.get("fuzzType", ""),
#             "vulnerabilities": []
#         }
#     # Read host paths from the specified .txt file
#     vhosts_paths = read_payloads(vhosts)

#     # Regular expressions for identifying potential vulnerabilities
#     sql_injection_patterns = [
#         r"'.*--",
#         r"union.*select",
#         r"insert.*into",
#         r"delete.*from",
#         r"drop.*table"
#     ]

#     xss_patterns = [
#         r"<script>",
#         r"javascript:",
#         r"onerror=",
#         r"onload="
#     ]

#     vulnerabilities = []

#     # Extracting targetUrl and fuzzType from input data
#     target_url = data.get("targetUrl", "")
#     fuzz_type = data.get("fuzzType", "")
#     results = data.get("results", [])

#     # Analyzing each entry in the JSON data
#     for entry in results:
#         payload = entry.get('payload', '')
#         response = entry.get('response')
#         _id = entry.get('_id', '')

#         # Check if the payload contains any API path
#         contains_vhost_path = any(payload.startswith(vhost_path) for vhost_path in vhosts_paths)

#         if contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Exposed or Misconfigured virtual host',
#                 'severity': 'High',
#                 'location': f'virtual host: {payload}',
#                 'id': _id
#             })

#         # Check for response code vulnerabilities
#         if response == '200' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Sensitive data exposure/ Broken Authentication',
#                 'severity': 'High',
#                 'location': f'Accessible virtual host {payload}',
#                 'id': _id
#             })
#         elif response == '301' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Open Redirect/ Information Disclosure',
#                 'severity': 'High',
#                 'location': f'Accessible API Endpoint: {payload}',
#                 'id': _id
#             })
#         elif response == '401' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Broken Authentication and Session Management',
#                 'severity': 'High',
#                 'location': f'Restricted API Endpoint: {payload}',
#                 'id': _id
#             })
#         elif response == '403' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Bypass using HTTP methods',
#                 'severity': 'High',
#                 'location': f'Restricted API Endpoint: {payload}',
#                 'id': _id
#             })
#         elif response == '404' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Endpoint Enumeration/ Information Disclosure',
#                 'severity': 'Medium',
#                 'location': f'Restricted API Endpoint: {payload}',
#                 'id': _id
#             })
#         elif response == '405' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'HTTP Verb Tampering/ Improper Security Configuration',
#                 'severity': 'Medium',
#                 'location': f'Restricted API Endpoint: {payload}',
#                 'id': _id
#             })
#         elif response == '500' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Server Misconfiguration or Injection Vulnerabilities',
#                 'severity': 'Critical',
#                 'location': f'Path causing server error: {payload}',
#                 'id': _id
#             })
#         elif response == '502' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Misconfigured Proxies or Gateways or Network-Based Attacks',
#                 'severity': 'Low',
#                 'location': f'Path causing server error: {payload}',
#                 'id': _id
#             })
#         elif response == '503' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Denial of Service',
#                 'severity': 'High',
#                 'location': f'Path causing server error: {payload}',
#                 'id': _id
#             })
#         elif response == '429' and contains_vhost_path:
#             vulnerabilities.append({
#                 'vulnerability': 'Rate Limiting Bypass or Denial of Service',
#                 'severity': 'High',
#                 'location': f'Path causing server error: {payload}',
#                 'id': _id
#             })

#         # Check for potential SQL Injection vulnerabilities
#         for pattern in sql_injection_patterns:
#             if re.search(pattern, payload, re.IGNORECASE):
#                 vulnerabilities.append({
#                     'vulnerability': 'Potential SQL Injection',
#                     'severity': 'High',
#                     'location': f'Path: {payload}',
#                     'id': _id
#                 })
#                 break

#         # Check for potential XSS vulnerabilities
#         for pattern in xss_patterns:
#             if re.search(pattern, payload, re.IGNORECASE):
#                 vulnerabilities.append({
#                     'vulnerability': 'Potential Cross-Site Scripting (XSS)',
#                     'severity': 'High',
#                     'location': f'Path: {payload}',
#                     'id': _id
#                 })
#                 break

#         # Check for potential directory traversal
#         if '..' in payload:
#             vulnerabilities.append({
#                 'vulnerability': 'Potential virtual host Traversal',
#                 'severity': 'High',
#                 'location': f'Path: {payload}',
#                 'id': _id
#             })

#     return {
#         "targetUrl": target_url,
#         "fuzzType": fuzz_type,
#         "vulnerabilities": vulnerabilities
#     }

# # Get JSON input from the user
# json_input ='''{
#     "fuzzType": "virtualHosts",
#     "targetUrl": "http://example.com",
#     "results": [
#         {
#             "payload": "http://example.com/admin",
#             "response": "200",
#             "_id": "123"
#         },
#         {
#             "payload": "http://example.com/test",
#             "response": "404",
#             "_id": "124"
#         },
#         {
#             "payload": "http://example.com/../../etc/passwd",
#             "response": "500",
#             "_id": "125"
#         }
#     ]
# }
# '''

# try:
#     # Load JSON input from the user
#     data = json.loads(json_input)
# except json.JSONDecodeError:
#     print("Invalid JSON input. Please provide valid JSON.")
#     data = {}

# # Specify the path to the .txt file containing virtual hosts paths
# vhosts = 'vh0sts.txt'  # Replace with your actual file path

# # Identifying vulnerabilities
# vulnerabilities_found = vhosts_vulnerabilities(data, vhosts)

# # Convert vulnerabilities to JSON format
# vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# # Print the JSON output
# print(vulnerabilities_json)
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
