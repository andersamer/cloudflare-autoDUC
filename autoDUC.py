import sys
import requests
import logging

class AutoDUC:
    def __init__(self, api_key, zone_id, record_id, record_name, public_api):
        self.api_key = api_key
        self.zone_id = zone_id
        self.record_id = record_id
        self.record_name = record_name
        self.public_api = public_api

    def requestHeader(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def getCurrentPublicIP(self):
        try:
            response = requests.get(self.public_api)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch current IP from \"{self.public_api}\": {repr(e)}")
            raise SystemExit(e)
        return response.text
    
    def getRecords(self):
        url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records"

        try:
            response = requests.get(url, headers=self.requestHeader())
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve DNS records at zone \"{self.zone_id}\": {repr(e)}")
            raise SystemExit(e)

        return response.json()
    
    # Iterates through our list of records and returns the record that we want
    def getRecordIP(self):
        records = self.getRecords()
        for record in records["result"]:
            if(record["id"] == self.record_id):
                return record["content"]
        logging.error(f"DNS record \"{self.record_name}\"({self.record_id}) not found in zone \"{self.zone_id}\".")
        sys.exit()
    
    def updateRecord(self, new_ip):
        url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{self.record_id}"
        
        payload = {
            "content": new_ip,
            "name": self.record_name,
            "proxied": False,
            "type": "A",
            "comment": "",
            "ttl": 60 # Measured in seconds, must be at least 60
        }

        try:
            response = requests.put(url, json=payload, headers=self.requestHeader())
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to update DNS record \"{self.record_name}\"({self.record_id}): {repr(e)}")
            raise SystemExit(e)

        logging.info(f"DNS record \"{self.record_name}\"({self.record_id}) has been successfully updated to \"{new_ip}\".")
        return response.text
    