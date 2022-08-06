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
from dynamic_client import *

class UPC_Client:

	def __init__(self, master_ip, master_port, worker_name, worker_thread):
		self.upc = 'UPC client'
		self.ip_addr = master_ip
		self.port = master_port
		self.worker = worker_name
		self.threads = worker_thread

	def request_worker_docker_ID(worker_name, worker_thread):
		docker_id = []
		for x in range(int(worker_thread)):
			IDs = input('Please enter ('+str(worker_name+') docker ID-'+str(x)+' : '))
			docker_id.append(IDs)
		return docker_id

	def main(self):
		print ('\nFor EPLAS, press>> 1 \nFor APLAS, press>> 2\nFor Dynamic scheduling, press>> 3\n')
		number = input('Press desire number = ')
		if str(number) == '1':
			print ("EPLAS job will process.")
			connect_master_eplas(str(self.ip_addr), int(self.port), str(self.worker))
		elif str(number) == '2':
			print ("APLAS job will process.")
			IDs = UPC_Client.request_worker_docker_ID(self.worker, self.threads)
			connect_master_aplas(str(self.ip_addr), int(self.port), str(self.worker), IDs)
		elif str(number) == '3':
			dynamic_client_main(str(self.ip_addr), int(self.port), str(self.worker))
		else:
			print ("Please type the correct number!!!")

	

if __name__ == "__main__":
	sys.setrecursionlimit(10**7)
	parser = argparse.ArgumentParser(description="Passing UPC Client's arguments")

	parser.add_argument("-ip", "--host", help="Enter host/IP address of the UPC master")
	parser.add_argument("-p", "--port", help="Enter port number of the UPC master")
	parser.add_argument("-n", "--name", help="Enter worker name")
	parser.add_argument("-t", "--thread", help="Enter number of threads of this worker")

	args = parser.parse_args()
	master_ip = args.host
	master_port = args.port
	worker_name = args.name
	worker_thread = args.thread

	client = UPC_Client(master_ip, master_port, worker_name, worker_thread)
	client.main()