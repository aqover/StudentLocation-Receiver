#!/usr/bin/python

import os
import time

TMP_FILE 	= "/var/tmp/git_pull"
DIR 		= "/home/fa/locating"

def git_pull(dir, file):
	os.system("cd " + dir)
	os.system("git pull > " + file)

def check_up_to_date(file):
	fd = open(file, "r")

	ck = 0
	for line in fd:
		data = line.strip()
		if data == "Already up-to-date.":
			ck = 1
			break

	fd.close()

	return (ck)

def do_post_update():
	os.system("sudo python post_update.py")
	os.system("sudo rm post_update.py")

def do_clear(file):
	os.system("rm " + file)

if __name__ == '__main__':
	while 1:
		git_pull(DIR, TMP_FILE)
		if not check_up_to_date(TMP_FILE):
			do_post_update()
			time.sleep(0.5)
			os.system("sudo /etc/init.d/locating restart")

		time.sleep(300)
		d0_clear(TMP_FILE)

# */5 * * * * /home/fa/locating/update.py