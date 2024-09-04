import json
import re

def read_patterns(file_path):
    try:
        with open(file_path, 'r') as file:
            patterns = [line.strip() for line in file.readlines()]
        return patterns
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def identify_url_parameter_vulnerabilities(json_input):
    # File paths to the patterns files
    sql_patterns_file = 'sql_injection_patterns.txt'
    xss_patterns_file = 'xss_patterns.txt'

    # Read patterns from files
    sql_injection_patterns = read_patterns(sql_patterns_file)
    xss_patterns = read_patterns(xss_patterns_file)

    vulnerabilities = []

    # Load the JSON input
    data = json.loads(json_input)

    # Analyzing each entry in the JSON data
    for entry in data:
        url = entry.get('url', '')

        # Extract URL parameters
        params = re.findall(r'\?(.*?)$', url)
        if params:
            param_string = params[0]
            param_pairs = param_string.split('&')
            for pair in param_pairs:
                key_value = pair.split('=')
                if len(key_value) == 2:
                    param_value = key_value[1]

                    # Check for SQL Injection vulnerabilities
                    for pattern in sql_injection_patterns:
                        if re.search(pattern, param_value, re.IGNORECASE):
                            vulnerabilities.append({
                                'vulnerability': 'Potential SQL Injection',
                                'severity': 'High',
                                'location': f'URL Parameter: {pair}',
                                'url': url
                            })
                            break

                    # Check for XSS vulnerabilities
                    for pattern in xss_patterns:
                        if re.search(pattern, param_value, re.IGNORECASE):
                            vulnerabilities.append({
                                'vulnerability': 'Potential Cross-Site Scripting (XSS)',
                                'severity': 'High',
                                'location': f'URL Parameter: {pair}',
                                'url': url
                            })
                            break

                    # Check for Sensitive Data Exposure
                    if re.search(r'(password|secret|token|key)', key_value[0], re.IGNORECASE):
                        vulnerabilities.append({
                            'vulnerability': 'Sensitive Data Exposure in URL Parameter',
                            'severity': 'High',
                            'location': f'URL Parameter: {pair}',
                            'url': url
                        })

    return vulnerabilities

# Identifying vulnerabilities
vulnerabilities_found = identify_url_parameter_vulnerabilities(json_input)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)