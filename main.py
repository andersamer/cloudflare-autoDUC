#!/usr/bin/python3

import os
import sys
import logging
import json
from autoDUC import AutoDUC

def initLogging(log_path):
    # Initialize logging
    logging.basicConfig(filename=log_path, format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

def getConfig(config_path):
    try:
        with open(config_path, "r") as config_JSON:
            config_dict = json.load(config_JSON)
            config_JSON.close()
            return config_dict
    except FileNotFoundError as e:
        logging.error("Configuration file not found, please check file path")
        raise SystemExit(e)

def main():
    # By default, generate paths to the log file and the config file to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, "update.log")
    config_path = os.path.join(script_dir, "conf.json")

    initLogging(log_path) # Initialize logging
    Config = getConfig(config_path) # Load the config
    
    # This is a quick-and-dirty fix for handling multiple DNS records. Will have to come 
    # up with a more robust solution soon
    for record in Config["Records"]:
        duc = AutoDUC(Config["AuthKey"], Config["ZoneID"], record["id"], record["name"], Config["PublicAddressAPI"])
        
        # Print out all records if specified in config
        if Config["ListRecords"]:
            print(duc.getRecords())
            sys.exit()

        # Check to make sure that the IP has changed before attempting to update
        current_public_ip = duc.getCurrentPublicIP()
        current_dns_ip = duc.getRecordIP()
        
        if current_public_ip != current_dns_ip:
            logging.info(f"New public IP address detected ({current_public_ip}) Attempting to update DNS...")
            duc.updateRecord(current_public_ip)
            # sys.exit()
        else:
            # Removing this logging statement because it's noisy
            # logging.info(f"Current IP address has not changed ({current_public_ip}). No update will be attempted.")
            pass

    sys.exit()

if __name__ == "__main__":
    main()
