import json
import socket
import sys
import datetime
import time
import os
import csv
import subprocess
import zipfile
from threading import Thread
import shutil
import multiprocessing
import argparse
from EPLAS_processing import *
from APLAS_processing import *
from OpenFOAM_processing import *
from dynamic_client import *
from static_client_prog import *
from periodic_static_client_prog import *

class UPC_Client:

	def __init__(self):
		self.upc = 'UPC client'

	def master_worker_info(info):
		master_information = []
		worker_information = []
		thread_information = []
		podman_thread_information = []
		with open(info) as json_file:
			data = json.load(json_file)
			for master in data['master']:
				master_information.append(master['IP_address'])
				master_information.append(master['port'])
				master_information.append(master['port_periodic'])
				#master_information.append(master['port2'])
			for worker in data['worker']:
				worker_information.append(worker['worker name'])
				worker_information.append(worker['number of thread'])
		with open(info) as json_file:
			data = json.load(json_file)
			for x in range(int(worker_information[1])):
				for thread in data['Thread-'+str(x+1)]:
					thread_information.append(thread['Docker ID-'+str(x+1)])
		with open(info) as json_file:
			data = json.load(json_file)
			for x in range(int(worker_information[1])):
				for thread in data['Thread-'+str(x+1)]:
					podman_thread_information.append(thread['Podman ID-'+str(x+1)])
		return master_information, worker_information, thread_information, podman_thread_information

	def worker_info(info):
		worker_information = []
		with open(info) as json_file:
			data = json.load(json_file)
			for worker in data['PC5']:
				worker_information.append(worker['IP_address'])
				worker_information.append(worker['port'])
		return worker_information

	def main(self):
		file = './master_worker_info_client.json'
		master_worker_information = UPC_Client.master_worker_info(file)
		master_information = master_worker_information[0]
		worker_information = master_worker_information[1]
		thread_information = master_worker_information[2]
		podman_thread_information = master_worker_information[3]
		worker_information_server = UPC_Client.worker_info(file)
		print ('\nFor EPLAS, press>> 1 \nFor APLAS, press>> 2\nFor Dynamic scheduling, press>> 3\nFor Static scheduling, press>> 4\nFor Periodic Static scheduling, press>> 5\nFor OpenFOAM, press>> 6\n')
		number = input('Press desire number = ')
		if str(number) == '1':
			print ("EPLAS job will process.")
			connect_master_eplas(master_information[0], master_information[1], worker_information[0])
		elif str(number) == '2':
			print ("APLAS job will process.")
			connect_master_aplas(master_information[0], master_information[1], worker_information[0], thread_information)
		elif str(number) == '3':
			dynamic_client_main(master_information[0], master_information[1], worker_information[0])
		elif str(number) == '4':
			thread_client_start = Thread(target = static_client_main, args = (master_information[0], master_information[1], worker_information[0]))
			thread_client_start1 = Thread(target = static_client_main1, args = (worker_information_server[0], worker_information_server[1]))
			thread_client_start.start()
			thread_client_start1.start()
		elif str(number) == '5':
			thread_client_start = Thread(target = periodic_static_client_main, args = (master_information[0], master_information[1], worker_information[0]))
			thread_client_start1 = Thread(target = periodic_static_client_main1, args = (worker_information_server[0], worker_information_server[1]))
			thread_client_start2 = Thread(target = periodic_static_client_main2, args = (master_information[0], master_information[2], worker_information[0]))
			thread_client_start.start()
			thread_client_start1.start()
			thread_client_start2.start()
		elif str(number) == '6':
			print ("OpenFOAM job will process.")
			connect_master_openfoam(master_information[0], master_information[1], worker_information[0], podman_thread_information)
		else:
			print ("Please type the correct number!!!")

	

if __name__ == "__main__":
	sys.setrecursionlimit(10**7)
	client = UPC_Client()
	client.main()