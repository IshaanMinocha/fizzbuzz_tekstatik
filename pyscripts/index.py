import argparse
import json

# Import functions from each of the existing scripts
from apiEndpointChecker import identify_api_vulnerabilities
from hiddenDirectoriesChecker import identify_hidden_directory_vulnerabilities
from injectionPatternsChecker import identify_vulnerabilities
from subdomainsChecker import identify_subdomain_vulnerabilities
from urlParaChecker import identify_url_parameter_vulnerabilities
from virtualHostsChecker import identify_virtual_host_vulnerabilities
from vulnerabilityChecker import check_vulnerabilities

def main():
    parser = argparse.ArgumentParser(description="Run various security checks.")
    parser.add_argument('--check', choices=['api', 'Hidden Directories', 'injections', 'subdomains', 'url parameters', 'Virtual Hosts', 'vulnerabilities'],
                        help='Type of check to perform', required=True)
    parser.add_argument('--input', help='Input JSON file for analysis', required=True)  # Input JSON file is required for all checks

    args = parser.parse_args()

    # Read JSON input from the file
    try:
        with open(args.input, 'r') as file:
            json_input = file.read()
    except FileNotFoundError:
        print(f"Error: The file {args.input} was not found.")
        return
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading the input file: {e}")
        return

    # Determine which check to run based on the argument provided
    if args.check == 'api':
        # API vulnerability check
        results = identify_api_vulnerabilities(json_input)
        print(json.dumps(results, indent=2))
    
    elif args.check == 'hidden Directories':
        # Hidden directories check
        results = identify_hidden_directory_vulnerabilities(json_input)
        print(json.dumps(results, indent=2))
    
    elif args.check == 'injections':
        # Injection patterns check
        results = identify_vulnerabilities(json_input)
        print(json.dumps(results, indent=2))
    
    elif args.check == 'subdomains':
        # Subdomains check
        results = identify_subdomain_vulnerabilities(json_input)
        print(json.dumps(results, indent=2))
    
    elif args.check == 'url parameters':
        # URL parameters check
        results = identify_url_parameter_vulnerabilities(json_input)
        print(json.dumps(results, indent=2))
    
    elif args.check == 'Virtual Hosts':
        # Virtual hosts check
        results = identify_virtual_host_vulnerabilities(json_input)
        print(json.dumps(results, indent=2))
    
    elif args.check == 'vulnerabilities':
        # General vulnerabilities check
        results = check_vulnerabilities(json_input)
        print(json.dumps(results, indent=2))
    else:
        print("Invalid check type specified.")

if __name__ == "__main__":
    main()
