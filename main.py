from __future__ import print_function
import os
import time
import sys

from buttercoin.client import ButtercoinClient

from config import api_key, api_secret

is_in_a_terminal = sys.stdin.isatty()


class colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m' if not is_in_a_terminal else ''
	WARNING = '\033[93m'
	FAIL = '\033[91m' if not is_in_a_terminal else ''
	ENDC = '\033[0m' if not is_in_a_terminal else ''


def clear_screen():
	if sys.platform != "win32":
		os.system("clear")
	else:
		os.system("cls")


client = ButtercoinClient(api_key=api_key,
						  api_secret=api_secret,
						  mode="production")

ticker = client.get_ticker()
balance = client.get_balances()
count = 0
frequency = 1.0
old = {'last': 0, 'bid': 0, 'ask': 0}
while True:
	try:
		count += 1
		changed = False
		"""Formatting"""

		currency = ticker['currency']
		last = ticker['last']
		bid = ticker['bid']
		ask = ticker['ask']

		if last < old['last']:
			old['last'] = last
			last = colors.FAIL + last + colors.ENDC
			changed = True
		elif last > old['last']:
			old['last'] = last
			last = colors.OKGREEN + str(last) + colors.ENDC
			changed = True

		if bid < old['bid']:
			old['bid'] = bid
			bid = colors.FAIL + str(bid) + colors.ENDC
			changed = True
		elif bid > old['bid']:
			old['bid'] = bid
			bid = colors.OKGREEN + str(bid) + colors.ENDC
			changed = True

		if ask < old['ask']:
			old['ask'] = ask
			ask = colors.FAIL + str(ask) + colors.ENDC
			changed = True
		elif ask > old['ask']:
			old['ask'] = ask
			ask = colors.OKGREEN + str(ask) + colors.ENDC
			changed = True

		if changed or True:
			clear_screen()
			print("Current balances: ${0}, {1}BTC".format(balance['USD'], balance['BTC']))
			print(
				"Last Buy: ${1}\nLast Bid: ${2}\nCurrent Asking Price: ${3}\nTime: {4}".format(currency, last, bid, ask,
																							   time.strftime(
																								   "%H:%M:%S")))
			print("{0}BTC -> USD (current market price): ${1}".format(round(balance['BTC'], 8),
																	  round(balance['BTC'] * old['bid'], 4)))
			print("${0} -> BTC (current market price): {0}BTC".format(round(balance['USD'], 2),
																	  round(balance['USD'] / old['ask'], 8)))
		# print("Update {0}".format(count))

		time.sleep(frequency)

	except KeyboardInterrupt:
		clear_screen()

		temp = raw_input("Would you like to quit or update prices? quit/update: ").lower()
		if temp == "update":
			clear_screen()
			temp = raw_input(
				"Enter a new USD balance or hit enter to continue with old balance of {0}\n ".format(balance['USD']))
			if temp != '':
				balance['USD'] = round(float(temp), 2)

			clear_screen()
			temp = raw_input(
				"Enter a new BTC balance or hit enter to continue with old balance of {0}\n ".format(balance['BTC']))
			if temp != '':
				balance['BTC'] = round(float(temp), 8)

			clear_screen()
			temp = raw_input("Enter a new frequency for update, currently set to {0} seconds\n".format(frequency))
			if temp != '':
				frequency = float(temp)

			clear_screen()
			print("Values updated")
			continue
		elif temp == "quit":
			break

clear_screen()