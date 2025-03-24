#!venv/bin/python3

import requests, logging, sys, os
from dotenv import dotenv_values
from pprint import pprint

# Initialize logging
log_filename = 'duc.log'
root_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(root_dir, 'duc.log')
logging.basicConfig(
    filename=log_path, 
    format='%(asctime)s [%(levelname)s] - %(message)s', 
    datefmt='%Y/%m/%d %I:%M:%S %p',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

logger.info(f'Loading environment variables.')
try:
    # Load variables from .env file into a dictionary
    env_vars = dotenv_values('.env')  # Defaults to `.env` in the current directory
    API_EMAIL = env_vars.get("CLOUDFLARE_API_EMAIL")
    API_TOKEN = env_vars.get("CLOUDFLARE_API_TOKEN")
    ZONE_ID = env_vars.get("CLOUDFLARE_ZONE_ID")
    PUBLIC_IP_API = env_vars.get("PUBLIC_IP_API")
except Exception as e:
    logger.error(f'Error while loading environment variables: {repr(e)}')
    raise SystemExit(repr(e))


def get_public_ip_address(url: str):
    """Gets the current public IP address of the host using a public IP API specified in `url`.

    Args:
        url (str): A URL pointing to the public IP API of choice.

    Returns:
        str: The response from the public IP API.
    """
    return make_api_request('GET', url)
    

def make_api_request(method: str, url: str, headers: dict=None, payload: dict=None):
    """Makes an API request to an API endpoint at `url`.

    Args:
        method (str): The request method to use.`
        url (str): The target URL to send the request to.
        payload (dict, optional): The payload to send in POST and PUT requests. Defaults to None.

    Raises:
        e: An error has occurred while sending the request, or the request has returned a 4xx or 5xx status code.

    Returns:
        dict: A JSON object parsed from the API response. If an error occurs in parsing the response as JSON, then raw text is returned.
    """
    try:
        response = requests.request(method, url, headers=headers, json=payload)
        response.raise_for_status()
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            # logger.warning(f'Response from "{url}" is not valid JSON. Returning raw text instead.') # True, but too noisy. Shhhh
            return response.text
    except Exception as e:
        logger.error(f'Error while making Cloudflare API request: {repr(e)}; Request error info: {response.json()}')
        raise e


def cloudflare_headers():
    """Return the necessary headers for a Cloudflare API request."""
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }


def get_zone_records(zone_id: str):
    """Gets all of the DNS records in the zone specified by `zone_id`.

    Args:
        zone_id (str): The target zone to retrieve DNS records from.

    Returns:
        list(dict): A list of DNS records. Only A and AAAA records are included.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    logger.info(f'Retrieving all DNS records for zone "{zone_id}"...')
    try:
        data = make_api_request('GET', url, headers=cloudflare_headers())
        result = data.get('result')
        filtered_result = [record for record in result if record['type'] in ['A', 'AAAA']]
        logger.info(f'Successfully retrieved {len(filtered_result)} DNS records from zone "{zone_id}".')
        return filtered_result
    except Exception as e:
        logger.error(f'Error while retrieving zone DNS records: {repr(e)}')
        raise e


def update_record(record: dict, zone_id: str, new_ip: str):
    """Updates an individual Cloudflare DNS record

    Args:
        record (dict): The record to update. Ideally, this is pulled straight from a Cloudflare API response.
        zone_id (str): The zone ID of the record to be updated.
        new_ip (str): The IP to update the new record with.

    Raises:
        RuntimeError: The API request went through, but the record was not updated successfully.
        e: An error occurred while making the API request to Cloudflare.

    Returns:
        dict: The response from the Cloudflare API, usually containing all of the relevant information for the target DNS record.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}"
    try:
        payload = record
        payload['content'] = new_ip
        record_name = record.get('name')
        old_ip = record['content']
        logger.debug(f'Updating "{record_name}" from `{old_ip}` to `{new_ip}`...')
        data = make_api_request('PATCH', url, headers=cloudflare_headers(), payload=payload)
        
        if not data['success']:
            logger.error(f'The DNS record "{record_name}" was not updated successfully: \nErrors: {data.get('errors')} \nMessages: {data.get('messages')}')
            raise SystemExit(f'DNS record update was unsuccessful: \n\nErrors: {data.get('errors')} \n\nMessages: {data.get('messages')}')
        
        logger.debug(f'Successfully updated "{record_name}" to `{new_ip}`.')
        return data
    
    except Exception as e:
        logger.error(f'Error while updating DNS record "{record_name}": {repr(e)}')
        raise e
    
    
def update_zone_records(new_ip, zone_records):
    """Updates all of the DNS record for the target zone, specified by a predefined global variable, `ZONE_ID`."""
    logger.info(f'Updating all zone DNS records to {new_ip}...')
    for record in zone_records:
        update_record(record, ZONE_ID, new_ip)
    return len(zone_records) # Return the number of records that were updated


def main():
    current_ip_address = get_public_ip_address(PUBLIC_IP_API)
    zone_records = get_zone_records(ZONE_ID)
    current_zone_record_ips = [record['content'] for record in zone_records]
    
    new_ip_address = False
    for ip in current_zone_record_ips:
        if ip != current_ip_address:
            new_ip_address = True
            break

    if new_ip_address:
        logger.info(f'New IP address detected: {current_ip_address}.')
        num_updated = update_zone_records(current_ip_address, zone_records)
        logger.info(f'{num_updated} DNS records were successfully updated for zone "{ZONE_ID}".')
    else:
        logger.info('No new IP address detected.')
    

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Recieved keyboard interrupt. Quitting.')
        print(f'\nQuitting...')
        sys.exit()
