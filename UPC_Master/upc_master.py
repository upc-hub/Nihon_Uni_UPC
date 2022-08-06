import argparse
import multiprocessing
import subprocess
import json
from master_operation_aplas import *
from master_operation_eplas import *
from master_operation_openfoam import *
from master_connection import *
from master_connection_openfoam import *
from dynamic_scheduling import *
from static_scheduling import *
from periodic_static_scheduling import *

class UPC_Master:

	def __init__(self):
		self.upc = 'UPC master'

	def master_info(info):
		master_information = []
		with open(info) as json_file:
			data = json.load(json_file)
			for master in data['master']:
				master_information.append(master['IP_address'])
				master_information.append(master['port'])
				master_information.append(master['number of worker'])
				master_information.append(master['port_periodic'])
		return master_information

	def worker_info(info):
		worker_ip = []
		worker_thread = []
		worker_port = []
		num_of_worker = UPC_Master.master_info(info)
		with open(info) as json_file:
			data = json.load(json_file)
			for x in range(int(num_of_worker[2])):
				for worker in data['worker-'+str(x+1)]:
					worker_ip.append(worker['IP_address'])
					worker_thread.append(worker['max_threads'])
					worker_port.append(worker['port'])
		return worker_ip, worker_thread, worker_port

	def main(self):
		eplas_dir = './EPLAS/newJobs/'			#EPLAS job directory (EPLAS system assigns jobs through pCloud-https)
		aplas_dir = './APLAS/newJobs/'			#APLAS job directory (APLAS system assigns jobs through FTP)
		local_dir = './local_user/newJobs/'		#Local user job directory (local user assigns jobs through LAN_static-https)
		tem_queue = './temporary_queue/'		#group all submitted jobs from various system
		com_queue = './common_queue/'			#renamed all submitted jobs Queue
		file = './master_worker_info.json'

		print ('\n-> For EPLAS, press = 1 \n-> For APLAS, press = 2 \n-> For Local_user, press = 3 \n-> For Static scheduling, press = 4 \n-> For Dynamic scheduling, press = 5 \n-> For Periodic static scheduling, press = 6 \n-> For OpenFOAM, press = 7 \n')
		number = input('Press desire number = ')
		if str(number) == '1':
			print ("EPLAS jobs will be processed in UPC system.")
			print ("\n")
			master_information = UPC_Master.master_info(file)
			worker_information = UPC_Master.worker_info(file)
			Thread(target = master_connection_open_close, args=(master_information[0], master_information[1], str(number), worker_information[2])).start()
			Thread(target = transform_to_upc_job_eplas, args=(eplas_dir, aplas_dir, local_dir, tem_queue, com_queue, worker_information[0], 'noThreads', master_information[0])).start()
		
		elif str(number) == '2':
			print ("APLAS jobs will be processed in UPC system.")
			master_information = UPC_Master.master_info(file)
			worker_information = UPC_Master.worker_info(file)
			Thread(target =master_connection_open_close, args=(master_information[0], master_information[1], str(number), 'worker_port')).start()
			Thread(target =transform_to_upc_job_aplas, args=(eplas_dir, aplas_dir, local_dir, tem_queue, com_queue, worker_information[0], worker_information[1], master_information[0])).start()

		elif str(number) == '3':
			print ("Local_user job will test.")

		elif str(number) == '4':
			print ("Static scheduling will test.")
			master_information = UPC_Master.master_info(file)
			static_main(master_information[0], master_information[1])

		elif str(number) == '5':
			print ("Dynamic scheduling will test.")
			master_information = UPC_Master.master_info(file)
			dynamic_main(master_information[0], master_information[1])

		elif str(number) == '6':
			print ("Periodic checkpointing will test.")
			master_information = UPC_Master.master_info(file)
			periodic_static_main(master_information[0], master_information[1], master_information[3])

		elif str(number) == '7':
			print ("OpenFOAM jobs will be processed in UPC system.")
			master_information = UPC_Master.master_info(file)
			worker_information = UPC_Master.worker_info(file)
			Thread(target =master_connection_open_close_openfoam, args=(master_information[0], master_information[1], str(number), 'worker_port')).start()
			Thread(target =transform_to_upc_job_openfoam, args=(eplas_dir, aplas_dir, local_dir, tem_queue, com_queue, worker_information[0], worker_information[1], master_information[0])).start()


		else:
			print ('Please choose the correct number')

if __name__ == "__main__":
	master = UPC_Master()
	master.main()