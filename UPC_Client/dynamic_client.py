import socket
import sys
import datetime
import time
import os
import csv
import subprocess
from threading import Thread

def dynamic_client_main(host, port, worker_name):
	sys.setrecursionlimit(10**7)
	global busy
	busy = 0
	global job_flag
	job_flag = 0
	global measurement
	measurement = './upc_dynamic_client.csv'
	connect_master(host, port, worker_name)

def connect_master(host, port, worker_name):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		soc.connect((host, int(port)))
		print ("Worker "+worker_name+" is connected to the UPC Master.")
	except:
		print("Connection error")
		sys.exit()
	soc.sendall(worker_name.encode("utf8"))
	total_job = soc.recv(5120).decode("utf8")
	global job_flag
	job_flag = job_flag+1
	while job_flag<=int(total_job):
		soc.sendall(str(job_flag).encode("utf8"))
		time.sleep(2)
		response = soc.recv(5120).decode("utf8")
		time.sleep(2)
		name_of_job = soc.recv(5120).decode("utf8")
		#checka(name_of_job)
		if response=="yes":
			receive_job(job_flag, name_of_job, soc)
		elif response=="last_job":
			receive_last_job(job_flag, soc, name_of_job)
		else:
			time.sleep(5)

def receive_job(job_flag, name_of_job, soc, host, port, worker_name):
	global measurement
	job_start_receive = time_second()
	data = name_of_job+ " start receiving time at workerpc5 is ["+str(job_start_receive)+" second]--["+standard_time(job_start_receive)+"]<<<<"
	record_csv(measurement, name_of_job, standard_time(job_start_receive))
	print ("Job No.",job_flag, "is received and ")
	total_time = job_execution(job_flag, name_of_job, soc)
	value = check_job_time(name_of_job)
	total = total_time+value
	data = "Total time is ["+str(total)+" second]--["+standard_time(total)+"]"
	record_csv(measurement, "Total", standard_time(total))
	print ("Finished Job No.", job_flag, "and request master to send the next job.")
	connect_master(host, port, worker_name)

def receive_last_job(job_flag, soc, name_of_job):
	global measurement
	job_start_receive = time_second()
	data = name_of_job+ " start receiving time at workerpc5 is ["+str(job_start_receive)+" second]--["+standard_time(job_start_receive)+"]<<<<"
	record_csv(measurement, name_of_job, standard_time(job_start_receive))
	print ("Job No.",job_flag, "is received and ")
	total_time = job_execution(job_flag, name_of_job, soc)
	value = check_job_time(name_of_job)
	total = total_time+value
	data = "Total time is ["+str(total)+" second]--["+standard_time(total)+"]"
	record_csv(measurement, "Total", standard_time(total))
	print ("This is the last job and no more job to assign me. I will leave. Bye...")
	soc.close()
	os._exit(os.EX_OK)

def job_execution(job_flag, name_of_job, soc):
	global measurement
	directory = './'
	
	s1 = time_second()
	subprocess.call(['python3', './receiver_pc.py'])
	e1 = time_second()
	job_receiving_time = int(e1)-int(s1)
	data1 = "Receiving time is ["+str(job_receiving_time)+" second]--["+standard_time(job_receiving_time)+"]"

	s2 = time_second()
	name_of_job1 = docker_name_check(name_of_job)
	#rename_desktop_docker(name_of_job1)
	print (name_of_job1)
	subprocess.call(['podman', 'load', '-i', name_of_job])
	e2 = time_second()
	job_loading_time = int(e2)-int(s2)
	data2 = "Loading time is ["+str(job_loading_time)+" second]--["+standard_time(job_loading_time)+"]"

	dd = name_of_job1.split('_')
	docker_name = 'pollen5005/'+dd[1]+":latest"

	s3 = time_second()
	subprocess.call(['podman', 'run', '-t', '--name', name_of_job1, '-v', '/home/upc/:/opt',docker_name])
	e3 = time_second()
	job_executing_time = int(e3)-int(s3)
	data3 = "Executing time is ["+str(job_executing_time)+" second]--["+standard_time(job_executing_time)+"]"

	subprocess.call(['podman', 'container', 'prune', '-f'])
	#check_delete_not(name_of_job)
	os.remove(str(directory+name_of_job))
	soc.sendall("result".encode("utf8"))
	time.sleep(2)
	result_dir = '/home/upc/'
	fill_count = 0
	for fills_name in os.listdir(result_dir):
		fill_count = fill_count+1
	soc.sendall(str(fill_count).encode("utf8"))
	time.sleep(2)
	soc.sendall(name_of_job.encode("utf8"))
	time.sleep(2)

	s4 = time_second()
	for fills_name in os.listdir(result_dir):
		soc.sendall(str(fills_name).encode("utf8"))
		time.sleep(5)
		fa = open(result_dir+fills_name, 'rb')
		I = fa.read(5120)
		while(I):
			soc.send(I)
			time.sleep(5)
			I = fa.read(5120)
		fa.close()
		time.sleep(5)
	e4 = time_second()
	result_transferring_time = int(e4)-int(s4)
	data4 = "Result transferring time is ["+str(result_transferring_time)+" second]--["+standard_time(result_transferring_time)+"]"
	subprocess.call(['podman', 'rmi', '-f', docker_name])

	for fills_name in os.listdir(result_dir):
		os.remove(str(result_dir+fills_name))

	total_time = job_receiving_time+job_loading_time+job_executing_time+result_transferring_time
	data5 = "Total time is ["+str(total_time)+" second]--["+standard_time(total_time)+"]"
	return total_time

def record_csv(csv_file, data, timea):
	with open(csv_file, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([data, timea])

def check_job_time(name_of_job):
	dd = name_of_job.split('_')
	with open('./pc_loadtime.csv', 'rt')as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			if row[0]==dd[1]:
				value = int(row[1])
				time.sleep(int(value))
				return value
			else:
				print ("Not that job.")

def time_second():
	start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	#print ("Starting time(h:m:s)-"+start_time+" ("+start_date+")")
	return start_total

# def checka(name_of_job):
# 	desktop = './'
# 	current_job_name = name_of_job.split('_')
# 	name_length = len(name_of_job)
# 	try:
# 		if (name_of_job[int(name_length)-1]=='a'):
# 			for name_job in os.listdir(desktop):
# 			 	try:
# 			 		check_job_name = name_job.split('_')
# 			 		if current_job_name[1]==check_job_name[1]:
# 			 			os.remove(str(desktop+name_job))
# 			 	except:
# 			 		print ("Not a.")
# 	except:
# 		print ("String index out of bound.")

def docker_name_check(name_of_job):
	dd = name_of_job.split('_')
	name_of_job1 = dd[1]
	docker1 = 'wimnetsimulatora'
	docker2 = 'apca'
	docker3 = 'dcgana'
	docker4 = 'recurrentnetworka'
	docker5 = 'mnista'
	docker6 = 'ffmpeg'
	docker7 = 'converter'
	docker8 = 'palabosa'
	docker9 = 'opma'
	docker10 = 'bitcoinhhcoina'
	docker11 = 'covid19countrycoa'
	docker12 = 'covid19traintestcoa'
	docker13 = 'ffmpegchange'
	docker14 = 'ffmpegresize'
	dockerb = 'ffmpegb'
	dockerc = 'ffmpegc'
	dockerd = 'ffmpegd'
	dockere = 'ffmpege'
	dockerf = 'ffmpegf'
	dockerg = 'ffmpegg'
	dockera = 'ffmpega'

	with open('./pc_loadtime.csv', 'rt')as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			if name_of_job1[0]=='w':
				return dd[0]+'_'+docker1
			elif name_of_job1[0]=='a':
				return dd[0]+'_'+docker2
			elif name_of_job1[0]=='d':
				return dd[0]+'_'+docker3
			elif name_of_job1[0]=='r':
				return dd[0]+'_'+docker4
			elif name_of_job1[0]=='m':
				return dd[0]+'_'+docker5
			elif name_of_job1[0]=='d':
				return dd[0]+'_'+docker3
			elif name_of_job1==docker6 or name_of_job1==dockera or name_of_job1==dockerb or name_of_job1==dockerc or name_of_job1==dockerd or name_of_job1==dockere or name_of_job1==dockerf or name_of_job1==dockerg:
				return dd[0]+'_'+docker6
			elif name_of_job1[3]=='v':
				return dd[0]+'_'+docker7
			elif name_of_job1[0]=='p':
				return dd[0]+'_'+docker8
			elif name_of_job1[0]=='o':
				return dd[0]+'_'+docker9
			elif name_of_job1[0]=='b':
				return dd[0]+'_'+docker10
			elif name_of_job1[7]=='c' and name_of_job1[8]=='o':
				return dd[0]+'_'+docker11
			elif name_of_job1[7]=='t':
				return dd[0]+'_'+docker12
			elif name_of_job1[6]=='c':
				return dd[0]+'_'+docker13
			elif name_of_job1[6]=='r':
				return dd[0]+'_'+docker14
			else:
				print ("Not that job job job job.")

# def rename_desktop_docker(name_of_job1):
# 	desktop = './'
# 	current_job_name = name_of_job1.split('_')
# 	for name_job in os.listdir(desktop):
# 	 	try:
# 	 		check_job_name = name_job.split('_')
# 	 		if current_job_name[1]==check_job_name[1]:
# 	 			os.rename(os.path.join(desktop, name_job), os.path.join(desktop,name_of_job1))
# 	 			print ("******", name_of_job1)
# 	 			subprocess.call(['chmod', '777', '-R', desktop+name_of_job1])
# 	 	except:
# 	 		print ("Move to another file.")

# def check_delete_not(name_of_job):
# 	directory = './'
# 	docker1 = 'wimnetsimulatora'
# 	docker2 = 'apca'
# 	docker3 = 'dcgana'
# 	docker4 = 'recurrentnetworka'
# 	docker5 = 'mnista'
# 	docker6 = 'ffmpeg'
# 	docker7 = 'convertera'
# 	docker8 = 'palabosa'
# 	docker9 = 'opma'
# 	docker10 = 'bitcoinhhcoin'
# 	docker11 = 'covid19countrycoa'
# 	docker12 = 'covid19traintestcoa'
# 	docker13 = 'ffmpegchange'
# 	docker14 = 'ffmpegresize'
# 	job = name_of_job.split('_')
# 	if (job[1]==docker1 or job[1]==docker2 or job[1]==docker3 or job[1]==docker4 or job[1]==docker5 or job[1]==docker6 or job[1]==docker7 or job[1]==docker8 or job[1]==docker9 or job[1]==docker10 or job[1]==docker11 or job[1]==docker12 or job[1]==docker13 or job[1]==docker14):
# 		print ("No need to delete.")
# 	else:
# 		os.remove(str(directory+name_of_job))


def standard_time(seconds): 
	min, sec = divmod(seconds, 60) 
	hour, min = divmod(min, 60) 
	return "%d:%02d:%02d" % (hour, min, sec)

if __name__ == "__main__":
	sys.setrecursionlimit(10**7)
	main()