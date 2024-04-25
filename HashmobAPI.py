import json
import requests
import os
import argparse
import time

CONFIG_PATH = 'api_config.json'
POTFILE_PATH = 'hashcat.potfile'
API_ENDPOINT = 'https://hashmob.net/api/v2/submit'


def get_config(config_path):
    if os.path.isfile(config_path):
        with open(config_path) as file:
            return json.load(file)
    else:
        return {}


def update_config(config_data, config_path):
    with open(config_path, 'w') as file:
        json.dump(config_data, file)


def setup():
    parser = argparse.ArgumentParser(
        prog='HashMob API Submit',
        description='Repeatedly submits the given potfile after a set delay.'
    )

    parser.add_argument('-c', '--config')
    parser.add_argument('-p', '--potfile')

    return parser.parse_args()


def upload_to_api(data, api_endpoint, api_key):
    headers = {
        'Content-Type': 'application/json',
        'API-Key': api_key
    }

    response = requests.post(api_endpoint, json=data, headers=headers)
    return response


def parse_potfile(potfile_path, previous_size):
    results = []
    with open(potfile_path) as file:
        file.seek(previous_size)
        for line in file:
            results.append(line.strip())

    return results


def main():
    args = setup()
    config_path = args.config or CONFIG_PATH
    potfile_path = args.potfile or POTFILE_PATH
    
    # Check for config file or generate defaults
    config_data = get_config(config_path)

    # Use defined config or ask for defaults on first time
    potfile_path = config_data.get('potfile_path', input("Enter the path to your hashcat.potfile: "))
    api_key = config_data.get('api_key', input("Enter your API key: "))
    resubmission_delay = config_data.get('resubmission_delay', int(input("Enter the delay between resubmissions in seconds: ")))
    previous_size = config_data.get('previous_size', 0)
    
    config_data['potfile_path'] = potfile_path
    config_data['api_key'] = api_key
    config_data['resubmission_delay'] = resubmission_delay
    update_config(config_data, config_path)

    algorithm = input("Enter the value for 'algorithm': ")
    while True:
        # Check current size and see if it has changed. If it hasn't wait resubmit delay
        while not os.path.getsize(potfile_path) > previous_size:
            time.sleep(resubmission_delay)

        previous_size = os.path.getsize()
        config_data['previous_size'] = previous_size
        update_config(config_data, config_path)

        # Convert potfile to JSON
        results = parse_potfile(potfile_path, previous_size)

        # Prepare data for API upload
        data = {
            "algorithm": algorithm,
            "founds": results
        }

        # Upload data to API
        try:
            response = upload_to_api(data, API_ENDPOINT, api_key)
            print(f'Status code: {response.status_code}')
        except Exception as e:
            print(f'Error: {e}')


if __name__ == "__main__":
    main()
