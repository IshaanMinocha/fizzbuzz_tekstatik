import json
import re

def identify_url_parameter_vulnerabilities(json_input):
    # Regular expressions for identifying potential vulnerabilities in URL parameters
    sql_injection_patterns = [
        r"'.*--",
        r"union.*select",
        r"insert.*into",
        r"delete.*from",
        r"drop.*table",
        r"select.*from.*where.*",
        r"union.*all.*select"
    ]

    xss_patterns = [
        r"<script>",
        r"javascript:",
        r"onerror=",
        r"onload=",
        r"alert\(.*\)"
    ]

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

# Sample JSON input
json_input = '''
[
  {
    "url": "http://example.com/api/v1/search?q=user' OR '1'='1",
    "status": 200,
    "size": 54321,
    "words": 234,
    "lines": 12,
    "duration": "0.234s"
  },
  {
    "url": "http://example.com/api/v1/login?user=admin&password=<script>alert('XSS')</script>",
    "status": 200,
    "size": 67890,
    "words": 456,
    "lines": 20,
    "duration": "0.456s"
  },
  {
    "url": "http://example.com/api/v1/profile?token=abc123",
    "status": 200,
    "size": 5678,
    "words": 123,
    "lines": 5,
    "duration": "0.234s"
  },
  {
    "url": "http://example.com/api/v1/submit?password=secret",
    "status": 200,
    "size": 1234,
    "words": 10,
    "lines": 2,
    "duration": "0.345s"
  }
]
'''

# Identifying vulnerabilities
vulnerabilities_found = identify_url_parameter_vulnerabilities(json_input)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
