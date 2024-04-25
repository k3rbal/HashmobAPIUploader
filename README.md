# Hashcat Potfile Parser and API Uploader

This Python script allows you to parse a `hashcat.potfile`, convert its contents into a JSON format, and upload it to an API endpoint. It is useful for monitoring and managing hash cracking results obtained using hashcat.

## Prerequisites

Before using this script, ensure you have the following installed:

- Python 3
- Requests library (install via `pip install requests`)

## Usage

1. Clone this repository to your local machine.

2. Navigate to the directory containing the script.

3. Run the script using the following command:

python hashcat_parser.py


4. Follow the prompts to enter the required information:
- Path to the `hashcat.potfile`
- Path for the JSON output file
- API endpoint URL
- API key
- Value for the 'algorithm'
- Delay between resubmissions in seconds

5. The script will continuously monitor the `hashcat.potfile`, converting its contents into JSON format and uploading them to the specified API endpoint. It will wait for the specified delay between resubmissions.

**Note:** This script was written to submit hashes to Hashmob.net's API and does not currently support salted submissions, though their API does.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
