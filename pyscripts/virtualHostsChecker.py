import json
import re

def identify_virtual_host_vulnerabilities(json_input):
    # List of critical paths and files commonly found in virtual hosts
    virtual_host_paths = [
        '/', '/index', '/index.php', '/default', '/admin', '/server-status', '/server-info',
        '/vhost/', '/vhosts/', '/virtual/', '/config/', '/conf/', '/web.config',
        '/.htaccess', '/.htpasswd', '/admin/config.php', '/.env', '/phpinfo.php',
        '/wp-config.php', '/db.php', '/localhost/', '/cgi-bin/', '/logs/', '/error/',
        '/debug/', '/status/', '/backup/', '/old/', '/test/', '/dev/', '/webadmin/',
        '/cgi-bin/php.cgi', '/cgi-bin/php5.cgi', '/cgi-bin/perl.cgi'
    ]

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

        # Check for exposed virtual host paths
        if any(vh_path in path for vh_path in virtual_host_paths):
            vulnerabilities.append({
                'vulnerability': 'Exposed or Misconfigured Virtual Host Path',
                'severity': 'High',
                'location': f'Virtual Host Path: {path}',
                'url': url
            })

        # Check for status code vulnerabilities
        if status == 200 and any(vh_path in path for vh_path in virtual_host_paths):
            vulnerabilities.append({
                'vulnerability': 'Accessible sensitive virtual host path',
                'severity': 'High',
                'location': f'Accessible Virtual Host Path: {path}',
                'url': url
            })
        elif status == 403 and any(vh_path in path for vh_path in virtual_host_paths):
            vulnerabilities.append({
                'vulnerability': 'Restricted virtual host path - potential misconfiguration',
                'severity': 'Medium',
                'location': f'Restricted Virtual Host Path: {path}',
                'url': url
            })
        elif status == 500:
            vulnerabilities.append({
                'vulnerability': 'Server Misconfiguration or Error in Virtual Host',
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

# Sample JSON input
json_input = '''
[
  {
    "path": "/vhost/admin/config.php",
    "status": 200,
    "size": 54321,
    "words": 234,
    "lines": 12,
    "duration": "0.234s",
    "url": "http://example.com/vhost/admin/config.php",
    "headers": {
      "server": "Apache/2.4.41 (Ubuntu)"
    }
  },
  {
    "path": "/server-status",
    "status": 403,
    "size": 67890,
    "words": 456,
    "lines": 20,
    "duration": "0.456s",
    "url": "http://example.com/server-status",
    "headers": {
      "server": "nginx/1.18.0"
    }
  },
  {
    "path": "/cgi-bin/php.cgi",
    "status": 200,
    "size": 5678,
    "words": 123,
    "lines": 5,
    "duration": "0.234s",
    "url": "http://example.com/cgi-bin/php.cgi",
    "headers": {
      "server": "Apache"
    }
  },
  {
    "path": "/.htaccess",
    "status": 403,
    "size": 1234,
    "words": 10,
    "lines": 2,
    "duration": "0.345s",
    "url": "http://example.com/.htaccess",
    "headers": {
      "server": "nginx"
    }
  },
  {
    "path": "/../../etc/passwd",
    "status": 403,
    "size": 1234,
    "words": 10,
    "lines": 2,
    "duration": "0.345s",
    "url": "http://example.com/../../etc/passwd",
    "headers": {
      "server": "Apache/2.4.41"
    }
  }
]
'''

# Identifying vulnerabilities
vulnerabilities_found = identify_virtual_host_vulnerabilities(json_input)

# Convert vulnerabilities to JSON format
vulnerabilities_json = json.dumps(vulnerabilities_found, indent=2)

# Print the JSON output
print(vulnerabilities_json)
