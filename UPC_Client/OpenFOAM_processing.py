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

def connect_master_openfoam(host, port, worker_name, IDs):
	global soc
	print (IDs)
	
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
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Please execute this job.", master_response)
		receive_job(host, port, master_response, soc, worker_name, IDs)

def receive_job(host, port, master_response, soc, worker_name, IDs):
	global csv_file
	if (master_response=="one"):
		csv_file = './results/thread_one.csv'
		one(host, port, soc, worker_name, IDs)
	elif (master_response=="two"):
		csv_file = './results/thread_one.csv'
		two(host, port, soc, worker_name, IDs)
	elif (master_response=="three"):
		csv_file = './results/thread_one.csv'
		three(host, port, soc, worker_name, IDs)
	elif (master_response=="four"):
		csv_file = './results/thread_one.csv'
		four(host, port, soc, worker_name, IDs)
	elif (master_response=="five"):
		csv_file = './results/thread_one.csv'
		five(host, port, soc, worker_name, IDs)
	elif (master_response=="six"):
		csv_file = './results/thread_one.csv'
		six(host, port, soc, worker_name, IDs)
	elif (master_response=="seven"):
		csv_file = './results/thread_one.csv'
		seven(host, port, soc, worker_name, IDs)
	elif (master_response=="eight"):
		csv_file = './results/thread_one.csv'
		eight(host, port, soc, worker_name, IDs)
	elif (master_response=="nine"):
		csv_file = './results/thread_one.csv'
		nine(host, port, soc, worker_name, IDs)
	elif (master_response=="ten"):
		csv_file = './results/thread_one.csv'
		ten(host, port, soc, worker_name, IDs)
	else:
		print ("Something wrong.")

def one(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread1_proce.start()
	returna = thread1_proce.join()
	if returna==None:
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("No need to wait other threads finishing.")

def two(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	if returna==None and returnb==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def three(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread3', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	if returna==None and returnb==None and returnc==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def four(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread3', worker_name, IDs, host, port))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread4', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def five(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread3', worker_name, IDs, host, port))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread4', worker_name, IDs, host, port))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread5', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def six(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread3', worker_name, IDs, host, port))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread4', worker_name, IDs, host, port))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread5', worker_name, IDs, host, port))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread6', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def seven(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread3', worker_name, IDs, host, port))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread4', worker_name, IDs, host, port))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread5', worker_name, IDs, host, port))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread6', worker_name, IDs, host, port))
	thread7_proce = multiprocessing.Process(target = thread7, args=(soc, 'thread7', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	thread7_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	returng = thread7_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None and returng==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def eight(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread3', worker_name, IDs, host, port))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread4', worker_name, IDs, host, port))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread5', worker_name, IDs, host, port))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread6', worker_name, IDs, host, port))
	thread7_proce = multiprocessing.Process(target = thread7, args=(soc, 'thread7', worker_name, IDs, host, port))
	thread8_proce = multiprocessing.Process(target = thread8, args=(soc, 'thread8', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	thread7_proce.start()
	thread8_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	returng = thread7_proce.join()
	returnh = thread8_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None and returng==None and returnh==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def nine(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread3', worker_name, IDs, host, port))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread4', worker_name, IDs, host, port))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread5', worker_name, IDs, host, port))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread6', worker_name, IDs, host, port))
	thread7_proce = multiprocessing.Process(target = thread7, args=(soc, 'thread7', worker_name, IDs, host, port))
	thread8_proce = multiprocessing.Process(target = thread8, args=(soc, 'thread8', worker_name, IDs, host, port))
	thread9_proce = multiprocessing.Process(target = thread9, args=(soc, 'thread9', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	thread7_proce.start()
	thread8_proce.start()
	thread9_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	returng = thread7_proce.join()
	returnh = thread8_proce.join()
	returni = thread9_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None and returng==None and returnh==None and returni==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def ten(host, port, soc, worker_name, IDs):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread1', worker_name, IDs, host, port))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread2', worker_name, IDs, host, port))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread3', worker_name, IDs, host, port))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread4', worker_name, IDs, host, port))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread5', worker_name, IDs, host, port))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread6', worker_name, IDs, host, port))
	thread7_proce = multiprocessing.Process(target = thread7, args=(soc, 'thread7', worker_name, IDs, host, port))
	thread8_proce = multiprocessing.Process(target = thread8, args=(soc, 'thread8', worker_name, IDs, host, port))
	thread9_proce = multiprocessing.Process(target = thread9, args=(soc, 'thread9', worker_name, IDs, host, port))
	thread10_proce = multiprocessing.Process(target = thread10, args=(soc, 'thread10', worker_name, IDs, host, port))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	thread7_proce.start()
	thread8_proce.start()
	thread9_proce.start()
	thread10_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	returng = thread7_proce.join()
	returnh = thread8_proce.join()
	returni = thread9_proce.join()
	returnj = thread10_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None and returng==None and returnh==None and returni==None and returnj==None:
		find_maximum()
		connect_master_openfoam(host, port, worker_name, IDs)
	else:
		print ("Wait other threads finishing.")

def find_maximum():
	global thread_list
	find_max = []
	csv_file1 = './results/thread_max.csv'
	csv_fileab = './max/'
	for name_job in os.listdir(csv_fileab):
		read_file = open('./max/'+name_job, 'r')
		for data in read_file:
			dataa = data.split(',')
			print (dataa[1])
			find_max.append(dataa[1])
		subprocess.call(['rm', '-r', './max/'+name_job])
	max_value = max(find_max)
	record_csv(csv_file1, str(max_value), '-------', '-------', '-------')

def thread1(soc, thread, worker_name, IDs, host, port):
	save_loc = 1
	access_port = str(worker_name[2])+'004'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread2(soc, thread, worker_name, IDs, host, port):
	save_loc = 2
	access_port = str(worker_name[2])+'005'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread3(soc, thread, worker_name, IDs, host, port):
	save_loc = 3
	access_port = str(worker_name[2])+'006'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread4(soc, thread, worker_name, IDs, host, port):
	save_loc = 4
	access_port = str(worker_name[2])+'007'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread5(soc, thread, worker_name, IDs, host, port):
	save_loc = 5
	access_port = str(worker_name[2])+'008'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread6(soc, thread, worker_name, IDs, host, port):
	save_loc = 6
	access_port = str(worker_name[2])+'009'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread7(soc, thread, worker_name, IDs, host, port):
	save_loc = 7
	access_port = str(worker_name[2])+'010'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread8(soc, thread, worker_name, IDs, host, port):
	save_loc = 8
	access_port = str(worker_name[2])+'011'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread9(soc, thread, worker_name, IDs, host, port):
	save_loc = 9
	access_port = str(worker_name[2])+'012'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread10(soc, thread, worker_name, IDs, host, port):
	save_loc = 10
	access_port = str(worker_name[2])+'013'
	thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port)

def thread_run(soc, thread, worker_name, IDs, save_loc, access_port, host, port):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', './receiver1.py', 'data'+str(save_loc), access_port])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	start1 = time_second()
	job_execute('data'+str(save_loc), access_port, start1, str(IDs[save_loc-1]), soc, host, port, worker_name, IDs, thread)
	soc.close()
	return "THREAD-"+str(save_loc)

def job_execute(data, portt, start1, container_name, soc, host, port, worker_name, IDs, thread_no):
	 global csv_file
	 global thread_list
	 csv_filea = './max/'+thread_no+'.csv'
	 directory = './'+data+'/'
	 name_of_job = ""
	 for name_job in os.listdir(directory):
	 	name_of_job = name_job
	 subprocess.call(['chmod', '777', '-R', directory+name_of_job])
	 job = name_of_job.split('.')
	 plas_job = job[0].split('_')
	 eeplas_job = job[0].split('-')
	 eeeplas_job = eeplas_job[0].split('_')
	 if eeeplas_job[3]=="openfoam":
	 	print ("This is the OpenFoam job.")
	 	zip_extract(name_of_job, directory)
	 	start3 = time_second()
	 	job_type = openfoam_execute(name_of_job, directory, container_name)
	 	end3 = time_second()
	 	real_execution_time = str(int(end3)-int(start3))
	 	abc = name_of_job.split('-')
	 	ddd = abc[1].split('.')
	 	record_csv(csv_file, real_execution_time, ddd[0], job_type, thread_no)
	 	record_csv(csv_filea, real_execution_time, '---', '---', '---')
	 	execute_job_plas(host, directory, job[0], soc, portt, start1)
	 	return real_execution_time
	 else:
	 	print ("This is a container.")
	 	connect_master_openfoam(host, port, worker_name, IDs)

def openfoam_execute(name_of_job,  directory, container_name):
	print (name_of_job)
	receive_job_working_dir = ''
	for name_job in os.listdir(directory):
		receive_job_working_dir = name_job

	for name_job in os.listdir(directory+receive_job_working_dir):
		print (name_job)
	open_work_directory = directory+receive_job_working_dir
	subprocess.call(['chmod', '777', '-R', open_work_directory])
	os.chdir(open_work_directory)
	openfoam_start = time_second()
	print ("*************")
	print (container_name)
	print ("*************")
	subprocess.call(['podman', 'container', 'run', '-ti', '--rm', '-v', './:/data', '-w', '/data', 'myopenfoam:'+container_name, './Allrun'])
	openfoam_end = time_second()
	direc = open_work_directory+"/postProcessing/probe(T)/0/T"
	openfoam_running_time = str(int(openfoam_end)-int(openfoam_start))
	os.chdir('..')
	os.chdir('..')
	subprocess.call(['pwd'])
	subprocess.call(['scp', direc, directory])
	subprocess.call(['chmod', '777', '-R', directory])
	subprocess.call(['rm', '-r', open_work_directory])
	time_file = directory+'time.csv'
	record_csv(time_file, openfoam_running_time,name_of_job, '---', '---')

def extract_aplas_manifest(file1):
	manifest = open(file1, 'rb')
	for line in manifest:
		line = line.decode('UTF-8')
		extract = line
		split_extract = extract.split('=')
		if split_extract[0]=='PROJECT':
			return split_extract[1]

def zip_extract(name_of_job, directory):
	file_name = directory+name_of_job
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	job_name_extract = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()
	subprocess.call(['chmod', '777', '-R', directory])
	subprocess.call(['rm', '-r', directory+name_of_job])

def execute_job_plas(host, directory, name_of_job, soc, portt, start1):
	global csv_file
	subprocess.call(['chmod', '777', '-R', directory])
	result_dir = "./result/"+name_of_job
	shutil.make_archive(result_dir, 'zip', directory)
	result = result_dir+".zip"
	end1 = time_second()
	receive1 = standard_time(int(end1)-int(start1))
	start2 = time_second()
	send_result(host, result, soc, directory, portt)
	end2 = time_second()
	receive2 = standard_time(int(end2)-int(start2))

def record_csv(csv_file, execution_time, name_of_job, job_type, thread_no):
	with open(csv_file, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([name_of_job, execution_time, job_type, thread_no])

def time_second():
	start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	return start_total

def standard_time(seconds): 
	min, sec = divmod(seconds, 60) 
	hour, min = divmod(min, 60) 
	return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)

def send_result(host, result, soc, directory, portt):
	delete_job = ""
	for jobs in os.listdir(directory):
		delete_job = jobs
		subprocess.call(['rm', '-r', directory+delete_job])
	time.sleep(2)
	time.sleep(3)
	subprocess.call(['python3', './sender.py', result, host, portt])
	subprocess.call(['rm', '-r', result])