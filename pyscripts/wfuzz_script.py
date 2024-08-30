import sys
import subprocess

def run_wfuzz(url, flags):
    command = ["wfuzz"] + flags + [url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

if __name__ == "__main__":
    url = sys.argv[1]
    flags = sys.argv[2:]

    stdout, stderr = run_wfuzz(url, flags)

    if stderr:
        print("Error:", stderr, file=sys.stderr)
    else:
        print(stdout)
