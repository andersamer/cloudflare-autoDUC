# Cloudflare AutoDUC

A simple script that acts as an **automatic DNS Update Client** for Cloudflare DNS. It uses the [Cloudflare DNS API](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-update-dns-record) to update a particular DNS record with the IP address of the current machine.

## Installation

To install, simply run the `install.sh` script. `autoDUC.py` will be copied to `~/.local/bin/cloudflare-autoDUC`, and the installer will create a file called `.env` file in that directory. Make sure you define the following variables in your `.env`:

* `CLOUDFLARE_API_KEY` - Your Cloudflare API key.
* `CLOUDFLARE_ZONE_ID` - The zone ID of the DNS record.
* `TARGET_DNS_RECORD_ID` - The ID of the DNS record you want to change. You can see all of your DNS record ID's by listing all of the records for a particular zone. (I made a function for this called `getRecords()` to make this part easier. Uncomment the line in the script and run it manually to see all of your records).
* `PUBLIC_IP_API_URL` - The URL of the site you want to query to get your current public IP. [ifconfig.me](https://ifconfig.me) has always been a good option.
* `TARGET_DNS_RECORD_NAME` - The name of the DNS record you want to change.
