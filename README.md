# Cloudflare AutoDUC

A simple script that acts as an **automatic DNS Update Client** for Cloudflare DNS. It uses the [Cloudflare DNS API](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-update-dns-record) to update **all `A`/`AAAA` records in a particular Cloudflare DNS Zone** with the IP address of the machine running the script.

## Installation

To install, clone the repository and create a virtual environment:

```bash
git clone https://github.com/andersamer/cloudflare-autoDUC
cd cloudflare-autoDUC
python3 -m venv venv
```

Activate the virtual environment:

* macOS/Linux:

```bash
source venv/bin/activate
```

* Windows (Powershell):

```bash
venv\Scripts\Activate
```

Then, install the required dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Then, deactivate the virtual environment.

## Usage

Before running the script, make sure to create a `.env` file in the root of the repository with the following variables:

```python
CLOUDFLARE_API_EMAIL= # The email you use to log in to Cloudflare
CLOUDFLARE_API_TOKEN= # This can be found under Cloudflare Dashboard > Profile > Profile > API Tokens > Create Token
CLOUDFLARE_ZONE_ID= # This can be found under Cloudflare Dashboard > Your Domain > API > ZoneID. Remember: all DNS records under this ZoneID will be updated!
PUBLIC_IP_API=https://ifconfig.me # This works the best here. I haven't tested any other services yet.
```

To run the script, give execution privileges to `main.py`.

```bash
chmod +x main.py
```

From here on, you are free to run the script manually using `./main.py`. If you want to regularly run the DUC, you can do so by pointing a cronjob at `main.py` script (make sure to the path of python executable in the venv directory here):

```bash
# crontab -e
* * * * * /path/to/git/repo/venv/python /path/to/git/repo/main.py
# If you want to capture cron logs
* * * * * /path/to/git/repo/venv/python /path/to/git/repo/main.py >> /path/to/git/repo/cron.log 2>&1
```

Script logs will be recorded in `<repository root>/duc.log`.

## Issues & Contributions

Please feel free to open an issue if you run into any problems. If you'd like to see new features, open a pull request!
