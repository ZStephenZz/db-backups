
# DBBackup

Python script to create backups and save them to AmazonS3.

## Installation
Install dependencies
```bash
pip install -r requirements.txt
```

Create a config.ini file and fill in your S3 key and passwords.
```bash
cp config.example.ini config.ini
```


## Run as cron job
* Every 24 hours
```bash
sudo chmod a+x dbbackup.py

crontab -e

0 0 * * * /usr/bin/python /path/to/dbbackup.py >/dev/null 2>&1
```
