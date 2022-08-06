from datetime import date
from threading import Thread
from aplas_job_operation import *
import shutil
import datetime
import time
import schedule
import os
import json
import subprocess
import zipfile
import socket
import traceback
import csv
import filetype
import sys
import multiprocessing
import requests
import json
import os
import codecs
import subprocess
global token_counter_today
global available_list           																										#current available worker list connected to UPC Master
global csv_file

token_counter_today = 0
available_list = []
csv_file = './thread_proportional_time.csv'

def transform_to_upc_job_aplas(EPLAS_dir, APLAS_dir, local_dir, all_job_dir, com_job_dir, ip, threads, serverIP):                                          			#submitted jobs are renamed to be compactible with the system requirements e.g. currentToken_ddmmyyyy_jobName
	global token_counter_today
	global available_list
	global pc6_limitt, pc5_limitt, pc4_limitt, pc3_limitt, pc2_limitt, pc1_limitt
	global ip6, ip5, ip4, ip3, ip2, ip1
	global hostIP
	hostIP = serverIP
	pc6_limitt = 1
	pc5_limitt = 1
	pc4_limitt = 1
	pc3_limitt = 1
	pc2_limitt = 1
	pc1_limitt = 1
	ip6 = ''
	ip5 = ''
	ip4 = ''
	ip3 = ''
	ip2 = ''
	ip1 = ''
	print ("Currently available worker : ", available_list)
	try:
		for x in range(6):
			if x==0:
				pc1_limitt = threads[x]
				ip1 = ip[x]
			elif x==1:
				pc2_limitt = threads[x]
				ip2 = ip[x]
			elif x==2:
				pc3_limitt = threads[x]
				ip3 = ip[x]
			elif x==3:
				pc4_limitt = threads[x]
				ip4 = ip[x]
			elif x==4:
				pc5_limitt = threads[x]
				ip5 = ip[x]
			else:
				pc6_limitt = threads[x]
				ip6 = ip[x]
	except IndexError:
		print ("Already assigned maximum threads to the available workers")	

	aplas_job_zipping(APLAS_dir, all_job_dir, com_job_dir)
	
	for file_name in os.listdir(all_job_dir):
		job_name = str(file_name)
		if (job_name[0].isdigit()):																										#check renamed or not
			print ()
		token_counter_today = token_counter_today + 1
		token = initiate_job_token_for_renaming()
		os.rename(os.path.join(all_job_dir, file_name), os.path.join(all_job_dir,token+'_'+file_name))          						#renaming process
		shutil.move(all_job_dir+token+'_'+file_name, com_job_dir)											    						#renamed jobs are moved to common Queue
		start = total_second()
		zip_extract_info(token+'_'+file_name, com_job_dir)      													   					#extract jobs's zips
		end = total_second()
		job_preparation_time = convert(int(end)-int(start))
		record_csv(csv_file, str(job_preparation_time)+ " job_preparation_time of"+token+'_'+file_name)      							#extract jobs's zips
	
	check_tick = True
	while check_tick:
		current_total = 0
		for entry_name in os.listdir(APLAS_dir):
			current_total = current_total+1
		if current_total>=1:
			time.sleep(5)
			print ("New job is detected.")
			check_tick = False
			transform_to_upc_job_aplas(EPLAS_dir, APLAS_dir, local_dir, all_job_dir, com_job_dir, ip, threads, serverIP)
		else:
			time.sleep(10)
			print ("No new job is detected.")
			check_tick=True

#schedule.every(10).seconds.do(transform_to_upc_job)                  																	#UPC Master checks jobs arrive from UPC Web Server every 30 seconds

def initiate_job_token_for_renaming():								   																	#generate currentToken for the submitted jobs
	global token_counter_today
	if check_day_change():                                 																				#check change to the next day or not for reseting the token
		token_counter_today = 0
	today_date = date.today()
	day = str(today_date.day)
	month = str(today_date.month)
	year = str(today_date.year)
	generate_token = str(token_counter_today)+"_"+day+month+year
	return generate_token

def check_day_change():                                    																				#check change to the next day or not			  						
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute
	second = datetime.datetime.now().second
	if (hour == '23' and minute == '59' and second == '59'):
		return True

def zip_extract_info(job_name, directory):                      																		#extract job's zip file and read the Metadata of job 
	zip_name = job_name.split('.')
	zip_name_container = job_name.split('_')
	aplas_name_container = zip_name[0].split('-')
	aplas_name_container1 = aplas_name_container[0].split('_')
	if aplas_name_container1[2]=='aplas':
		file_name = directory+job_name
		file_name1 = directory+zip_name[0]
		subprocess.call(['mkdir', file_name1])
		subprocess.call(['mv', file_name, file_name1+'/'])
		file_name2 = file_name1+'/'+job_name
		
		zip_ref = zipfile.ZipFile(file_name2)
		extracted = zip_ref.namelist()
		name_of_job = extracted[0].split('/')
		zip_ref.extractall(file_name1)
		zip_ref.close()
		os.remove(file_name2)
		subprocess.call(['chmod', '777', '-R', file_name1])
		job_dir = directory+zip_name[0]
		check_container_require(zip_name_container[0], job_dir, zip_name[0])
		#print ("APLAS............")
	else:
		file_name = directory+job_name
		zip_ref = zipfile.ZipFile(file_name)
		extracted = zip_ref.namelist()
		name_of_job = extracted[0].split('/')
		zip_ref.extractall(directory)
		zip_ref.close()
		os.rename(os.path.join(directory, name_of_job[0]), os.path.join(directory,zip_name[0]))       									#extracted zip's name may be different from the renames by the System
		os.remove(file_name)                                                                          									#previous zip files are removed
		subprocess.call(['chmod', '777', '-R', directory])
		job_dir = directory+zip_name[0]
		check_container_require(zip_name_container[0], job_dir, zip_name[0])                          									#check container is needed to build or not by reading job's Metadata

def check_container_require(zip_name_container, job_dir, sys_name):
	global available_list
	container_queue = './container_queue/'
	common_queue = './common_queue/'
	docker_template = './Dockerfile'               													  									#Dokerfile template if job is necessary to build a container
	base_directory = './'
	detect_system = sys_name.split('_')
	detect_systema = sys_name.split('-')
	detect_systemb = detect_systema[0].split('_')
	local = detect_system[2]
	if(local[0]=='l'):                                                             					  									#differentiate between local and outsider systems
		detect_system[2]='local_user'

	elif detect_systemb[2]=="aplas":
		aplas_job_preparation(common_queue, detect_systemb, sys_name, base_directory, detect_systema, container_queue, job_dir)
		available_worker = current_available_worker()                      																#checked is there any worker already connected to master before jobs arrived
		if available_worker=="":                                           																#if there is no available worker, assign null
			print ()
		else:
			try:
				print (available_list[0], "<<<<this worker will be poped from the list.")             									#If a job is assigned to the worker, that worker is removed from the available worker list.
				pop_worker(available_list[0])
			except IndexError:
				print ()

	else:
		print ("")

def update_job_list(job_name, status):                                                 																		#record job and worker status
	job_list_loc = './job_list_status.csv'
	with open(job_list_loc, 'a') as csvfile1:
		fieldnames1 = ['Job', 'Status']
		writerpp1 = csv.DictWriter(csvfile1, fieldnames=fieldnames1)
		writerpp1.writerow({'Job': job_name, 'Status': status})

def current_available_worker():                                                        																		#check is there any available worker in the list for the current job
	global available_list
	try:
		return available_list[0]
	except IndexError:
		null_str = ""
		return null_str
		print ("All worker are busy.")
	
def update_worker(pc):                                                                 																		#connected workers update 
	global available_list
	global pc6_limitt, pc5_limitt, pc4_limitt, pc3_limitt, pc2_limitt, pc1_limitt
	container_queue = './container_queue/'
	base_directory = './'
	print (available_list, "Check job by worker")
	print ("This is the length", len(available_list))
	if len(available_list)==0:                                                         																		#check connected worker is already in the available worker list
		push_worker(pc)                                                                																		#if not, that worker is added to the available worker list
		print ("This is the first time join.")                                        
	else:                                                                              																		#connected worker is already in the avaialable list
		break_out_flag1 = False
		print ("This is not the first time.")
		for worker in range(0, len(available_list)):
			if pc in available_list[worker]:
				break_out_flag1 = True
				break
		if break_out_flag1:
			print (pc, "This worker is already added.")
		else:
			push_worker(pc)
			print (pc, "This worker is added to the available list.")
	send_job = ""
	send_worker = ""
	no_job = ""
	no_worker = ""
	with open('./job_list_status.csv') as f:          																		#update job and worker list (this time is adding current connected worker to the status file.)
		reader = csv.reader(f)
		lines = list(reader)
		print (lines, "lines ************************")
		print ("")
		print (len(lines), "length of lines ************************")
		pc1_count = 1
		pc1_limit = pc1_limitt
		pc2_count = 1
		pc2_limit = pc2_limitt
		pc3_count = 1
		pc3_limit = pc3_limitt
		pc4_count = 1
		pc4_limit = pc4_limitt
		pc5_count = 1
		pc5_limit = pc5_limitt
		pc6_count = 1
		pc6_limit = pc6_limitt
		try:
			if pc=="PC4":
				for entry_name in os.listdir(base_directory+'PC44/'):
					if pc4_count>pc4_limit:
						break
					else:
						shutil.move(base_directory+'PC44/'+entry_name, base_directory+"PC4")
						print ('PC44 moved jobs.')
						pc4_count = pc4_count+1
			elif pc=="PC5":
				for entry_name in os.listdir(base_directory+'PC55/'):
					if pc5_count>pc5_limit:
						break
					else:
						shutil.move(base_directory+'PC55/'+entry_name, base_directory+"PC5")
						print ('PC55 moved jobs.')
						pc5_count = pc5_count+1
			elif pc=="PC6":
				for entry_name in os.listdir(base_directory+'PC66/'):
					if pc6_count>pc6_limit:
						break
					else:
						shutil.move(base_directory+'PC66/'+entry_name, base_directory+"PC6")
						pc6_count = pc6_count+1
			elif pc=="PC3":
				for entry_name in os.listdir(base_directory+'PC33/'):
					if pc3_count>pc3_limit:
						break
					else:
						shutil.move(base_directory+'PC33/'+entry_name, base_directory+"PC3")
						pc3_count = pc3_count+1
			elif pc=="PC1":
				for entry_name in os.listdir(base_directory+'PC11/'):
					if pc1_count>pc1_limit:
						break
					else:
						shutil.move(base_directory+'PC11/'+entry_name, base_directory+"PC1")
						pc1_count = pc1_count+1
			elif pc=="PC2":
				for entry_name in os.listdir(base_directory+'PC22/'):
					if pc2_count>pc2_limit:
						break
					else:
						shutil.move(base_directory+'PC22/'+entry_name, base_directory+"PC2")
						pc2_count = pc2_count+1
			else:
				print ("csv file error.........................")
			return "aa", "bb"

		except IndexError:
			send_job = "No job"
			send_worker = "No worker"
			print ("There is no job.")
			return "aa", send_worker

def check_job_to_execute_aplas(connection, ip, pc_name):                               
	global pc6_limitt, pc5_limitt, pc4_limitt, pc3_limitt, pc2_limitt, pc1_limitt
	global ip6, ip5, ip4, ip3, ip2, ip1
	container_queue = './container_queue/'
	base_directory = './'
	if len(os.listdir(base_directory+pc_name))== 0:                                 																		#each connected worker check its correspondance queue for the jobs exist or not
		print ("empty")
		connection.sendall("wait".encode("utf8"))                                   																		#if there is no job, send  'wait' message by Master to that worker
	else:                                                                           																		#if there are jobs, grab only the first job in its queue
		aplas_directory = './'+pc_name+'/'
		#ip6 = '172.28.235.227'
		#ip5 = '172.28.235.245'
		#ip4 = '172.28.235.212'
		#ip3 = '172.28.235.205'
		#ip2 = '192.168.0.170'
		#ip1 = '172.28.235.226'
		ip = ""
		#pc6_limitt = 6
		#pc5_limitt = 5
		#pc4_limitt = 4
		#pc3_limitt = 1
		#pc2_limitt = 1
		#pc1_limitt = 1
		counter = 0
		current_total = 0
		token_jobs = []	
		for entry_name in os.listdir(aplas_directory):
			current_total = current_total+1

		print ("Current total.......................", current_total)
		if pc_name=="PC6" and current_total<pc6_limitt:
			ip = ip6
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
			print (token_jobs)
		elif pc_name=="PC5" and current_total<pc5_limitt:
			ip = ip5
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		elif pc_name=="PC4" and current_total<pc4_limitt:
			ip = ip4
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		elif pc_name=="PC3" and current_total<pc3_limitt:
			ip = ip3
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		elif pc_name=="PC2" and current_total<pc2_limitt:
			ip = ip2
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		elif pc_name=="PC1" and current_total<pc1_limitt:
			ip = ip1
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		else:
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
				counter = counter+1
				if pc_name=="PC6" and counter==pc6_limitt:
					ip = ip6
					break
				elif pc_name=="PC5" and counter==pc5_limitt:
					ip = ip5
					break
				elif pc_name=="PC4" and counter==pc4_limitt:
					ip = ip4
					break
				elif pc_name=="PC3" and counter==pc3_limitt:
					ip = ip3
					break
				elif pc_name=="PC2" and counter==pc2_limitt:
					ip = ip2
					break
				elif pc_name=="PC1" and counter==pc1_limitt:
					ip = ip1
					break
				else:
					print ("Unknown worker......")
			print (token_jobs)

		if len(token_jobs)==1:
			connection.sendall("one".encode("utf8"))
			one_thread(pc_name, connection, aplas_directory, token_jobs[0], ip, pc_name[2]+'004')
		elif len(token_jobs)==2:
			connection.sendall("two".encode("utf8"))
			two_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], ip, pc_name[2]+'004', pc_name[2]+'005')
		elif len(token_jobs)==3:
			connection.sendall("three".encode("utf8"))
			three_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006')
		elif len(token_jobs)==4:
			connection.sendall("four".encode("utf8"))
			four_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007')
		elif len(token_jobs)==5:
			connection.sendall("five".encode("utf8"))
			five_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008')
		elif len(token_jobs)==6:
			connection.sendall("six".encode("utf8"))
			six_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009')
		elif len(token_jobs)==7:
			connection.sendall("seven".encode("utf8"))
			seven_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], token_jobs[6], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009', pc_name[2]+'010')
		elif len(token_jobs)==8:
			connection.sendall("eight".encode("utf8"))
			eight_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], token_jobs[6], token_jobs[7], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009', pc_name[2]+'010', pc_name[2]+'011')
		elif len(token_jobs)==9:
			connection.sendall("nine".encode("utf8"))
			nine_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], token_jobs[6], token_jobs[7], token_jobs[8], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009', pc_name[2]+'010', pc_name[2]+'011', pc_name[2]+'012')
		else:
			connection.sendall("ten".encode("utf8"))
			ten_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], token_jobs[6], token_jobs[7], token_jobs[8], token_jobs[9], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009', pc_name[2]+'010', pc_name[2]+'011', pc_name[2]+'012', pc_name[2]+'013')

def one_thread(pc_name, connection, directory, job1, ip, port1):

	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	send_one_proce.start()
	result1_proce.start()

def two_thread(pc_name, connection, directory, job1, job2, ip, port1, port2):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	result1_proce.start()
	result2_proce.start()

def three_thread(pc_name, connection, directory, job1, job2, job3, ip, port1, port2, port3):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()

def four_thread(pc_name, connection, directory, job1, job2, job3, job4, ip, port1, port2, port3, port4):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()

def five_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, ip, port1, port2, port3, port4, port5):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()

def six_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, ip, port1, port2, port3, port4, port5, port6):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()

def seven_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, job7, ip, port1, port2, port3, port4, port5, port6, port7):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	send_seven_proce = multiprocessing.Process(target = send_seven, args=(connection, directory, job7, ip, port7))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	result7_proce = multiprocessing.Process(target = result7, args=(connection, port7, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	send_seven_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()
	result7_proce.start()

def eight_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, job7, job8, ip, port1, port2, port3, port4, port5, port6, port7, port8):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	send_seven_proce = multiprocessing.Process(target = send_seven, args=(connection, directory, job7, ip, port7))
	send_eight_proce = multiprocessing.Process(target = send_eight, args=(connection, directory, job8, ip, port8))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	result7_proce = multiprocessing.Process(target = result7, args=(connection, port7, pc_name))
	result8_proce = multiprocessing.Process(target = result8, args=(connection, port8, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	send_seven_proce.start()
	send_eight_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()
	result7_proce.start()
	result8_proce.start()

def nine_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, job7, job8, job9, ip, port1, port2, port3, port4, port5, port6, port7, port8, port9):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	send_seven_proce = multiprocessing.Process(target = send_seven, args=(connection, directory, job7, ip, port7))
	send_eight_proce = multiprocessing.Process(target = send_eight, args=(connection, directory, job8, ip, port8))
	send_nine_proce = multiprocessing.Process(target = send_nine, args=(connection, directory, job9, ip, port9))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	result7_proce = multiprocessing.Process(target = result7, args=(connection, port7, pc_name))
	result8_proce = multiprocessing.Process(target = result8, args=(connection, port8, pc_name))
	result9_proce = multiprocessing.Process(target = result9, args=(connection, port9, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	send_seven_proce.start()
	send_eight_proce.start()
	send_nine_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()
	result7_proce.start()
	result8_proce.start()
	result9_proce.start()

def ten_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, job7, job8, job9, job10, ip, port1, port2, port3, port4, port5, port6, port7, port8, port9, port10):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	send_seven_proce = multiprocessing.Process(target = send_seven, args=(connection, directory, job7, ip, port7))
	send_eight_proce = multiprocessing.Process(target = send_eight, args=(connection, directory, job8, ip, port8))
	send_nine_proce = multiprocessing.Process(target = send_nine, args=(connection, directory, job9, ip, port9))
	send_ten_proce = multiprocessing.Process(target = send_ten, args=(connection, directory, job10, ip, port10))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	result7_proce = multiprocessing.Process(target = result7, args=(connection, port7, pc_name))
	result8_proce = multiprocessing.Process(target = result8, args=(connection, port8, pc_name))
	result9_proce = multiprocessing.Process(target = result9, args=(connection, port9, pc_name))
	result10_proce = multiprocessing.Process(target = result10, args=(connection, port10, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	send_seven_proce.start()
	send_eight_proce.start()
	send_nine_proce.start()
	send_ten_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()
	result7_proce.start()
	result8_proce.start()
	result9_proce.start()
	result10_proce.start()

def record_csv(csv_file, data):
	with open(csv_file, 'a')as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([data])

def total_second():
    start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
    start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
    start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
    return start_total

def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)

def send_one(connection, directory, job1, ip, port1):
	thread_job_send(directory, job1, ip, port1)

def send_two(connection, directory, job2, ip, port2):
	thread_job_send(directory, job2, ip, port2)

def send_three(connection, directory, job3, ip, port3):
	thread_job_send(directory, job3, ip, port3)

def send_four(connection, directory, job4, ip, port4):
	thread_job_send(directory, job4, ip, port4)

def send_five(connection, directory, job5, ip, port5):
	thread_job_send(directory, job5, ip, port5)

def send_six(connection, directory, job6, ip, port6):
	thread_job_send(directory, job6, ip, port6)

def send_seven(connection, directory, job7, ip, port7):
	thread_job_send(directory, job7, ip, port7)

def send_eight(connection, directory, job8, ip, port8):
	thread_job_send(directory, job8, ip, port8)

def send_nine(connection, directory, job9, ip, port9):
	thread_job_send(directory, job9, ip, port9)

def send_ten(connection, directory, job10, ip, port10):
	thread_job_send(directory, job10, ip, port10)

def thread_job_send(directory, job, ip, port):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job, ip, port])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread job sending time --->'+job)
	subprocess.call(['rm', '-r', directory+job])

def result1(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result2(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result3(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result4(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result5(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result6(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result7(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result8(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result9(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])

def result10(connection, aa, pc_name):
	global hostIP
	subprocess.call(['python3', './thread_receiver.py', 'Thread_results/'+pc_name+'/', aa, hostIP])


def results_accept(connection, pc_name, sys_name, name_job):                                                    															#to accept the results from the worker
	print ("I will accept the result.")
	subprocess.call(['python3', './receiver.py', sys_name])
	running_directory = './'+sys_name+'/jobStatus/running/'+name_job            															#update the web interface and results can be seen under finished directory.
	subprocess.call(['rm', '-r', running_directory])
	extract_dir = './'+sys_name+'/jobStatus/finished/'
	result_dir = './'+sys_name+'/results/'
	for extract_name in os.listdir(extract_dir):
			extract_split = extract_name.split('_')
			if extract_split[2]=="EPLAS":
				extract_zip_EPLAS(extract_name, extract_dir)
				subprocess.call(['rm', '-r', extract_dir+extract_name])
				break
	for extract_name in os.listdir(extract_dir):
		shutil.move(extract_dir+extract_name, result_dir)


def extract_zip_EPLAS(name_of_job, directory):
	file_name = directory+name_of_job
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	job_name_extract = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()
		
def push_worker(pc):                                                        																								#workers are pushed to the available woker list
	global available_list
	if pc=="PC1":
		available_list.append("PC1")
	elif pc=="PC2":
		available_list.append("PC2")
	elif pc=="PC3":
		available_list.append("PC3")
	elif pc=="PC4":
		available_list.append("PC4")
	elif pc=="PC5":
		available_list.append("PC5")
	else:
		available_list.append("PC6")

def pop_worker(pc):                                                         																								#workers are removed from the available worker list
	global available_list
	print (available_list, "pop_worker")
	for worker in range(0, len(available_list)):
		if pc in available_list[worker]:
			if pc=="PC1":
				available_list.remove("PC1")
			elif pc=="PC2":
				available_list.remove("PC2")
			elif pc=="PC3":
				available_list.remove("PC3")
			elif pc=="PC4":
				available_list.remove("PC4")
			elif pc=="PC5":
				available_list.remove("PC5")
			else:
				available_list.remove("PC6")
		else:
			print ("This worker is already not free.")

if __name__ == "__main__":                                                 																									#Starting point of the program
	main()