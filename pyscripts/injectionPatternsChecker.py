import json
import re
import requests

def identify_vulnerabilities(json_input):
    # Patterns for detecting header injection vulnerabilities
    header_injection_patterns = [
        r'\r\n',
        r'\n\n',
        r'Host: .*',
        r'X-Forwarded-For: .*'
    ]

    # Shell Injection patterns
    shell_injection_patterns = [
        r'\b(?:;|&&|\|\|)\s*(?:rm\s*-rf\s*|ls\s*-l\s*|cat\s*)\b',
        r'\b(?:system|exec|shell_exec|passthru)\b',
        r'\b(?:`|\'|\"\|)\s*(?:ls\s*-l\s*|ps\s*-ef\s*)\b'
    ]

    # Cookie security checks
    cookie_security_flags = {
        'Secure': 'Ensure cookies are transmitted over HTTPS only',
        'HttpOnly': 'Prevent access to cookies via JavaScript',
        'SameSite': 'Control cross-site request forgery'
    }

    # AJAX Injection checks (Placeholder)
    ajax_injection_placeholder = "Client-side analysis required for AJAX injections."

    vulnerabilities = []

    # Load the JSON input
    data = json.loads(json_input)

    # Analyzing each entry in the JSON data
    for entry in data:
        url = entry.get('url', '')
        headers = entry.get('headers', {})
        cookies = entry.get('cookies', {})
        response_body = entry.get('response_body', '')
        _id = entry.get('_id', '')
        # Header Manipulation Checks
        for pattern in header_injection_patterns:
            if re.search(pattern, response_body, re.IGNORECASE):
                vulnerabilities.append({
                    'vulnerability': 'Potential Header Injection',
                    'severity': 'High',
                    'location': f'URL: {url}',
                    'details': f'Matched Pattern: {pattern}',
                    'id': _id
                })

        # Shell Injection Checks
        for pattern in shell_injection_patterns:
            if re.search(pattern, url, re.IGNORECASE) or any(re.search(pattern, param, re.IGNORECASE) for param in entry.get('params', [])):
                vulnerabilities.append({
                    'vulnerability': 'Potential Shell Injection',
                    'severity': 'High',
                    'location': f'URL: {url}',
                    'details': f'Matched Pattern: {pattern}',
                    'id': _id
                })

        # Session and Cookie Analysis
        for cookie_name, cookie_value in cookies.items():
            for flag, description in cookie_security_flags.items():
                if flag not in cookie_value:
                    vulnerabilities.append({
                        'vulnerability': f'Cookie Security Flag Missing: {flag}',
                        'severity': 'High',
                        'location': f'Cookie: {cookie_name}',
                        'details': description,
                        'id': _id
                    })

        # AJAX Injection Checks
        vulnerabilities.append({
            'vulnerability': ajax_injection_placeholder,
            'severity': 'Info',
            'location': f'URL: {url}',
            'details': 'Client-side analysis required for AJAX injections.',
            'id': _id
        })

    return vulnerabilities

# Sample JSON input
json_input = '''
[
  {
    "url": "http://example.com/api/v1/search?q=ls%20-l",
    "headers": {
      "X-Forwarded-For": "127.0.0.1"
    },
    "cookies": {
      "session_id": "abc123; Secure; HttpOnly",
      "user_token": "xyz789"
    },
    "response_body": "Some response with potential header injection \\r\\n Host: evil.com"
  },
  {
    "url": "http://example.com/some/path?param=`rm -rf /`",
    "headers": {
      "Content-Type": "application/json"
    },
    "cookies": {
      "session_id": "def456"
    },
    "response_body": "Response body content"
  }
]
'''

# Identifying vulnerabilities
vulnerabilities_found = identify_vulnerabilities(json_input)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
