from datetime import date
from threading import Thread
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
global token_counter_today
global available_list           #current available worker list connected to UPC Master
global chk_aplas_jobs

token_counter_today = 0
available_list = []
chk_aplas_jobs = []

def transform_to_upc_job_eplas(EPLAS_dir, APLAS_dir, local_dir, all_job_dir, com_job_dir, ip, threads, serverIP):                                          #submitted jobs are renamed to be compactible with the system requirements e.g. currentToken_ddmmyyyy_jobName
	global token_counter_today
	global available_list
	csv_file = './aplas.csv'
	print ("Currently available worker : ", available_list)
	subprocess.call(['scp', '-r', local_dir+'.', all_job_dir])
	subprocess.call(['rm', '-r', local_dir])
	for jobs in os.listdir(EPLAS_dir):
		shutil.move(EPLAS_dir+jobs, all_job_dir)
	
	for file_name in os.listdir(all_job_dir):
		job_name = str(file_name)
		if (job_name[0].isdigit()):																															#check renamed or not
			print ()
		token_counter_today = token_counter_today + 1
		token = initiate_job_token()
		os.rename(os.path.join(all_job_dir, file_name), os.path.join(all_job_dir,token+'_'+file_name))          											#renaming process
		shutil.move(all_job_dir+token+'_'+file_name, com_job_dir)											    											#renamed jobs are moved to common Queue
		start = total_second()
		zip_extract(token+'_'+file_name, com_job_dir)
		end = total_second()
		job_preparation_time = convert(int(end)-int(start))
		record_csv(csv_file, str(job_preparation_time)+ " job_preparation_time of"+token+'_'+file_name)      												#extract jobs's zips
	
	check_tick = True
	while check_tick:
		current_total = 0
		for entry_name in os.listdir(EPLAS_dir):
			print (entry_name)
			current_total = current_total+1
		if current_total>=1:
			time.sleep(5)
			print ("New job is detected.")
			check_tick = False
			transform_to_upc_job_eplas(EPLAS_dir, APLAS_dir, local_dir, all_job_dir, com_job_dir, ip, threads, serverIP)
		else:
			time.sleep(10)
			print ("No new jobs are detected.")
			check_tick=True

#schedule.every(10).seconds.do(transform_to_upc_job_eplas)                  																					#UPC Master checks jobs arrive from UPC Web Server every 30 seconds

def initiate_job_token():								   																									#generate currentToken for the submitted jobs
	global token_counter_today
	if check_day_change():                                 																									#check change to the next day or not for reseting the token
		token_counter_today = 0
	today_date = date.today()
	day = str(today_date.day)
	month = str(today_date.month)
	year = str(today_date.year)
	generate_token = str(token_counter_today)+"_"+day+month+year
	return generate_token

def check_day_change():                                    																									#check change to the next day or not			  						
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute
	second = datetime.datetime.now().second
	if (hour == '23' and minute == '59' and second == '59'):
		return True

def zip_extract(job_name, directory):                      																									#extract job's zip file and read the Metadata of job 
	zip_name = job_name.split('.')
	zip_name_container = job_name.split('_')
	aplas_name_container = zip_name[0].split('-')
	aplas_name_container1 = aplas_name_container[0].split('_')
	file_name = directory+job_name
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	name_of_job = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()
	os.rename(os.path.join(directory, name_of_job[0]), os.path.join(directory,zip_name[0]))       															#extracted zip's name may be different from the renames by the System
	os.remove(file_name)                                                                          															#previous zip files are removed
	subprocess.call(['chmod', '777', '-R', directory])
	job_dir = directory+zip_name[0]
	check_container_require(zip_name_container[0], job_dir, zip_name[0])                          															#check container is needed to build or not by reading job's Metadata

def check_container_require(zip_name_container, job_dir, sys_name):
	global available_list
	container_queue = './container_queue/'
	common_queue = './common_queue/'
	docker_template = './Dockerfile'               																											#Dokerfile template if job is necessary to build a container
	base_directory = './'
	detect_system = sys_name.split('_')
	detect_systema = sys_name.split('-')
	detect_systemb = detect_systema[0].split('_')
	local = detect_system[2]
	if(local[0]=='l'):                                                             																			#differentiate between local and outsider systems
		detect_system[2]='local_user'
	elif detect_system[2]=='EPLAS':
		print (sys_name+" is the EPLAS job. It doesn't need to check Metadata.")
		subprocess.call(['scp', '-r', common_queue+sys_name, base_directory+detect_system[2]+'/jobStatus/waiting/'])          								#after necessary checking, jobs are moved to the waiting queue of correspondance system. It can be seen on Web interface.
		shutil.move(job_dir, container_queue)                              																					#All checked jobs are reached to the container queue and then, moved to the correspondance worker queue
		available_worker = current_available_worker()                      																					#checked is there any worker already connected to master before jobs arrived
		if available_worker=="":                                           																					#if there is no available worker, assign null
			print ()
		else:
			shutil.move(container_queue+str(sys_name), base_directory+str(available_worker))      															#if there is a worker for the current job, this job is moved from the container queue to that worker queue 
		update_job_list(sys_name, available_worker)                                               															#record current job and worker's tates
		try:
			print (available_list[0], "<<<<this worker will be poped from the list.")             															#If a job is assigned to the worker, that worker is removed from the available worker list.
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
	

def update_worker_eplas(pc):                                                                 																#connected workers update 
	global available_list
	container_queue = './container_queue/'
	base_directory = './'
	print (available_list, "<----current available worker list")
	#print ("This is the length", len(available_list))
	if len(available_list)==0:                                                         																		#check connected worker is already in the available worker list
		push_worker(pc)                                                                																		#if not, that worker is added to the available worker list
		#print ("This is the first time join.")                                        
	else:                                                                              																		#connected worker is already in the avaialable list
		break_out_flag1 = False
		#print ("This is not the first time.")
		for worker in range(0, len(available_list)):
			if pc in available_list[worker]:
				break_out_flag1 = True
				break
		if break_out_flag1:
			print (pc, " (worker) is already added.")
		else:
			push_worker(pc)
			print (pc, "This worker is added to the available list.")
	send_job = ""
	send_worker = ""
	no_job = ""
	no_worker = ""
	with open('./job_list_status.csv') as f:          																										#update job and worker list (this time is adding current connected worker to the status file.)
		reader = csv.reader(f)
		lines = list(reader)
		try:
			if lines[1][0] == "":
				no_job = "No job"
				no_worker = "No worker"
			else:                                                                     																		#if job already added in the status file but there is no worker for this job. (Update that place)
				break_out_flag = False
				for i in range(len(lines)):
					for j in range(len(lines[i])):
						if lines[i][j]=="":
							lines[i][j] = available_list[0]
							send_job = lines[i][j-1]
							send_worker = lines[i][j]
							break_out_flag = True
							pop_worker(pc)
							break
					if break_out_flag:
						break

				with open('./job_list_status.csv', 'w') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerows(lines)
				try:
					shutil.move(container_queue+send_job, base_directory+send_worker)                      													#Update job is moved to the correspondance worker queue
				except shutil.Error:
					print ()

				return send_job, send_worker

		except IndexError:
			send_job = "No job"
			send_worker = "No worker"
			print ("There is no job.")
			return send_job, send_worker

def check_job_to_execute_eplas(host, connection, ip, pc_name, worker_port):                               
	container_queue = './container_queue/'
	base_directory = './'
	if len(os.listdir(base_directory+pc_name))== 0:                                 																		#each connected worker check its correspondance queue for the jobs exist or not
		print ("No new jobs are detected.")
		connection.sendall("wait".encode("utf8"))                                   																		#if there is no job, send  'wait' message by Master to that worker
	else:                                                                           																		#if there are jobs, grab only the first job in its queue
		job = ""
		for entry_name in os.listdir(base_directory+pc_name):
			job = entry_name
			#print (entry_name, "Job name")
			break
		path = base_directory+pc_name+"/"
		
		
		create_zip = job+".zip"
		csv_file ='./aplas.csv'
		shutil.make_archive(base_directory+pc_name+"/"+job, 'zip', base_directory+pc_name+"/"+job)
		subprocess.call(['chmod', '777', '-R', path])
		subprocess.call(['rm', '-r', path+job])
		connection.sendall(create_zip.encode("utf8"))                                                                                					#job name is sent to the worker
		print ("UPC Master will send this ",create_zip, "(job) soon.")
		time.sleep(3)
		sys_name = job.split("_")
		sys_name1 = job.split("-")
		sys_name2 = sys_name1[0].split("_")
		time.sleep(5)                                                                                                                					#give some time to the worker for job accept 
		#print (ip, "................................")
		subprocess.call(['python3', './sender.py', base_directory+pc_name+"/"+job+".zip", ip])       													#job is sent to the worker
		subprocess.call(['rm', '-r', base_directory+pc_name+"/"+job+".zip"])
		subprocess.call(['chmod', '777', '-R', base_directory+"EPLAS/jobStatus/waiting/"])
		subprocess.call(['rm', '-r', base_directory+"EPLAS/jobStatus/waiting/*"])
		time.sleep(3)
		result1(host, connection, pc_name, worker_port)
		subprocess.call(['chmod', '777', '-R', base_directory+"EPLAS/jobStatus/finished/"])

def total_second():
    start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
    start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
    start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
    return start_total

def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)

def extract_zip_EPLAS(name_of_job, directory):
	file_name = directory+name_of_job
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	job_name_extract = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()

def record_csv(csv_file, data):
	with open(csv_file, 'a')as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([data])
		
def push_worker(pc):                                                        																				#workers are pushed to the available woker list
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

def pop_worker(pc):                                                         																				#workers are removed from the available worker list
	global available_list
	print (available_list, " is busy right now!!!")
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

def result1(host, connection, pc_name, worker_port):
	subprocess.call(['python3', './eplas_receiver.py', 'EPLAS/jobStatus/finished/', str(worker_port[int(pc_name[2])-1]), host])

if __name__ == "__main__":                                                 																					#Starting point of the program
	main()