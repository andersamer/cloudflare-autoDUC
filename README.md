# Cloudflare AutoDUC

A simple script that acts as an **automatic DNS Update Client** for Cloudflare DNS. It uses the [Cloudflare DNS API](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-update-dns-record) to update a particular DNS record with the IP address of the current machine.

## Installation

To install, simply run the `install.sh` script. By default, the script and its configuration file will be copied to `~/.local/bin/cloudflare-autoDUC`. You can change the installation directory by editing the `DEST` variable in `install.sh`. Make sure to properly configure the script using the `conf.json` file after installing.

```json
{
    "AuthKey": "",
    "ZoneID": "",
    "Records": [
        {
            "id": "",
            "name": ""
        },
        {
            "id": "",
            "name": ""
        }
    ],
    "PublicAddressAPI": "https://ifconfig.me",
    "ListRecords": false
}
```

**Hint:** If you're having a hard time finding the record ID for the particular DNS record that you want to update, set `ListRecords` to `true` and run the script manually. If your `ZoneID` and `AuthKey` are set, then the script will print out all of the DNS records for that `ZoneID`. You can use that data to find the ID for the DNS record that you want to update.

If you don't want to use `install.sh`, you can point your own cronjob at the script yourself:

```shell
0 */3 * * * /usr/bin/python /path/to/script/directory/main.py
```
