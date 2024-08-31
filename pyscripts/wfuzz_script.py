import sys
import subprocess
import json
import re

def run_wfuzz(url, flags):
    command = ["wfuzz"] + flags + [url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def parse_output(output):
    output = strip_ansi_codes(output)  #  this will strip ansi escape codes
    # print("Raw Wfuzz result:\n")
    print(output)
    results = []
    lines = output.splitlines()

    for line in lines:
        if line.startswith("000"):
            match = re.match(r"(\d+):\s+(\d+)\s+(\d+)\s+L\s+(\d+)\s+W\s+(\d+)\s+Ch\s+\"([^\"]+)\"", line)
            if match:
                results.append({
                    "ID": match.group(1),
                    "Response": match.group(2),
                    "Lines": match.group(3),
                    "Words": match.group(4),
                    "Chars": match.group(5),
                    "Payload": match.group(6)
                })
    return results

if __name__ == "__main__":
    url = sys.argv[1]
    flags = sys.argv[2:]

    stdout, stderr = run_wfuzz(url, flags)

    if stderr:
        print("Error:", stderr, file=sys.stderr)
    else:
        results = parse_output(stdout)
        json_output = json.dumps(results, indent=4)
        print(json_output)
