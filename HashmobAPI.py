import os
import json
import requests
import time

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def upload_to_api(data, api_endpoint, api_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.post(api_endpoint, json=data, headers=headers)
    return response


def parse_potfile(potfile_path):
    results = []
    with open(potfile_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) == 3:
                    result = {
                        'hash': parts[0],
                        'password': parts[2]
                    }
                    results.append(result)
    return results

def main():
    potfile_path = input("Enter the path to your hashcat.potfile: ")
    json_output_path = input("Enter the path for the JSON output file: ")
    api_endpoint = input("Enter the API endpoint URL: ")
    api_key = input("Enter your API key: ")
    algorithm = input("Enter the value for 'algorithm': ")

    # Convert potfile to JSON
    results = parse_potfile(potfile_path)

    # Prepare data for API upload
    data = {
        "algorithm": algorithm,
        "founds": results
    }

    # Upload data to API
    try:
        response = upload_to_api(data, api_endpoint, api_key)
        print(f'Status code: {response.status_code}')
    except Exception as e:
        print(f'Error: {e}')

    # Write JSON data to file
    with open(json_output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    main()
