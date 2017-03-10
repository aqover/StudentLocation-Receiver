#!/usr/bin/python

import os

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

def clear(file):
	os.system("rm " + file)

if __name__ == '__main__':
	git_pull(DIR, TMP_FILE)
	if not check_up_to_date(TMP_FILE):
		do_post_update()
		os.system("sudo /etc/init.d/locating restart")

	clear()

# */5 * * * * /home/fa/locating/update.py