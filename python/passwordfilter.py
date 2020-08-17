#!/usr/bin/env python

# this is a filter meant to be used with a logfile containing
# debug output from wpa_supplicant or reaver, which extracts
# cryptographic values of interest and tries to run pixiewps
# with them. input is passed on stdin.

import sys, os, re

class Data():
	def __init__(self):
		self.pke = ''
		self.pkr = ''
		self.e_nonce = ''


	def __repr__(self):
		return \
			"WPS Pin = " + self.pke + "\n" \
			"AP Name = " + self.pkr + "\n" \
			"Passphrase = " + self.e_nonce + "\n"

def process_wpa_supplicant_line(data, line):
	def get_hex(line):
		a = line.split('\n', 3)
		return a[2].replace(' ', '')

        pattern = "'(.*?)'"

	if line.startswith('[+]'):
		if '[+] WPA PSK:' in line:
              		data.e_nonce  = re.search(pattern, line).group(1)
		elif 'AP SSID:' in line:
			data.pkr  = re.search(pattern, line).group(1)
		elif 'WPS PIN:' in line:
			data.pke  = re.search(pattern, line).group(1)
		

def got_all_pixie_data(data):
	return data.pke and data.pkr and data.e_nonce 

if __name__ == '__main__':

	data = Data()

	while True:
		line = sys.stdin.readline()
		if line == '': break
		process_wpa_supplicant_line(data, line.rstrip('\n'))

	print(data)


