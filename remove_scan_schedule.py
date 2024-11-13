import argparse
import requests

API_BASE_URL = 'https://api.detectify.com/rest'


def get_scan_profiles(key: str) -> list:
    """Retrieve all scan profiles and extract their tokens.

    :param key: A valid Detectify API key
    :return: A list of scan profile tokens
    """
    print("Retrieving scan profiles...")
    api_endpoint = '/v2/profiles/'
    response = requests.get(url=f'{API_BASE_URL}{api_endpoint}', headers={'X-Detectify-Key': key})

    if response.status_code == 200:
        profiles = response.json()
        tokens = [profile['token'] for profile in profiles]
        print(f"Retrieved {len(tokens)} scan profiles.")
        return tokens
    else:
        print(f"Failed to retrieve scan profiles: {response.status_code} - {response.text}")
        return []


def remove_scan_schedule(key: str, token: str) -> None:
    """Remove the scan schedule for a given scan profile token.

    :param key: A valid Detectify API key
    :param token: The token for the scan profile to remove the schedule from
    """
    api_endpoint = f'/v2/scanschedules/{token}/'
    response = requests.delete(url=f'{API_BASE_URL}{api_endpoint}', headers={'X-Detectify-Key': key})

    if response.status_code == 200:
        print(f"Successfully removed scan schedule for token: {token}")
    else:
        print(f"Failed to remove scan schedule for token {token}: {response.status_code} - {response.text}")


def main():
    parser = argparse.ArgumentParser(description='Remove scan schedules for all Detectify scan profiles')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    args = parser.parse_args()

    tokens = get_scan_profiles(args.key)
    if tokens:
        for token in tokens:
            remove_scan_schedule(args.key, token)


if __name__ == '__main__':
    main()
