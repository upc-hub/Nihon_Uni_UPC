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
def main():
	global pc1_count
	pc1_count = 0
	global pc2_count
	pc2_count = 0
	global pc3_count
	pc3_count = 0
	global pc4_count
	pc4_count = 0
	global chk_count
	chk_count = 0
	global pc3_chk_counter
	pc3_chk_counter = 0
	global fixed_chk
	fixed_chk = 0
	start_server_new()
	global measurement
	measurement = '/home/heinhtet/Desktop/Systematic-1/new_complete/migrate/conduct_measurement1.csv'
def start_server_new():
	
	directory = '/home/heinhtet/Desktop/Systematic-1/new_complete/remove_zip/'
	host = "192.168.56.100"
	port = 2000
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print ("-------------------------------------")
	print ("Elastic UPC Master is started.")
	global measurement
	

	try:
		soc.bind((host, port))
	except:
		print ("Bind failed error:"+ str(sys.exc_info()))
		sys.exit()
	soc.listen(120)

	entry1 = []
	worker_names1 = []
	global my_dict
	#directory = '/home/heinhtet/Desktop/Systematic-1/new_complete/remove_zip/'
	for entry_name1 in os.listdir(directory):
		entry1.append(entry_name1)
	print (entry1)
	directorya = '/home/heinhtet/Desktop/Systematic-1/new_complete/'
	with open('/home/heinhtet/Desktop/Systematic-1/new_complete/assignn12.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			worker_names1.append(row[0])
	mylist = list( dict.fromkeys(worker_names1) )
	my_dict = {i:worker_names1.count(i) for i in worker_names1}
	print ('mylist', mylist)
	print ('mydict', my_dict)
	print (my_dict[mylist[0]])

	global pc1
	global pc2
	global pc3
	global pc4
	global cc1
	global cc2
	global cc3
	global cc4
	global pc3_chk_count

	pc4 = directorya+"PC4/"
	pc3 = directorya+"PC3/"
	pc2 = directorya+"PC2/"
	pc1 = directorya+"PC1/"
	pc3_chk = directorya+"checkpoint_jobs/"
	#pc3_chk_count = 1

	cc4 = my_dict["PC4"]
	cc3 = my_dict["PC3"]
	#cc2 = my_dict["PC2"]
	cc1 = my_dict["PC1"]

	estimate_job_name = ''
	estimate_pc1_sec = ''
	estimate_pc2_sec = ''
	estimate_pc3_sec = ''
	estimate_pc4_sec = ''


	for assign in mylist:
		subprocess.call(['mkdir', directorya+assign])
		subprocess.call(['chmod', '777', '-R', directorya+assign])




	for assign in mylist:
		up_to = my_dict[assign]
		flag = 1
		with open('/home/heinhtet/Desktop/Systematic-1/new_complete/assignn12.csv') as f:
			reader = csv.reader(f)
			next(reader, None)
			for row in reader:
				if assign==row[0]:
					print (my_dict[assign], row[1])
					#subprocess.call(['mkdir', row[1]])
					#subprocess.call(['chmod', '777', '-R', directory+row[1]])
					shutil.move(directory+row[1],directorya)
					new_name = str(flag)+'_'+row[1]
					os.rename(os.path.join(directorya, row[1]), os.path.join(directorya,new_name))
					shutil.move(directorya+new_name,directorya+row[0])
					flag =  flag+1
				


	with open('/home/heinhtet/Desktop/Systematic-1/new_complete/assignn12.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			#if row[1]==:
				
			with open(directorya+'/estimate/master_time.csv') as rr:
				reader1 = csv.reader(rr)
				next(reader1, None)
				for row1 in reader1:
					

						
					if re.search(row1[0], row[1]):
						estimate_job_name = row[1]
						estimate_pc1_sec = row1[5]
						estimate_pc2_sec = row1[6]
						estimate_pc3_sec = row1[7]
						estimate_pc4_sec = row1[8]
						print ("Estimated job name:", estimate_job_name)
						with open(directorya+'remove_zip/jobs.csv', 'a') as csvfile1:
							fieldnames1 = ['Job Name', 'pc1_sec', 'pc2_sec', 'pc3_sec', 'pc4_sec']
							writerpp1 = csv.DictWriter(csvfile1, fieldnames=fieldnames1)
							#writerpp.writeheader()
							writerpp1.writerow({'Job Name': estimate_job_name, 'pc1_sec': estimate_pc1_sec, 'pc2_sec': estimate_pc2_sec, 'pc3_sec': estimate_pc3_sec, 'pc4_sec': estimate_pc4_sec})

						with open(directorya+row[0]+'/pc_time.csv', 'a') as csvfile:
							fieldnames = ['Job Name', 'pc1_sec', 'pc2_sec', 'pc3_sec', 'pc4_sec']
							writerpp = csv.DictWriter(csvfile, fieldnames=fieldnames)
							#writerpp.writeheader()
							writerpp.writerow({'Job Name': estimate_job_name, 'pc1_sec': estimate_pc1_sec, 'pc2_sec': estimate_pc2_sec, 'pc3_sec': estimate_pc3_sec, 'pc4_sec': estimate_pc4_sec})
					else:
						print ("Skip")
	global pc1_sum
	pc1_sum = 0
	global pc2_sum
	pc2_sum = 0
	global pc3_sum
	pc3_sum = 0
	global pc4_sum
	pc4_sum = 0
	for total in mylist:
		with open(directorya+total+'/pc_time.csv', 'rt')as f:
			comb = csv.reader(f)
			for row in comb:
				pc1_sum = pc1_sum+int(row[1])
				pc2_sum = pc2_sum+int(row[2])
				pc3_sum = pc3_sum+int(row[3])
				pc4_sum = pc4_sum+int(row[4])
			print (pc1_sum)
			print (pc2_sum)
			print (pc3_sum)
			print (pc4_sum)
			
			with open(directorya+total+'/'+total+'.csv', 'a')as csvfile:
				fields = ['Total', 'PC1', 'PC2', 'PC3', 'PC4'] 
				csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
				csvwriter.writeheader()
				csvwriter.writerow({'Total': 'Total', 'PC1': pc1_sum, 'PC2': pc2_sum, 'PC3': pc3_sum, 'PC4': pc4_sum})
			pc1_sum = 0
			pc2_sum = 0
			pc3_sum = 0
			pc4_sum = 0


			#with open(directorya+total+'/pc_time_1.csv', 'a') as summ:
			#	fieldnames = ['Job Name', 'pc1_sec', 'pc2_sec', 'pc3_sec', 'pc4_sec']
			#	writerpp = csv.DictWriter(csvfile, fieldnames=fieldnames)
			#	writerpp.writerow({'Job Name': 'total', 'pc1_sec': pc1_sum, 'pc2_sec': pc2_sum, 'pc3_sec': pc3_sum, 'pc4_sec': pc4_sum})




						




	e1 = end()
	
	#print ("Total unzipping time :"+ convert(int(e1)-int(s1)))
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
			try:
				global pc1_count
				pc1_count = pc1_count+1
				Thread(target=client_thread_new, args=(connection, ip, port, pc1,cc1, pc1_count,pc_name,mylist)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()

		elif (pc_name=="PC2"):
			try:
				global pc2_count
				pc2_count = pc2_count+1
				Thread(target=client_thread_new, args=(connection, ip, port, pc2,cc2, pc2_count,pc_name,mylist)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=="PC3_check"):
			print ("Check to the new checkpoint_jobs directory")
			try:
				global pc3_chk_counter
				pc3_chk_counter = pc3_chk_counter+1
				global fixed_chk
				pc3_chk_count = fixed_chk
				Thread(target=client_thread_new, args=(connection, ip, port, pc3_chk,pc3_chk_count, pc3_chk_counter,pc_name,mylist)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()

		elif (pc_name=="PC4"):
			try:
				global pc4_count
				pc4_count = pc4_count+1
				Thread(target=client_thread_new, args=(connection, ip, port, pc4,cc4, pc4_count,pc_name,mylist)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()

		elif (pc_name=="PC3"):
			try:
				global pc3_count
				pc3_count = pc3_count+1
				Thread(target=client_thread_new, args=(connection, ip, port, pc3,cc3, pc3_count,pc_name,mylist)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		else:
			print ("Thank you very much.")

		
		
	soc.close()

def client_thread_new(connection, ip, port, directory, count,pc_count, pc_name, mylist, max_buffer_size = 5120):
	#global start_counter
	#start_counter = start_counter+1
	#global count_control
	global chk_count
	print ("This is the check count.", chk_count)

	if pc_count>count:
		if chk_count==0:
			print ("There is no job remaining.")
			connection.sendall("no_job".encode("utf8"))
			connection.close()
		else:
			connection.sendall("check".encode("utf8"))
			print ("PC-3 will send PC3_check.")
			#time.sleep(5)
			#pc_nick = connection.recv(5120).decode("utf8")#available PC name
			#print (pc_nick+"is waiting to receive any checkpoint image")
			#chk_count=0
			connection.close()

		#time.sleep(5)
		#check_dir = '/home/heinhtet/Desktop/Systematic-1/new_complete/checkpoint_jobs/'
		#subprocess.call(['python3', '/home/heinhtet/Desktop/Systematic-1/sender.py', check_dir+jobs, ip])
		
	else:
		connection.sendall("data".encode("utf8"))   #1st_send(no_of_projects)
		#count_control = count_control-1
		#while start_counter<=count:
		send_receive_jobs_new(connection, ip, port, directory, count, pc_count, pc_name, mylist)
		print ("Now counter is at :", pc_count)
	
		#start_counter = 0
		#is_active = False
	
	

	#is_active = True
	#while is_active:





	#	client_input = receive_input(connection, max_buffer_size)
	#	if "__quit__" in client_input:
	#		print ("Client is requesting to quit.")
	#		connection.close()
	#		is_active = False
	#	else:
	#		print ("Processed result:{}".format(client_input))
	#		connection.sendall("-".encode("utf8"))

def send_receive_jobs_new(connection, ip, port, directory, count, start_counter, pc_name, mylist):
	global measurement
	measurement = '/home/heinhtet/Desktop/Systematic-1/new_complete/migrate/conduct_measurement1.csv'
	global chk_count
	global fixed_chk
	#print (entry_names)
	
		
		


	file_count = 0
	for jobs in os.listdir(directory):
		data = jobs.split("_")
		if (data[0]==str(start_counter)):
			connection.sendall(str(jobs).encode("utf8"))  #2nd_send(folder_name)
			time.sleep(5)
			try:
				if (data[2]=="c"):
					chk_count = chk_count-1
					print ("Send via ftp.")
					chk_directory = '/home/heinhtet/Desktop/Systematic-1/new_complete/checkpoint_data/'
					for fold_name in os.listdir(chk_directory):
						fold_name_data = fold_name.split("_")
						if (fold_name_data[0]==str(start_counter)):
							s_c = start()
							connection.sendall(str(fold_name).encode("utf8"))
							print ("Send checkpoint Name:", fold_name)
							subprocess.call(['scp', '/home/heinhtet/Desktop/Systematic-1/new_complete/checkpoint_data/'+fold_name, 'root@192.168.56.105:/tmp'])
							os.chdir('/home/heinhtet/Desktop/Systematic-1/new_complete/checkpoint_data/')
							subprocess.call(['rm', '-r', fold_name])
							e_c = end()
							with open(measurement, 'a') as csvfile:
								csvwriter = csv.writer(csvfile)
								csvwriter.writerow([""])
								csvwriter.writerow(["Docker checkpoint data(tar file) transferring time of "+fold_name+"is"+convert(int(e_c)-int(s_c))])
						else:
							print ("Error at checkpoint data sending")
						
					#connection.sendall()
					
			except IndexError:
				print ("There is no checkpoint (or) assigned job lists are not finished till.")
			
			s4 = start()
			subprocess.call(['python3', '/home/heinhtet/Desktop/Systematic-1/sender.py', directory+jobs, ip])
			
			e4 = end()
			print ("Docker Image transferring time*********"+convert(int(e4)-int(s4))+"*****")
			with open('/home/heinhtet/Desktop/Systematic-1/new_complete/remove_zip/jobs.csv', 'a') as csvfile1:
				fieldnames1 = ['Job Name', 'pc_name', 'pc_last_job_start', 'pc_last_job_sec']
				writerpp1 = csv.DictWriter(csvfile1, fieldnames=fieldnames1)
				#writerpp.writeheader()
				writerpp1.writerow({'Job Name': jobs, 'pc_name': pc_name, 'pc_last_job_start': convert(e4), 'pc_last_job_sec': e4})
			with open(measurement, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				csvwriter.writerow(["Docker Image transferring time of "+jobs+"is"+convert(int(e4)-int(s4))])

			foldName = connection.recv(5120).decode("utf8")#############################
			time.sleep(5)
			nn = connection.recv(5120).decode("utf8")
			time.sleep(5)
			done_percent = connection.recv(5120).decode("utf8")
			if(foldName==jobs):
				print ("Receive from worker:"+foldName)
				os.remove(str(directory+foldName))
				dirName = directory+foldName+"/"
				os.makedirs(dirName)
				subprocess.call(['chmod', '777', '-R', dirName])

				#files_count = connection.recv(5120).decode("utf8")
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
			else:
				print ("Receive from worker:"+foldName)
				print ("Possible worker with such job:"+nn)
				print ("done percentage"+done_percent)
				time.sleep(5)

				#global chk_count
				chk_count = chk_count+1
				fixed_chk = chk_count
				load_org_dock = directory+jobs

				time_compare = []
				worker_compare = []


				chk_img = foldName+'.tar.gz'
				chk_job = '/home/heinhtet/Desktop/Systematic-1/new_complete/checkpoint_jobs/'
				print ("This is the transfer directory for load original docker Image >>> "+load_org_dock)
				print ("This is the transfer checkpoint Image >>> "+chk_img)
				shutil.move(load_org_dock, chk_job)
				#shutil.move('/home/heinhtet/Desktop/Systematic-1/new_complete/estimate/'+pc_name+'.csv', chk_job)
				typecast = ''
				typecast1 = ''
				for total in mylist:
					if pc_name==total:
						print ("It is not required to check the duration")
						shutil.move('/home/heinhtet/Desktop/Systematic-1/new_complete/'+total+'/pc_time.csv', chk_job)
					else:
						shutil.move('/home/heinhtet/Desktop/Systematic-1/new_complete/'+total+'/'+total+'.csv', chk_job)
						index = re.findall('(\d+)', total)
						#typecast = index
						with open(chk_job+total+'.csv', 'rt') as f:
						    reader = csv.reader(f)
						    i = next(reader)
						    worker_compare.append(i[int(typecast1.join(index))])
						
						with open(chk_job+total+'.csv', 'rt')as f:
							comb = csv.reader(f)
							#reader = csv.reader(f)
							next(comb, None)
							for row in comb:
								time_compare.append(row[int(typecast.join(index))])
				print ("----------------------------------")
				print ("Worker compare", worker_compare)
				print ("Time compare", time_compare)
				print ("----------------------------------")
				smallest_duration = int(time_compare[0])
				smallest_index = 0
				for i in range(len(time_compare)):
					if int(time_compare[i])<smallest_duration:
						smallest_duration = int(time_compare[i])
						smallest_index = int(i)
				print ("The most efficient PC is ", worker_compare[smallest_index], "and the working duration is ", convert(smallest_duration), "(", smallest_duration,")")
				print ("----------------------------------")
				standard = 0
				with open(chk_job+'pc_time.csv', 'rt')as f:
					comb = csv.reader(f)
					for row in comb:
						if row[0]==nn:
							standard = row[int(typecast.join(re.findall('(\d+)', worker_compare[smallest_index])))]
						else:
							print ("")
				print ("The standard cpu time of checkpoint job(", nn, ")executing at current efficient worker(", worker_compare[smallest_index], ")is ", convert(int(standard)), "(", standard,")")
				print ("----------------------------------")
				print ("Checkpoint job finishing percent before interrupt is ", done_percent, "%")
				finish_percentage = int(float(float(standard)-((float(done_percent)/100)*float(standard))))
				print ("The remaining time of ", nn, "if it will execute at", worker_compare[smallest_index], "is ",convert(finish_percentage), "(", finish_percentage,")")
				print ("----------------------------------")

						#l=[l for time_compare in input("List:").split(",")]
						#min1 = l[0]
						#for i in range(len(l)):
						#	if l[i] < min1:
						#		min1 = l[i]
						#		worker1 = worker_compare[i]
						#print ("The most possible worker is ", worker1, " and the duration is ", min1)
						#time_compare.sort()
						#print("Smallest element is:", *list1[:1])
				#with open('/home/heinhtet/Desktop/Systematic-1/new_complete/remove_zip/jobs.csv') as rr:
				#	reader1 = csv.reader(rr)
				#	next(reader1, None)
				#	for row1 in reader1:

				



				os.rename(os.path.join(chk_job, jobs), os.path.join(chk_job,jobs+'_'+'c'))


				#foldNamea = connection.recv(5120).decode("utf8")
				#print ("Receive from worker:"+foldNamea)
				#os.remove(str(directory+foldNamea))
				dirName = directory+nn+"/"
				os.makedirs(dirName)
				subprocess.call(['chmod', '777', '-R', dirName])

				files_count = connection.recv(5120).decode("utf8")
				print ("Files count:", files_count)
				time.sleep(5)

				for account in range(int(files_count)):
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
				
				#try:
				#shutil.move(load_org_dock, chk_job)
					
				#except OSError:
				#	print ()
				

				#subprocess.call(['python3', '/home/heinhtet/Desktop/Systematic-1/new_complete/receiver.py'])
			
			back_data = connection.recv(5120).decode("utf8")
			if "finish" in back_data:
				print ("Check is there any other jobs")
				time.sleep(5)
				connection.close()
				exit()
				#construct_files(connection, file_name)

		else:
			print ("False")

# def start_server(directory,count,entry_names,s1):
# 	host = "192.168.11.10"
# 	port = 2000
# 	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 	print ("-------------------------------------")
# 	print ("Elastic UPC Master is started.")
# 	global start_counter
# 	start_counter = 0
# 	global count_control
# 	count_control = count
# 	try:
# 		soc.bind((host, port))
# 	except:
# 		print ("Bind failed error:"+ str(sys.exc_info()))
# 		sys.exit()
# 	soc.listen(120)


# 	flag = 1
# 	for fold_name in os.listdir(directory):
# 		os.rename(os.path.join(directory, fold_name), os.path.join(directory,str(flag)+'_'+fold_name))
# 		flag = flag+1



# 	for jobs in os.listdir(directory):
# 		print (jobs)
# 	print ("No. of projects = ",count)
# 	time.sleep(5)
# 	e1 = end()
# 	print ("Total unzipping time :"+ convert(int(e1)-int(s1)))
# 	print ("UPC Master is now listening the workers")
# 	print ("-------------------------------------")
# 	while True:
# 		connection, address = soc.accept()
# 		ip, port = str(address[0]), str(address[1])
# 		print ("A worker node connected with "+ip+" : "+port)
		
# 		try:
# 			Thread(target=client_thread, args=(connection, ip, port, directory,count, entry_names)).start()
# 		except:
# 			print ("Thread could not start.")
# 			traceback.print_exc()
# 	soc.close()

# def client_thread(connection, ip, port, directory, count,entry_names, max_buffer_size = 5120):
# 	global start_counter
# 	start_counter = start_counter+1
# 	global count_control

# 	if start_counter>count:
# 		print ("There is no job remaining.")
# 		connection.sendall("no_job".encode("utf8"))
# 		connection.close()
# 	else:
# 		connection.sendall(str(count_control).encode("utf8"))   #1st_send(no_of_projects)
# 		count_control = count_control-1
# 		#while start_counter<=count:
# 		send_receive_jobs(connection, ip, port, directory, entry_names, count, start_counter)
# 		print ("Now counter is at :", start_counter)
	
# 		#start_counter = 0
# 		#is_active = False
	
	

# 	is_active = True
# 	while is_active:





# 		client_input = receive_input(connection, max_buffer_size)
# 		if "__quit__" in client_input:
# 			print ("Client is requesting to quit.")
# 			connection.close()
# 			is_active = False
# 		else:
# 			print ("Processed result:{}".format(client_input))
# 			connection.sendall("-".encode("utf8"))

def receive_input(connection, max_buffer_size):
	client_input = connection.recv(max_buffer_size)
	client_input_size = sys.getsizeof(client_input)

	if client_input_size > max_buffer_size:
		print("The input size is greater than expected {}".format(client_input_size))

	decoded_input = client_input.decode("utf8").rstrip()
	return decoded_input

# def send_receive_jobs(connection, ip, port, directory, entry_names, count, start_counter):
# 	print (entry_names)
	
		
		


# 	file_count = 0
# 	for jobs in os.listdir(directory):
# 		data = jobs.split("_")
# 		if (data[0]==str(start_counter)):
# 			connection.sendall(str(jobs).encode("utf8"))  #2nd_send(folder_name)
# 			time.sleep(5)
# 			s4 = start()
# 			subprocess.call(['python3', '/home/heinhtet/Desktop/Systematic-1/sender.py', directory+jobs, ip])
# 			e4 = end()
# 			print ("Docker Image transferring time*********"+convert(int(e4)-int(s4))+"*****")

# 			foldName = connection.recv(5120).decode("utf8")
# 			os.remove(str(directory+foldName))
# 			dirName = directory+foldName+"/"
# 			os.makedirs(dirName)
# 			subprocess.call(['chmod', '777', '-R', dirName])

# 			files_count = connection.recv(5120).decode("utf8")
# 			print ("Files count:", files_count)
# 			time.sleep(5)

# 			for account in range(int(files_count)):
# 				filees_name = connection.recv(5120).decode("utf8")
# 				time.sleep(5)
# 				with open(dirName+filees_name, 'wb')as f:
# 					datta = connection.recv(5120)
# 					time.sleep(5)
# 					if not datta:
# 						f.close()
# 						print ("File is closed.")
# 					f.write(datta)
# 				print ("Successfully get the file.")
# 				time.sleep(5)
			
# 			back_data = connection.recv(5120).decode("utf8")
# 			if "finish" in back_data:
# 				print ("Check is there any other jobs")
# 				connection.close()
# 				exit()
# 				#construct_files(connection, file_name)

# 		else:
# 			print ("False")
	
	

#def construct_files(connection, file_name):
#	f = open(file_name, 'rb')
#	I = f.read(5120)
#	while (I):
#		connection.send(I)
#		I = f.read(5120)
#	f.close()
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
if __name__=="__main__":
	main()	
#print (str(folder_names)[1:-1])



