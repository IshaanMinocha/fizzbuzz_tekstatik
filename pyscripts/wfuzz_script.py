import sys
import subprocess
import json
import re

def run_wfuzz(url, flags):
    #command = ["wsl", "wfuzz"] + flags + [url] # win with wsl 
    command = ["wfuzz"] + flags + [url] # mac
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result.stdout, result.stderr

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def parse_output(output):
    output = strip_ansi_codes(output)  #  this will strip ansi escape codes
    # print("Raw Wfuzz result:\n")
    #print(output)
    results = []
    lines = output.splitlines()

    for line in lines:
        if line.startswith("000"):
            match = re.match(r"(\d+):\s+(\d+)\s+(\d+)\s+L\s+(\d+)\s+W\s+(\d+)\s+Ch\s+\"([^\"]+)\"", line)
            if match:
                results.append({
                    "response": match.group(2),
                    "lines": int(match.group(3)),
                    "words": int(match.group(4)),
                    "chars": int(match.group(5)),
                    "payload": match.group(6)
                })
    return results

if __name__ == "__main__":
    url = sys.argv[1]
    flags = sys.argv[2:]
    fuzz_type = sys.argv[5]
    
    stdout, stderr = run_wfuzz(url, flags)

    if stderr:
        print("Error:", stderr, file=sys.stderr)
    else:
        results = parse_output(stdout)
        fuzz_data = {
            "targetUrl": url,
            "fuzzType": fuzz_type,  
            "output": results
        }
        json_output = json.dumps(fuzz_data, indent=4)
        print(json_output)