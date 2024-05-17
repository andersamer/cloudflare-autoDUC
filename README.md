# Cloudflare AutoDUC

A simple script that acts as an **automatic DNS Update Client** for Cloudflare DNS. It uses the [Cloudflare DNS API](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-update-dns-record) to update a particular DNS record with the IP address of the current machine.

## Installation

To install, simply run the `install.sh` script. By default, the script and its configuration file will be copied to `~/.local/bin/cloudflare-autoDUC`. You can change the installation directory by editing the `DEST` variable in `install.sh`. Make sure to properly configure the script using [the `conf.json` file](https://github.com/andersamer/cloudflare-autoDUC/blob/main/conf.json) after installing.

```json
{
    "AuthKey": "",   // Your Cloudflare API key
    "ZoneID": "",    // The Zone ID of the record you wish to update
    "Record":{
        "id": "",    // The ID of the record you wish to update
        "domain": "" // The domain of the reocrd you wish to update
    },
    "PublicAddressAPI": "https://ifconfig.me", // A URL for an API that you can 
                                               // use to check your current 
                                               // public IP
    "ListRecords": false // Set this to `true` if you want the script to print
                         // all of the records for a particular zone. (This is 
                         // especially useful for finding your Record ID)
}
```

If you don't want to use `install.sh`, you can point your own cronjob at the script yourself:

```shell
0 */3 * * * /usr/bin/python /path/to/script/directory/main.py
```
