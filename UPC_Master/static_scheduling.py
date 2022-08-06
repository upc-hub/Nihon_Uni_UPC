import shutil
import datetime
import time
import os, zipfile
import subprocess
import socket
import sys
from threading import Thread
import traceback
import time
import csv
import re
from migration_process_master import *
global schedule_file
schedule_file = True
def static_main(host, port):
	global pc1_count, pc2_count, pc3_count, pc4_count, pc5_count, pc6_count, measurement, worker_free_not, worker1, worker2, worker3, worker4, worker5, worker6, migrate_job_name_and_worker, name_worker, checkpoint_send
	pc1_count, pc2_count, pc3_count, pc4_count, pc5_count, pc6_count, worker1, worker2, worker3, worker4, worker5, worker6, migrate_job_name_and_worker, name_worker, checkpoint_send = 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, [], 0, 0
	worker_free_not = [worker1, worker2, worker3, worker4, worker5, worker6]
	measurement = './conduct_measurement1.csv'
	thread_master_start = Thread(target = start_server_new, args=(host,port))
	thread_master_start.start()
	#thread_master_start1 = Thread(target = start_server_new1, args=(host,port2))
	#thread_master_start1.start()

def check_schedule_file():
	global schedule_file
	schedule_dir = "./remove_zip"
	move_dir = "./schedule_file"
	for jobs in os.listdir(schedule_dir):
		try:
			receive_file_name=jobs.split(".")
			if receive_file_name[1]=="csv":
				shutil.copy(schedule_dir+"/"+jobs,move_dir)
				subprocess.call(['rm', '-r', schedule_dir+"/"+jobs])
				schedule_file = False
			else:
				print ("No schedule file yet.")
		except IndexError:
			print ("No file yet")

def start_server_new(host, port):
	directory = './remove_zip/'
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print ("-------------------------------------")
	print ("Elastic UPC Master is started.")
	global measurement, worker_free_not, worker1, worker2, worker3, worker4, worker5, worker6
	worker_free_not = [worker1, worker2, worker3, worker4, worker5, worker6]
	try:
		soc.bind((host, port))
	except:
		print ("Bind failed error:"+ str(sys.exc_info()))
		sys.exit()
	soc.listen(120)

	
	global schedule_file
	while schedule_file:
		check_schedule_file()
		time.sleep(5)

	worker_names1 = []
	global my_dict
	directorya = './'
	with open('./schedule_file/schedule.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			worker_names1.append(row[0])
	mylist = list( dict.fromkeys(worker_names1) )
	my_dict = {i:worker_names1.count(i) for i in worker_names1}
	#print ('worker list accordance with schedule', mylist)
	#print ('worker and job list for each accordance with schedule', my_dict)
	#print (my_dict[mylist[0]])

	global pc1, pc2, pc3, pc4, pc5, pc6, cc1, cc2, cc3, cc4, cc5, cc6, pc3_chk_count

	pc6, pc5, pc4, pc3, pc2, pc1 = directorya+"PC6/", directorya+"PC5/", directorya+"PC4/", directorya+"PC3/", directorya+"PC2/", directorya+"PC1/"
	pc6_chk, pc5_chk, pc4_chk, pc3_chk, pc2_chk, pc1_chk = directorya+"PC6_c/", directorya+"PC5_c/", directorya+"PC4_c/", directorya+"PC3_c/", directorya+"PC2_c/", directorya+"PC1_c/"
	#cc6 = my_dict["PC6"]
	cc5 = my_dict["PC5"]
	#cc4 = my_dict["PC4"]
	#cc3 = my_dict["PC3"]
	#cc2 = my_dict["PC2"]
	#cc1 = my_dict["PC1"]
	
	rename_job_flag_move_worker_dir(directory, mylist, my_dict, directorya)

	print ("UPC Master is now listening the workers")
	print ("-------------------------------------")

	while True:
		connection, address = soc.accept()
		ip, port = str(address[0]), str(address[1])
		print ("-------------------------------------")
		print ("A worker node connected with "+ip+" : "+port)

		time.sleep(5)
		pc_name = connection.recv(5120).decode("utf8")  #very first receive(PC_Name)
		if (pc_name=="PC1"):
			global pc1_count
			pc1_count = pc1_count+1
			worker1 = 1
			accept_worker(connection, ip, port, pc1,cc1, pc1_count,pc_name,mylist)

		elif (pc_name=="PC2"):
			global pc2_count
			pc2_count = pc2_count+1
			worker2 = 1
			accept_worker(connection, ip, port, pc2,cc2, pc2_count,pc_name,mylist)

		elif (pc_name=="PC3"):
			global pc3_count
			pc3_count = pc3_count+1
			worker3 = 1
			accept_worker(connection, ip, port, pc3,cc3, pc3_count,pc_name,mylist)

		elif (pc_name=="PC4"):
			global pc4_count
			pc4_count = pc4_count+1
			worker4 = 1
			accept_worker(connection, ip, port, pc4,cc4, pc4_count,pc_name,mylist)

		elif (pc_name=="PC5"):
			global pc5_count
			pc5_count = pc5_count+1
			worker5 = 1
			accept_worker(connection, ip, port, pc5,cc5, pc5_count,pc_name,mylist)

		elif (pc_name=="PC6"):
			global pc6_count
			pc6_count = pc6_count+1
			worker6 = 1
			accept_worker(connection, ip, port, pc6,cc6, pc6_count,pc_name,mylist)
		
		elif (pc_name=="PC1_c"):
			pc1_migrate = Thread(target = migrate_job_check, args=(connection, ip, port, pc_name))
			pc1_migrate.start()

		elif (pc_name=="PC2_c"):
			pc2_migrate = Thread(target = migrate_job_check, args=(connection, ip, port, pc_name))
			pc2_migrate.start()

		elif (pc_name=="PC4_c"):
			pc4_migrate = Thread(target = migrate_job_check, args=(connection, ip, port, pc_name))
			pc4_migrate.start()

		elif (pc_name=="PC6_c"):
			pc6_migrate = Thread(target = migrate_job_check, args=(connection, ip, port, pc_name))
			pc6_migrate.start()

		elif (pc_name=="PC5_c"):
			pc5_migrate = Thread(target = migrate_job_check, args=(connection, ip, port, pc_name))
			pc5_migrate.start()

		else:
			print ("Unrecognized woker PCs!!!", pc_name)


	soc.close()

def migrate_job_check(connection, ip, port, pc_name):
	global migrate_job_name_and_worker, name_worker, checkpoint_send
	print ("PC----------", migrate_job_name_and_worker)
	worker_desire = connection.recv(5120).decode("utf8")
	print (worker_desire)
	worker_want = worker_desire.split("_")
	if worker_want[1]=="prepare":
		print ("Checkpoint jobs will send "+pc_name)
		if name_worker > 0:
			checkpoint_send = 1
			accept_worker_for_checkpoint(connection, ip, port)
			#name_worker = name_worker-1
			separate = migrate_job_name_and_worker[name_worker-1]
			migrate_job_name_and_worker.remove(separate)
			name_worker = name_worker-1
			
			job_worker_separate = separate.split("_")
			accept_worker = pc_name.split('_')
			print (separate)
			print ("This ", job_worker_separate[0]+'_'+job_worker_separate[1], "job will be sent to the ", accept_worker[0])
			print ("This is the directory of PC that accepted the migrated job --->", worker_want[3])
			directoryy = './'+job_worker_separate[2]+"/"
			jobs = job_worker_separate[0]+'_'+job_worker_separate[1]
			print (directoryy)
			print (jobs)
			chk_accept_alert = connection.recv(5120).decode("utf8")
			time.sleep(5)
			if chk_accept_alert=="chk_accept_alert":
				print ("Worker is ready to accept migrated image.")
				send_original_job(connection, ip, jobs, directoryy)
			
			chk_accept_tar = connection.recv(5120).decode("utf8")
			time.sleep(5)
			if chk_accept_tar=="chk_accept_tar":
				print ("Worker is ready to accept checkpoint image.")
				jobs = job_worker_separate[0]+'_'+job_worker_separate[1]+"_c.tar.gz"
				if accept_worker[0]=="PC1":
					directoryy = './worker-1/'
					send_original_job(connection, ip, jobs, directoryy)
				elif accept_worker[0]=="PC2":
					directoryy = './worker-2/'
					send_original_job(connection, ip, jobs, directoryy)
				elif accept_worker[0]=="PC3":
					directoryy = './worker-3/'
					send_original_job(connection, ip, jobs, directoryy)
				elif accept_worker[0]=="PC4":
					directoryy = './worker-4/'
					send_original_job(connection, ip, jobs, directoryy)
				elif accept_worker[0]=="PC5":
					directoryy = './worker-5/'
					send_original_job(connection, ip, jobs, directoryy)
				else:
					directoryy = './worker-6/'
					send_original_job(connection, ip, jobs, directoryy)
		else:
			print ("There is no original job to be migrated.")
		
	else:
		job_name_and_worker = worker_want[0]+"_"+worker_want[1]+"_"+worker_want[3]
		print (job_name_and_worker)
		if job_name_and_worker not in migrate_job_name_and_worker:
			name_worker = name_worker+1
			migrate_job_name_and_worker.append(job_name_and_worker)
		else:
			None
		#migrate_job_name_and_worker.append(job_name_and_worker) if job_name_and_worker not in migrate_job_name_and_worker else None
		#if len(migrate_job_name_and_worker)==0:
		#	migrate_job_name_and_worker.append(job_name_and_worker)
		#	name_worker = name_worker+1
		#else:
		#	for check_already in migrate_job_name_and_worker:
		#		if check_already==job_name_and_worker:
		#			print ("No need to add again.")
		#		else:
		#			migrate_job_name_and_worker.append(job_name_and_worker)
		#			name_worker = name_worker+1
		print ("Please take a rest "+pc_name)
		rest_worker(connection, ip, port)

def accept_worker_for_checkpoint(connection, ip, port):
	global checkpoint_send
	if checkpoint_send==1:
		connection.sendall("checkpoint".encode("utf8"))
	else:
		time.sleep(5)
		accept_worker_for_checkpoint(connection, ip, port)

def rest_worker(connection, ip, port):
	connection.sendall("rest".encode("utf8"))

def accept_worker(connection, ip, port, pc0,cc0, pc0_count,pc_name,mylist):
	try:
		Thread(target=client_thread_new, args=(connection, ip, port, pc0,cc0, pc0_count,pc_name,mylist)).start()
	except:
		print ("Thread could not start.")
		traceback.print_exc()

def client_thread_new(connection, ip, port, directory, count,pc_count, pc_name, mylist, max_buffer_size = 5120):
	#print ("Current count ----->", pc_count)
	#print ("Maximum limit ----->", count)
	if pc_count>count:
		print ("There is no job remaining.")
		update_worker_status(pc_name)
		connection.sendall("no_job".encode("utf8"))
		time.sleep(3)
	else:
		connection.sendall("data".encode("utf8"))   #1st_send(no_of_projects)
		send_receive_jobs_new(connection, ip, port, directory, count, pc_count, pc_name, mylist)
		print ("Now counter is at :", pc_count)

def rename_job_flag_move_worker_dir(directory, mylist, my_dict, directorya):
	for assign in mylist:
		up_to = my_dict[assign]
		flag = 1
		with open('./schedule_file/schedule.csv') as f:
			reader = csv.reader(f)
			next(reader, None)
			for row in reader:
				if assign==row[0]:
					print (my_dict[assign], row[1])
					shutil.move(directory+row[1],directorya)
					new_name = str(flag)+'_'+row[1]
					os.rename(os.path.join(directorya, row[1]), os.path.join(directorya,new_name))
					shutil.move(directorya+new_name,directorya+row[0])
					waiting_dir='./status/waiting/'
					file_name=new_name+'_'+row[0]
					subprocess.call(['touch', waiting_dir+file_name])
					flag =  flag+1

def update_worker_status(pc_name):
	global worker_free_not, worker1, worker2, worker3, worker4, worker5, worker6
	if pc_name=="PC1":
		worker1 = 0
		worker_free_not = [worker1, worker2, worker3, worker4, worker5, worker6]
		print ("PC1------------------------", worker_free_not)
		worker_info = migrate_call(worker_free_not)
		worker1 = worker_info[0]
		worker2 = worker_info[1]
		worker3 = worker_info[2]
		worker4 = worker_info[3]
		worker5 = worker_info[4]
		worker6 = worker_info[5]

	elif pc_name=="PC2":
		worker2 = 0
		worker_free_not = [worker1, worker2, worker3, worker4, worker5, worker6]
		print ("PC2------------------------", worker_free_not)
		worker_info = migrate_call(worker_free_not)
		worker1 = worker_info[0]
		worker2 = worker_info[1]
		worker3 = worker_info[2]
		worker4 = worker_info[3]
		worker5 = worker_info[4]
		worker6 = worker_info[5]

	elif pc_name=="PC3":
		worker3 = 0
		worker_free_not = [worker1, worker2, worker3, worker4, worker5, worker6]
		print ("PC3------------------------", worker_free_not)
		worker_info = migrate_call(worker_free_not)
		worker1 = worker_info[0]
		worker2 = worker_info[1]
		worker3 = worker_info[2]
		worker4 = worker_info[3]
		worker5 = worker_info[4]
		worker6 = worker_info[5]

	elif pc_name=="PC4":
		worker4 = 0
		worker_free_not = [worker1, worker2, worker3, worker4, worker5, worker6]
		print ("PC4------------------------", worker_free_not)
		worker_info = migrate_call(worker_free_not)
		worker1 = worker_info[0]
		worker2 = worker_info[1]
		worker3 = worker_info[2]
		worker4 = worker_info[3]
		worker5 = worker_info[4]
		worker6 = worker_info[5]

	elif pc_name=="PC5":
		worker5 = 0
		worker_free_not = [worker1, worker2, worker3, worker4, worker5, worker6]
		print ("PC5------------------------", worker_free_not)
		worker_info = migrate_call(worker_free_not)
		worker1 = worker_info[0]
		worker2 = worker_info[1]
		worker3 = worker_info[2]
		worker4 = worker_info[3]
		worker5 = worker_info[4]
		worker6 = worker_info[5]

	else:
		worker6 = 0
		worker_free_not = [worker1, worker2, worker3, worker4, worker5, worker6]
		print ("PC6------------------------", worker_free_not)
		worker_info = migrate_call(worker_free_not)
		worker1 = worker_info[0]
		worker2 = worker_info[1]
		worker3 = worker_info[2]
		worker4 = worker_info[3]
		worker5 = worker_info[4]
		worker6 = worker_info[5]

def send_receive_jobs_new(connection, ip, port, directory, count, start_counter, pc_name, mylist):
	global measurement
	measurement = './migrate/conduct_measurement1.csv'
	file_count = 0
	for jobs in os.listdir(directory):
		data = jobs.split("_")
		if (data[0]==str(start_counter)):
			s4 = start()
			send_original_job(connection, ip, jobs, directory)
			e4 = end()
			#data_append_file(measurement, jobs, pc_name, e4, s4)
			foldName = connection.recv(5120).decode("utf8")#############################
			time.sleep(5)
			nn = connection.recv(5120).decode("utf8")
			time.sleep(5)
			done_percent = connection.recv(5120).decode("utf8")
			
			if(foldName==jobs):
				rer = start()
				print ("Receive from worker:"+foldName)
				pcName=directory.split("/")
				file_name=foldName+'_'+pcName[1]
				pre_dir='./status/running/'
				now_dir='./status/finished/'
				subprocess.call(['mv', pre_dir+file_name, now_dir+file_name])
				subprocess.call(['rm', '-r', directory+foldName])
				#os.remove(str(directory+foldName))
				dirName = './results/'+foldName+"_result/"

				#dirName = directory+foldName+"_result/"
				os.makedirs(dirName)
				subprocess.call(['chmod', '777', '-R', dirName])
				print ("Files count:", nn)
				time.sleep(5)

				for account in range(int(nn)):
					filees_name = connection.recv(5120).decode("utf8")
					time.sleep(5)
					with open(dirName+filees_name, 'wb')as f:
						datta = connection.recv(5120)
						time.sleep(5)
						if not datta:
							f.close()
							print ("File is closed.")
						f.write(datta)
					print ("Successfully get the file.")
					time.sleep(5)
				
				data_append_file1(measurement, foldName, pc_name, rer, nn)
				shutil.make_archive(dirName, 'zip', './results')
				subprocess.call(['rm', '-r', now_dir+file_name])
				subprocess.call(['rm', '-r', dirName])
				

			else:
				print ("Is there any error?")
		else:
			print ("Index out of bound Exception!!!")
				
def send_original_job(connection, ip, jobs, directory):
	connection.sendall(str(jobs).encode("utf8"))  #2nd_send(folder_name)
	time.sleep(5)
	senda = start()
	pcName=directory.split("/")
	file_name=jobs+'_'+pcName[1]
	pre_dir='./status/waiting/'
	now_dir='./status/running/'
	subprocess.call(['python3', './sender_m.py', directory+jobs, ip])
	subprocess.call(['mv', pre_dir+file_name, now_dir+file_name])
	sendb = end()

	measurement_result_file = './latest.csv'
	information = "Job send time master"
	data_msg1 = str(int(sendb)-int(senda))
	data_msg2 = convert(int(sendb)-int(senda))
	measure_latest(measurement_result_file, information, data_msg1, data_msg2)


def data_append_file(measurement, jobs, pc_name, e4, s4):
	with open('./remove_zip/jobs.csv', 'a') as csvfile1:
		fieldnames1 = ['Job Name', 'pc_name', 'pc_last_job_start', 'pc_last_job_sec']
		writerpp1 = csv.DictWriter(csvfile1, fieldnames=fieldnames1)
		writerpp1.writerow({'Job Name': jobs, 'pc_name': pc_name, 'pc_last_job_start': convert(e4), 'pc_last_job_sec': e4})
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["------------------------------------"])
		csvwriter.writerow(["Docker Image transferring time of "+jobs+" is "+convert(int(e4)-int(s4))])
		csvwriter.writerow(["Start transfer time of "+jobs+" is "+convert(int(s4))])
		csvwriter.writerow(["End transfer time of "+jobs+" is "+convert(int(e4))])
		csvwriter.writerow(["------------------------------------"])

def data_append_file1(measurement, foldName, pc_name, rer, nn):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["------------------------------------"])
		csvwriter.writerow(["Receiving time of successfully finished job - "+str(foldName)+" from worker "+pc_name+" is "+convert(int(rer))])
		csvwriter.writerow(["Number of received files - "+str(nn)])
		csvwriter.writerow(["------------------------------------"])


def receive_input(connection, max_buffer_size):
	client_input = connection.recv(max_buffer_size)
	client_input_size = sys.getsizeof(client_input)

	if client_input_size > max_buffer_size:
		print("The input size is greater than expected {}".format(client_input_size))

	decoded_input = client_input.decode("utf8").rstrip()
	return decoded_input

def start():
	start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	print ("Starting time(h:m:s)-"+start_time+" ("+start_date+")")
	return start_total
def end():
	finish_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	finish_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	finish_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	print ("Finishing time(h:m:s)-"+finish_time+" ("+finish_date+")")
	return finish_total

def convert(seconds):
	min, sec = divmod(seconds, 60)
	hour, min = divmod(min, 60)
	return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)

def measure_latest(measurement_result_file, information, data_msg1, data_msg2):
	with open(measurement_result_file, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([information, data_msg1, data_msg2])