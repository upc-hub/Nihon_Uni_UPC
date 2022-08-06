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
import random

def connect_master_eplas(host, port, worker_name):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		soc.connect((host, port))
		print ("Worker "+worker_name+" is connected to the UPC Master.")
	except:
		print("Connection error")
		sys.exit()
	soc.sendall(worker_name.encode("utf8"))
	master_response = soc.recv(5120).decode("utf8")
	if master_response=="wait":
		print ("There is no job at master.")
		time.sleep(5)
		connect_master_eplas(host, port, worker_name)
	else:
		print ("Please execute this job.", master_response)
		receive_job(master_response, soc, host, port, worker_name)

def receive_job(name_of_job, soc, host, port, worker_name):
	directory = './data/'
	csv_file = './eplas.csv'
	start_d = time_second()
	subprocess.call(['python3', './receiver.py'])
	print ("Hein Htet.............................................")
	end_d = time_second()
	job_receiving_time = standard_time(int(end_d)-int(start_d))
	record_csv(csv_file, str(job_receiving_time)+' job_receiving_time')
	subprocess.call(['chmod', '777', '-R', directory+name_of_job])
	job = name_of_job.split('.')
	plas_job = job[0].split('_')
	eeplas_job = job[0].split('-')
	eeeplas_job = eeplas_job[0].split('_')
	if plas_job[2]=="EPLAS":
		print (plas_job, '**********************************')
		start_a = time_second()
		zip_extract(name_of_job, directory)
		start_b = time_second()
		eplas_execute(name_of_job, directory)
		end_b = time_second()
		execution_time = standard_time(int(end_b)-int(start_b))
		record_csv(csv_file, str(execution_time)+' execution_time-----------'+name_of_job)
		result = './eplas_modify/output/'
		for jobs in os.listdir('./eplas_modify/output/'):
			result_job = jobs
		execute_job_plas(result, job[0], soc, start_a, host)
		connect_master_eplas(host, port, worker_name)
	else:
		print ("This is a container.")
		connect_master_eplas(host, port, worker_name)

def zip_extract(name_of_job, directory):
	file_name = directory+name_of_job
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	job_name_extract = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()
	subprocess.call(['chmod', '777', '-R', directory])
	subprocess.call(['rm', '-r', directory+name_of_job])

def eplas_execute(name_of_job, directory):
	subprocess.call(['docker', 'run', '-v', '/home/pc4/Desktop/upc_client/data/:/data', '-it', 'seancook/openpose-cpu', '-display', '0', '-image_dir', '/data', '-write_images', '/data', '-write_json', '/data'])
	for jobs in os.listdir(directory):
		job_separate = jobs.split("_")
		job_loc = len(job_separate)-1
		if job_separate[job_loc][0]=="r":
			print (job_separate[job_loc],"-----------------")
			shutil.move(directory+jobs, './eplas_modify/process/picture/')
		elif job_separate[job_loc][0]=="k":
			print (job_separate[job_loc],"-----------------")
			shutil.move(directory+jobs, './eplas_modify/process/keypoints/')
		else:
			subprocess.call(['rm', '-r', directory+jobs])
			print ("Deleted......")
	eplas_modify(directory)

def eplas_modify(directory):
	subprocess.call(['python3', './EPLAS.py', '-f', './eplas_modify'])
	for jobs in os.listdir('./eplas_modify/process/picture/'):
		subprocess.call(['rm', '-r', './eplas_modify/process/picture/'+jobs])
	for jobs in os.listdir('./eplas_modify/process/keypoints/'):
		subprocess.call(['rm', '-r', './eplas_modify/process/keypoints/'+jobs])

def execute_job_plas(directory, name_of_job, soc, start_a, host):
	subprocess.call(['chmod', '777', '-R', directory])
	result_dir = "./result/"+name_of_job
	shutil.make_archive(result_dir, 'zip', directory)
	result = result_dir+".zip"
	send_result(result, soc, directory, host)
	for jobs in os.listdir('./eplas_modify/output/'):
		subprocess.call(['rm', '-r', './eplas_modify/output/'+jobs])

def send_result(result, soc, directory, host):
	subprocess.call(['python3', './sender.py', result, host, '5005'])
	subprocess.call(['rm', '-r', result])

def record_csv(csv_file, data):
	with open(csv_file, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([data])

def time_second():
	start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	return start_total

def standard_time(seconds): 
	min, sec = divmod(seconds, 60) 
	hour, min = divmod(min, 60) 
	return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)