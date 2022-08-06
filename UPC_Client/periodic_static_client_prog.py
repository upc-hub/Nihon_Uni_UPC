import socket
import sys, os
import datetime
import time
import subprocess
import csv
import json
global counter
from threading import Thread
counter = 0
global jobs_name, periodic, periodic_counter
jobs_name = ""
periodic, periodic_counter = 0, 0
def periodic_static_client_main1(host, port):
	global move_container_master, chk_main_counter, jobs_name
	move_container_master, chk_main_counter = '', 0
	print ("----------------------------------------")
	print ("----------------------------------------")
	print (host, "******", port)
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		soc.bind((host, port))
	except:
		print ("Bind failed error:"+ str(sys.exc_info()))
	soc.listen(120)
	while True:
		connection, address = soc.accept()
		ip, port = str(address[0]), str(address[1])
		print ("A master node connected with "+ip+" : "+port)
		time.sleep(5)
		message = connection.recv(5120).decode("utf8")
		print ("----------------------------------------")
		print (message)
		print ("----------------------------------------")
		time.sleep(5)
		message1 = connection.recv(5120).decode("utf8")
		print ("----------------------------------------")
		print (message1)
		print ("----------------------------------------")
		file = './master_worker_info_client.json'
		workerName = worker_name(file)
		move_container_master = jobs_name+"_"+message+"_"+str(workerName)+"_"+message1
		print ("hein htet",move_container_master)
		time.sleep(5)
		connection.sendall(move_container_master.encode("utf8"))
		if message=="stop":
			checkpointing(message1)
			chk_main_counter = 1
		else:
			accepting()
			chk_main_counter = 1

def checkpointing(message1):
	global jobs_name
	chka = start()
	os.system('podman container checkpoint -l --ignore-rootfs --export=/tmp/'+jobs_name+'_c.tar.gz')
	chkb = end()

	file = './master_worker_info_client.json'
	worker_ip = worker_info(file)
	subprocess.call(['scp', '/tmp/'+jobs_name+'_c.tar.gz', 'root@'+worker_ip+':/home/heinhtet/Desktop/UPC_APLAS/'+message1+'/'])
	print (message1)
	subprocess.call(['rm', '-r', '/tmp/'+jobs_name+'_c.tar.gz'])
	chkc = end()

	measurement_result_file = './latest.csv'
	information = "Checkpointing time"
	data_msg1 = str(int(chkb)-int(chka))
	data_msg2 = convert(int(chkb)-int(chka))
	measure_latest(measurement_result_file, information, data_msg1, data_msg2)

	information = "Checkpoint transfer time"
	data_msg1 = str(int(chkc)-int(chkb))
	data_msg2 = convert(int(chkc)-int(chkb))
	measure_latest(measurement_result_file, information, data_msg1, data_msg2)

def accepting():
	print ("I will accept the migrated job.")

def worker_name(info):
	worker_information = ''
	with open(info) as json_file:
		data = json.load(json_file)
		for worker in data["worker"]:
			worker_information = worker['worker name']
	return worker_information

def worker_info(info):
	worker_information = ''
	with open(info) as json_file:
		data = json.load(json_file)
		for worker in data["master"]:
			worker_information = worker['IP_address']
	return worker_information

def periodic_static_client_main(host, port, worker_name):
	global jobs_name, g, counter, stop_threads, tha, tha1, soc, measurement, move_container_master, chk_main_counter
	jobs_name, g = "", ""
	stop_threads, tha, tha1 = False, False, False
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	a = start()
	measurement = './conduct_measurement.csv'

	try:
		soc.connect((host, int(port)))
	except:
		print("Connection error")
		sys.exit()
	time.sleep(5)

	if counter == 0:
		print (worker_name)
		soc.sendall(worker_name.encode("utf8"))
	else:
		if chk_main_counter == 1:
			checkpoint_request = str(worker_name)+"_c" 
			soc.sendall(checkpoint_request.encode("utf8"))
			print (checkpoint_request)
			time.sleep(10)
			print (move_container_master,"_second send")
			move_container_master1 = move_container_master.split("_")
			print (move_container_master1)
			#to_send_chkpoint = move_container_master1[1]+"_"+move_container_master1[2]+"_"+move_container_master1[3]
			#print (to_send_chkpoint)
			soc.sendall(move_container_master.encode("utf8"))
		else:
			periodic_static_client_main(host, port, worker_name)

	global directory
	directory = '/home/upc/'
	jobs_no = soc.recv(5120).decode("utf8")
	print (jobs_no)
	if jobs_no=="no_job":
		counter = 1
		print ("It can be still accept the checkpoint migrated jobs.")
		periodic_static_client_main(host, port, worker_name)
	elif jobs_no=="check":
		counter = 1
		print ("PC can still accept extra checkpoint jobs.")
		periodic_static_client_main(host, port, worker_name)
	elif jobs_no=="checkpoint":
		checkpoint_will_accept(soc, measurement, directory)
	elif jobs_no=="rest":
		rest_worker(soc)
	elif jobs_no=="data":
		main_job_call(jobs_no, measurement, directory)
		
	else:
		periodic_static_client_main(host, port, worker_name)
	soc.sendall("finish".encode("utf8"))
	for fills_name in os.listdir(directory):
		os.remove(str(directory+fills_name))
	time.sleep(5)
	subprocess.call(['podman', 'container', 'prune', '-f'])
	periodic_static_client_main(host, port, worker_name)
	
	print("Enter 'quit' to exit")
	message = input(" -> ")

	while message != 'quit':
		soc.sendall(message.encode("utf8"))

		if soc.recv(5120).decode("utf8") == "-":
			pass        # null operation

		message = input(" -> ")

	soc.send(b'--quit--')

def main_job_call(jobs_no, measurement, directory):
	print ("No. of jobs at master", jobs_no)
	global jobs_name, periodic
	jobs_name = soc.recv(5120).decode("utf8")
	global check
	check = jobs_name.split("_")
	print ("Receive job names:", jobs_name)
	data_append2(measurement, jobs_name)
	
	dd = jobs_name.split("_")
	try:
		print ("Check error or not"+dd[2])
		print ("This is creating checkpoint empty container.")
		docker_name = 'pollen5005/'+dd[1]+":latest"
		print ("Container name:", docker_name)
		checkpoint_name = dd
		print ("Recive checkpoint Name:", checkpoint_name)

		try:
			checkpoint_restore(measurement, jobs_name, directory, soc)

		except KeyboardInterrupt:
			print ("Checkpoint name:"+jobs_name)
			subprocess.call(['docker', 'checkpoint', 'create', '--checkpoint-dir=/tmp', jobs_name, check[0]+'_checkpoint'])
			os.chdir('/tmp')
			subprocess.call(['tar', 'czf', check[0]+'_checkpoint.tar.gz', check[0]+'_checkpoint'])
			soc.sendall(str(check[0]+'_checkpoint').encode("utf8"))
			#time.sleep(5)
			#subprocess.call(['python3', './sender.py', 'checkpoint'+check[0]+'.tar.gz', '192.168.56.100'])
			subprocess.call(['scp', check[0]+'_checkpoint.tar.gz', 'root@192.168.56.100:/home/heinhtet/Desktop/UPC_APLAS/checkpoint_data/'])
			subprocess.call(['rm', '-r', check[0]+'_checkpoint', check[0]+'_checkpoint.tar.gz'])
	except IndexError:
		docker_name = podman_loading(dd, jobs_name, measurement)
		g = start()
		s5 = start()
		periodic = 1
		subprocess.call(['podman', 'run', '-t', '--name', jobs_name, '-v', '/home/upc/:/opt',docker_name])
		while True:
			
			e5 = end()
			data_append8(measurement, s5, jobs_name)
			if tha:
				while True:
					if tha1:
						break
				break
			print ("No interrupt..............................................................")
			print ("Docker Container Running time:*******"+convert(int(e5)-int(s5))+"********")
			data_append7(measurement, jobs_name, e5, s5)

			s6 = start()
			soc.sendall(str(jobs_name).encode("utf8"))
			time.sleep(5)

			fill_count = 0
			for fills_name in os.listdir(directory):
				fill_count = fill_count+1
			print ("Total no. of result files", fill_count)
			soc.sendall(str(fill_count).encode("utf8"))
			time.sleep(5)
			soc.sendall(str('sss').encode("utf8"))
			time.sleep(5)
			for fills_name in os.listdir(directory):
				print (fills_name)
				soc.sendall(str(fills_name).encode("utf8"))
				time.sleep(5)
				fa = open(directory+fills_name, 'rb')
				I = fa.read(5120)
				while(I):
					soc.send(I)
					time.sleep(5)
					I = fa.read(5120)
				fa.close()
				time.sleep(5)
			e6 = end()
			print ("Result transferring time:*******"+convert(int(e6)-int(s6))+"********")
			data_append9(measurement, jobs_name, e6, s6)
			break

def periodic_checkpointing(host, port, worker_name,soc):
	global periodic
	if periodic==0:
		print ("00000000000000000000000000000000000")
		print ("Hello World, Hein Htet.", worker_name)
		print ("00000000000000000000000000000000000")
		soc.sendall("periodic checkpoint will not send from".encode("utf8"))
		time.sleep(60)
	else:
		soc.sendall("periodic".encode("utf8"))
		create_periodic_checkpoint(worker_name)
		time.sleep(60)

def create_periodic_checkpoint(worker_name):
	global periodic_counter
	periodic_counter = periodic_counter+1
	os.system('podman container checkpoint -l --ignore-rootfs -R --export=/tmp/'+str(periodic_counter)+'_'+jobs_name+'_c.tar.gz')
	time.sleep(3)
	file = './master_worker_info_client.json'
	worker_ip = worker_info(file)
	new_worker_name = worker_name_conversion(worker_name)
	subprocess.call(['scp', '/tmp/'+str(periodic_counter)+'_'+jobs_name+'_c.tar.gz', 'root@'+worker_ip+':/home/heinhtet/Desktop/UPC_APLAS/periodic/'+new_worker_name+'/'])
	subprocess.call(['rm', '-r', '/tmp/'+str(periodic_counter)+'_'+jobs_name+'_c.tar.gz'])

def worker_name_conversion(worker_name):
	if worker_name=="PC1":
		return "worker-1"
	elif worker_name=="PC2":
		return "worker-2"
	elif worker_name=="PC3":
		return "worker-3"
	elif worker_name=="PC4":
		return "worker-4"
	elif worker_name=="PC5":
		return "worker-5"
	else:
		return "worker-6"

def periodic_static_client_main2(host, port, worker_name):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		soc.connect((host, int(port)))
	except:
		print("Connection error")
		sys.exit()
	time.sleep(5)
	soc.sendall(str(worker_name).encode("utf8"))
	time.sleep(5)
	while True:
		periodic_checkpointing(host, port, worker_name, soc)

def checkpoint_restore(measurement, jobs_name, directory, soc):
	s_resume = start()	
	subprocess.call(['python3', './receiver_c.py'])
	e_resume = end()
	data_append3(measurement, s_resume, e_resume)
	
	subprocess.call(['podman', 'container', 'restore', '--import=/tmp/'+jobs_name, '-n', 'oooo'])
	s5 = start()
	while True:
		tmm = os.popen("podman ps").read()
		counc = tmm.count("oooo")
		if (counc==0):
			print ("Job is still running. Job count is", counc)
			break
		print ("Executing......")
		time.sleep(5)
	print ("Finished executing.")
	subprocess.call(['rm', '-r', '/tmp/'+jobs_name])
	e5 = end()
	print ("Docker Container checkpoint Running time:*******"+convert(int(e5)-int(s5))+"********")
	data_append4(measurement, s5, e5, jobs_name)

	s6 = start()
	soc.sendall(str(jobs_name).encode("utf8"))
	time.sleep(5)

	fill_count = 0
	for fills_name in os.listdir(directory):
		fill_count = fill_count+1
	print ("Total no. of checkpoint result files", fill_count)
	soc.sendall(str(fill_count).encode("utf8"))
	time.sleep(5)
	soc.sendall(str('sss').encode("utf8"))
	time.sleep(5)
	for fills_name in os.listdir(directory):
		print (fills_name)
		soc.sendall(str(fills_name).encode("utf8"))
		time.sleep(5)
		fa = open(directory+fills_name, 'rb')
		I = fa.read(5120)
		while(I):
			soc.send(I)
			time.sleep(5)
			I = fa.read(5120)
		fa.close()
		time.sleep(5)
	e6 = end()
	print ("Checkpoint result transferring time:*******"+convert(int(e6)-int(s6))+"********")
	data_append5(measurement, jobs_name, e6, s6)
	soc.close()

def checkpoint_will_accept(soc, measurement, directory):
	print ("----------------------------")
	print ("Checkpoint will be accepted...................")
	print ("----------------------------")
	accept_info = soc.sendall("chk_accept_alert".encode("utf8"))
	print ("Checkpoint alert is sent to accept migrated job.")
	time.sleep(5)
	jobs_no = soc.recv(5120).decode("utf8")
	print ("This original job ", jobs_no, "is received for accepting migrated job.")
	time.sleep(5)
	#time.sleep(5)
	#jobs_name = soc.recv(5120).decode("utf8")
	dd = jobs_no.split("_")
	podman_loading(dd, jobs_no, measurement)
	print ("Finished original migrated job loading.")
	accept_info_chk = soc.sendall("chk_accept_tar".encode("utf8"))
	time.sleep(5)
	jobs_name = soc.recv(5120).decode("utf8")
	print ("This ", jobs_name, " is received to restore.")
	time.sleep(5)
	checkpoint_restore(measurement, jobs_name, directory, soc)



def podman_loading(dd, jobs_name, measurement):
	docker_name = 'pollen5005/'+dd[1]+":latest"
	print ("Container name:", docker_name)
	run_time = 0	
	sa = start()
	subprocess.call(['python3', './receiver_m.py'])
	ea = end()
	s4 = start()
	subprocess.call(['podman', 'load', '-i', jobs_name])
	e4 = end()
	print ("Docker Image Loading time:*******"+convert(int(e4)-int(s4))+"********")
	
	measurement_result_file = './latest.csv'
	information = "Docker image loading time"
	data_msg1 = str(int(e4)-int(s4))
	data_msg2 = convert(int(e4)-int(s4))
	measure_latest(measurement_result_file, information, data_msg1, data_msg2)
	
	information = "Job receiving time"
	data_msg1 = str(int(ea)-int(sa))
	data_msg2 = convert(int(ea)-int(sa))
	measure_latest(measurement_result_file, information, data_msg1, data_msg2)
	data_append6(measurement, sa, ea)
	
	os.remove(str(jobs_name))
	return docker_name


def rest_worker(soc):
	print ("----------------------------")
	print ("No more job and take a rest for a while...................")
	print ("----------------------------")

def measure_latest(measurement_result_file, information, data_msg1, data_msg2):
	with open(measurement_result_file, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([information, data_msg1, data_msg2])

def data_append2(measurement, jobs_name):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["-----------------------"])
		#csvwriter.writerow(["Total no. of jobs will be received from master is ", jobs_no])
		csvwriter.writerow(["Current received job is ", jobs_name])
		#csvwriter.writerow(["-----------------------"])

def data_append3(measurement, s_resume, e_resume):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["-----------------------"])
		csvwriter.writerow(["Interrupted job start-receiving time", convert(int(s_resume))])
		csvwriter.writerow(["Interrupted job end-receiving time", convert(int(e_resume))])
		csvwriter.writerow(["How long receiving time", convert(int(e_resume)-int(s_resume))])

def data_append4(measurement, s5, e5, jobs_name):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["-----------------------"])
		csvwriter.writerow(["Interrupted job checkpoint start-running time"+ convert(int(s5))])
		csvwriter.writerow(["Interrupted job checkpoint stop-running time"+ convert(int(e5))])
		csvwriter.writerow(["How long interrupted job checkpoint running time"+jobs_name+" is "+convert(int(e5)-int(s5))])

def data_append5(measurement, jobs_name, e6, s6):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["-----------------------"])
		csvwriter.writerow(["Interrupted job result transferring time of "+jobs_name+" is "+convert(int(e6)-int(s6))])

def data_append6(measurement, sa, ea):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["-----------------------"])
		csvwriter.writerow(["Normal job start-receiving time", convert(int(sa))])
		csvwriter.writerow(["Normal job end-receiving time", convert(int(ea))])
		csvwriter.writerow(["How long normal job receiving time", convert(int(ea)-int(sa))])

def data_append7(measurement, jobs_name, e5, s5):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["Docker (without interrupt) Container Running time of "+jobs_name+" is "+convert(int(e5)-int(s5))])

def data_append8(measurement, s5, jobs_name):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["-----------------------"])
		csvwriter.writerow(["Start executing time"+convert(int(s5))+" of job "+ str(jobs_name)])

def data_append9(measurement, jobs_name, e6, s6):
	with open(measurement, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["Docker Container result transferring time of "+jobs_name+" is "+convert(int(e6)-int(s6))])

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