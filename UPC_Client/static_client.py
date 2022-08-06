import socket
import sys, os
import datetime
import time
import subprocess
import csv
global counter
from pynput import keyboard
from threading import Thread

def static_client_main(host, port, worker_name):
	global jobs_name, g, counter, stop_threads, tha, tha1, soc, measurement
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

	soc.sendall(worker_name.encode("utf8"))

	global directory
	directory = '/home/upc/'
	jobs_no = soc.recv(5120).decode("utf8")
	if jobs_no=="no_job":
		soc.close()
	elif jobs_no=="check":
		counter = 1
		print ("PC can still accept extra checkpoint jobs.")
		main()
	else:
		print ("No. of jobs at master", jobs_no)
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
			data_append6(measurement, sa, ea)
			
			os.remove(str(jobs_name))
			g = start()
			s5 = start()
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
	soc.sendall("finish".encode("utf8"))
	for fills_name in os.listdir(directory):
		os.remove(str(directory+fills_name))
	time.sleep(5)
	subprocess.call(['podman', 'container', 'prune'])
	main()
	
	print("Enter 'quit' to exit")
	message = input(" -> ")

	while message != 'quit':
		soc.sendall(message.encode("utf8"))

		if soc.recv(5120).decode("utf8") == "-":
			pass        # null operation

		message = input(" -> ")

	soc.send(b'--quit--')

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