#! /usr/bin/env python

import os
import time
import tinys3
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def save_to_storage(path, conf):
	print("Uploading file to Amazon S3...")
	S3 = tinys3.Connection(conf['S3_KEY'], conf['S3_SECRET'], conf['S3_ENDPOINT'], tls=True)
	file_contents = open(path, 'rb')
	S3.upload(path, file_contents, conf['S3_BUCKET'])
	print("Done!")


def mysqldump(conf):
	BACKUP_DIR = "backups/" + conf['DB_NAME']
	FILE_DEST = "{0}/{1}-{2}.sql".format(
		BACKUP_DIR, conf['DB_NAME'], time.strftime('%Y-%m-%d')
	)

	if not os.path.exists(BACKUP_DIR):
	    os.makedirs(BACKUP_DIR)

	command = "mysqldump -u {user} -p{password} {database} > {destination} | gzip -c > {destination}.gz"

	os.system(command.format(
		user=conf['DB_USER'],
		password=conf['DB_PASS'],
		database=conf['DB_NAME'],
		destination=FILE_DEST
	))
	print(conf['DB_NAME'] + ", backup completed.")

	# Save the file in storage.
	save_to_storage(FILE_DEST, conf)


# Create one dump for each site in the configuration file.
for site, config in config.items():
	if not site == 'DEFAULT':
  		mysqldump(config)