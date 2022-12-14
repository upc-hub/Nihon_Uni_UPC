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
	global real_pp, real_ee, pc1_count, pc2_count, pc3_count, pc4_count, pc5_count, pc6_count, chk_count, pc5_chk_counter, pc6_chk_counter, pc3_chk_counter, pc4_chk_counter, pc2_chk_counter, pc1_chk_counter, fixed_chk5, fixed_chk6, fixed_chk3, fixed_chk4, fixed_chk33, fixed_chk2, count_job_four, count_job_three, fixed_chk1, pc33, pc44, measurement
	real_pp, real_ee = [], []
	pc1_count, pc2_count, pc3_count, pc4_count, pc5_count, pc6_count, chk_count, pc5_chk_counter, pc6_chk_counter, pc3_chk_counter, pc4_chk_counter, pc2_chk_counter, pc1_chk_counter, fixed_chk5, fixed_chk6, fixed_chk3, fixed_chk4, fixed_chk33, fixed_chk2, fixed_chk1, pc33, pc44, count_job_four, count_job_three = 0, 0, 0, 0, 0, 0, 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0
	start_server_new() 
	measurement = './conduct_measurement1.csv'


def start_server_new():
	directory = './remove_zip/'
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

	worker_names1 = []
	global my_dict
	directorya = './'
	with open('./assign12.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			worker_names1.append(row[0])
	mylist = list( dict.fromkeys(worker_names1) )
	my_dict = {i:worker_names1.count(i) for i in worker_names1}
	#print ('worker list accordance with assign12', mylist)
	#print ('worker and job list for each accordance with assign12', my_dict)
	#print (my_dict[mylist[0]])

	global pc1, pc2, pc3, pc4, pc5, pc6, cc1, cc2, cc3, cc4, cc5, cc6, pc3_chk_count

	pc6, pc5, pc4, pc3, pc2, pc1 = directorya+"PC6/", directorya+"PC5/", directorya+"PC4/", directorya+"PC3/", directorya+"PC2/", directorya+"PC1/"
	pc6_chk, pc5_chk, pc4_chk, pc3_chk, pc2_chk, pc1_chk = directorya+"PC6_c/", directorya+"PC5_c/", directorya+"PC4_c/", directorya+"PC3_c/", directorya+"PC2_c/", directorya+"PC1_c/"

	#cc6 = my_dict["PC6"]
	#cc5 = my_dict["PC5"]
	#cc4 = my_dict["PC4"]
	cc3 = my_dict["PC3"]
	#cc2 = my_dict["PC2"]
	#cc1 = my_dict["PC1"]

	
	#process_dir_creation(directorya, mylist)
	
	rename_job_flag_move_worker_dir(directory, mylist, my_dict, directorya)
	
	#generate_csv_worker_each_jobTime(directorya)
	
	#generate_csv_worker_totalTime(mylist, directorya)

	#generate_time_estimate_file(mylist, directorya)
	

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
			accept_worker(connection, ip, port, pc1,cc1, pc1_count,pc_name,mylist)

		elif (pc_name=="PC2"):
			global pc2_count
			pc2_count = pc2_count+1
			accept_worker(connection, ip, port, pc2,cc2, pc2_count,pc_name,mylist)


		elif (pc_name=="PC3"):
			global pc3_count
			pc3_count = pc3_count+1
			accept_worker(connection, ip, port, pc3,cc3, pc3_count,pc_name,mylist)

		elif (pc_name=="PC4"):
			global pc4_count
			pc4_count = pc4_count+1
			accept_worker(connection, ip, port, pc4,cc4, pc4_count,pc_name,mylist)

		elif (pc_name=="PC6"):
			global pc6_count
			pc6_count = pc6_count+1
			accept_worker(connection, ip, port, pc6,cc6, pc6_count,pc_name,mylist)


		elif (pc_name=="PC1_c"):
			print ("Check to the new checkpoint_jobs directory")
			global pc1_chk_counter
			pc1_chk_counter = pc1_chk_counter+1
			global fixed_chk1
			pc1_chk_count = fixed_chk1
			accept_worker(connection, ip, port, pc1_chk,pc1_chk_count, pc1_chk_counter,pc_name,mylist)

		elif (pc_name=="PC2_c"):
			print ("Check to the new checkpoint_jobs directory")
			global pc2_chk_counter
			pc2_chk_counter = pc2_chk_counter+1
			global fixed_chk2
			pc2_chk_count = fixed_chk2
			accept_worker(connection, ip, port, pc2_chk,pc2_chk_count, pc2_chk_counter,pc_name,mylist)

		elif (pc_name=="PC3_cc"):
			print ("Join worker and send checkpoint image job.")
			global pc33
			global pc3_chk_counter
			global fixed_chk33
			global count_job_three
			three_dir = directorya+"PC3_c/"
			if pc33 == 0:
				file_nn = os.listdir(three_dir)
				for file_name in file_nn:
					#change = file_name.split("_")
					count_job_three = count_job_three+1
					#new_name = str(count_job_three)+"_"+change[1]+"_"+change[2]
					#os.rename(os.path.join(three_dir, file_name), os.path.join(three_dir,new_name))

				pc3_chk_counter = pc3_chk_counter+1
				pc3_chk_count = fixed_chk33
				accept_worker(connection, ip, port, three_dir, count_job_three, pc3_chk_counter,pc_name,mylist)			
				pc33 = 1
			else:
				pc3_chk_counter = pc3_chk_counter+1
				pc3_chk_count = fixed_chk33
				accept_worker(connection, ip, port, three_dir,count_job_three, pc3_chk_counter,pc_name,mylist)

		elif (pc_name=="PC4_cc"):
			print ("Check to the new checkpoint_jobs directory")
			global pc44
			global pc4_chk_counter
			global fixed_chk4
			global count_job_four
			four_dir = directorya+"PC4_c/"
			if pc44 == 0:
				file_nn = os.listdir(four_dir)
				for file_name in file_nn:
					change = file_name.split("_")
					count_job_four = count_job_four+1
					new_name = str(count_job_four)+"_"+change[1]+"_"+change[2]
					os.rename(os.path.join(four_dir, file_name), os.path.join(four_dir,new_name))
				
				pc4_chk_counter = pc4_chk_counter+1
				pc4_chk_count = fixed_chk4
				accept_worker(connection, ip, port, four_dir, count_job_four, pc4_chk_counter,pc_name,mylist)
				pc44 = 1
			else:
				pc4_chk_counter = pc4_chk_counter+1
				pc4_chk_count = fixed_chk4
				accept_worker(connection, ip, port, four_dir,count_job_four, pc4_chk_counter,pc_name,mylist)
		
		else:
			print ("Thank you very much.")

		
		
	soc.close()

def accept_worker(connection, ip, port, pc0,cc0, pc0_count,pc_name,mylist):
	try:
		Thread(target=client_thread_new, args=(connection, ip, port, pc0,cc0, pc0_count,pc_name,mylist)).start()
	except:
		print ("Thread could not start.")
		traceback.print_exc()

def process_dir_creation(directorya, mylist):
	for assign in mylist:
		subprocess.call(['mkdir', directorya+assign])
		subprocess.call(['chmod', '777', '-R', directorya+assign])
		subprocess.call(['mkdir', directorya+'c_'+assign])
		subprocess.call(['chmod', '777', '-R', directorya+'c_'+assign])
		subprocess.call(['mkdir', directorya+assign+'_c'])
		subprocess.call(['chmod', '777', '-R', directorya+assign+'_c'])
		subprocess.call(['mkdir', directorya+assign+'_c_result'])
		subprocess.call(['chmod', '777', '-R', directorya+assign+'_c_result'])

def rename_job_flag_move_worker_dir(directory, mylist, my_dict, directorya):
	for assign in mylist:
		up_to = my_dict[assign]
		flag = 1
		with open('./assign12.csv') as f:
			reader = csv.reader(f)
			next(reader, None)
			for row in reader:
				if assign==row[0]:
					print (my_dict[assign], row[1])
					shutil.move(directory+row[1],directorya)
					new_name = str(flag)+'_'+row[1]
					os.rename(os.path.join(directorya, row[1]), os.path.join(directorya,new_name))
					shutil.move(directorya+new_name,directorya+row[0])
					flag =  flag+1

def generate_csv_worker_each_jobTime(directorya):
	estimate_job_name, estimate_pc1_sec, estimate_pc2_sec, estimate_pc3_sec, estimate_pc4_sec, estimate_pc5_sec, estimate_pc6_sec = '', '', '', '', '', '', ''			
	with open('./assign12.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			with open(directorya+'/estimate/master_time.csv') as rr:
				reader1 = csv.reader(rr)
				next(reader1, None)
				for row1 in reader1:
					if re.search(row1[0], row[1]):
						estimate_job_name = row[1]
						estimate_pc1_sec = row1[7]
						estimate_pc2_sec = row1[8]
						estimate_pc3_sec = row1[9]
						estimate_pc4_sec = row1[10]
						estimate_pc5_sec = row1[11]
						estimate_pc6_sec = row1[12]
						print ("Estimated job name:", estimate_job_name)
						with open(directorya+'remove_zip/jobs.csv', 'a') as csvfile1:
							fieldnames1 = ['Job Name', 'pc1_sec', 'pc2_sec', 'pc3_sec', 'pc4_sec', 'pc5_sec', 'pc6_sec']
							writerpp1 = csv.DictWriter(csvfile1, fieldnames=fieldnames1)
							writerpp1.writerow({'Job Name': estimate_job_name, 'pc1_sec': estimate_pc1_sec, 'pc2_sec': estimate_pc2_sec, 'pc3_sec': estimate_pc3_sec, 'pc4_sec': estimate_pc4_sec, 'pc5_sec': estimate_pc5_sec, 'pc6_sec': estimate_pc6_sec})

						with open(directorya+row[0]+'/pc_time.csv', 'a') as csvfile:
							fieldnames = ['Job Name', 'pc1_sec', 'pc2_sec', 'pc3_sec', 'pc4_sec', 'pc5_sec', 'pc6_sec']
							writerpp = csv.DictWriter(csvfile, fieldnames=fieldnames)
							writerpp.writerow({'Job Name': estimate_job_name, 'pc1_sec': estimate_pc1_sec, 'pc2_sec': estimate_pc2_sec, 'pc3_sec': estimate_pc3_sec, 'pc4_sec': estimate_pc4_sec, 'pc5_sec': estimate_pc5_sec, 'pc6_sec': estimate_pc6_sec})
					else:
						print ("Skip")

def generate_csv_worker_totalTime(mylist, directorya):
	global pc1_sum, pc2_sum, pc3_sum, pc4_sum, pc5_sum, pc6_sum
	pc1_sum, pc2_sum, pc3_sum, pc4_sum, pc5_sum, pc6_sum = 0 , 0, 0, 0, 0, 0
	for total in mylist:
		with open(directorya+total+'/pc_time.csv', 'rt')as f:
			comb = csv.reader(f)
			for row in comb:
				pc1_sum = pc1_sum+int(row[1])
				pc2_sum = pc2_sum+int(row[2])
				pc3_sum = pc3_sum+int(row[3])
				pc4_sum = pc4_sum+int(row[4])
				pc5_sum = pc5_sum+int(row[5])
				pc6_sum = pc6_sum+int(row[6])
			#print (pc1_sum)
			#print (pc2_sum)
			#print (pc3_sum)
			#print (pc4_sum)
			#print (pc5_sum)
			#print (pc6_sum)
			
			with open(directorya+total+'/'+total+'.csv', 'a')as csvfile:
				fields = ['Total', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6'] 
				csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
				csvwriter.writeheader()
				csvwriter.writerow({'Total': 'Total', 'PC1': pc1_sum, 'PC2': pc2_sum, 'PC3': pc3_sum, 'PC4': pc4_sum, 'PC5': pc5_sum, 'PC6': pc6_sum})
			pc1_sum, pc2_sum, pc3_sum, pc4_sum, pc5_sum, pc6_sum = 0 , 0, 0, 0, 0, 0

def generate_time_estimate_file(mylist, directorya):
	global real_ee, real_pp
	real_ee, real_pp = [], []
	for total in mylist:
		with open(directorya+total+'/'+total+'.csv', 'rt')as f:
			comb = csv.reader(f)
			header = next(comb)
			ccount = 0
			for rowa in header:
				ccount = ccount+1
				if rowa==total:
					#print (rowa)
					#print (ccount)
					real_pp.append(rowa)
					if header != None:
						for row in comb:
							real_ee.append(row[ccount-1])
							#print (row[ccount-1])
	#print (real_ee)
	#print (real_pp)
	with open('./remove_zip/real_estimate.csv', 'w') as csvfile1:
		write = csv.writer(csvfile1) 
		write.writerow(real_pp) 
		write.writerow(real_ee) 

def client_thread_new(connection, ip, port, directory, count,pc_count, pc_name, mylist, max_buffer_size = 5120):
	global chk_count
	print ("This is the check count.", chk_count)
	print ("Current count ----->", pc_count)
	print ("Maximum limit ----->", count)

	if pc_count>count:
		if chk_count==0:
			print ("There is no job remaining.")
			connection.sendall("no_job".encode("utf8"))
			connection.close()
		else:
			connection.sendall("check".encode("utf8"))
			print ("There is still checkpoint job at Master.")
			connection.close()
	else:
		connection.sendall("data".encode("utf8"))   #1st_send(no_of_projects)
		send_receive_jobs_new(connection, ip, port, directory, count, pc_count, pc_name, mylist)
		print ("Now counter is at :", pc_count)

def send_receive_jobs_new(connection, ip, port, directory, count, start_counter, pc_name, mylist):
	global measurement, chk_count, fixed_chk3
	measurement = './migrate/conduct_measurement1.csv'
	file_count = 0
	for jobs in os.listdir(directory):
		data = jobs.split("_")
		if (data[0]==str(start_counter)):
			connection.sendall(str(jobs).encode("utf8"))  #2nd_send(folder_name)
			time.sleep(5)
			s4 = start()
			subprocess.call(['python3', './sender_m.py', directory+jobs, ip])
			e4 = end()
			#global ee
			#ee = []
			#ee.append(str(e4)+'_'+pc_name)
			#print (ee)
			#text = open("./remove_zip/real_estimate.csv", "r")
			#text = ''.join([i for i in text])
			#text = text.replace(pc_name, str(e4))
			#x = open("./remove_zip/real_estimate.csv","w")  
			#x.writelines(text) 
			#x.close()
			#print ("Docker Image transferring time*********"+convert(int(e4)-int(s4))+"*****")	
			data_append_file(measurement, jobs, pc_name, e4, s4)


			foldName = connection.recv(5120).decode("utf8")#############################
			time.sleep(5)
			nn = connection.recv(5120).decode("utf8")
			time.sleep(5)
			done_percent = connection.recv(5120).decode("utf8")
			
			if(foldName==jobs):
				rer = start()
				print ("Receive from worker:"+foldName)
				os.remove(str(directory+foldName))
				dirName = directory+foldName+"/"
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
				
			else:
				print ("Receive from worker: ----->"+foldName)
				print ("Original name of unsuccessful job: ----->"+nn)
				print ("Done percentage: ----->"+done_percent)
				time.sleep(5)
				chk_count = chk_count+1
				fixed_chk3 = chk_count
				load_org_dock = directory+jobs

				final_time1 = []
				final_worker1 = []


				chk_img = foldName
				#chk_job = './'+pc_name+'_c/'
				#inter_pc = './c_'+pc_name+'/'
				print ("This is the transfer directory for load original docker Image >>> "+load_org_dock)
				print ("This is the transfer checkpoint Image >>> "+chk_img)
				###shutil.move(load_org_dock, chk_job)
				# typecast = ''
				# typecast1 = ''
				# for total in mylist:
				# 	if pc_name==total:
				# 		print ("It is not required to check the duration")
				# 		###shutil.copy('./'+total+'/pc_time.csv', chk_job)
				# 	else:
				# 		shutil.copy('./'+total+'/'+total+'.csv', chk_job)
				# 		index = re.findall('(\d+)', total)
				# 		#typecast = index
				# 		with open(chk_job+total+'.csv', 'rt') as f:
				# 			reader = csv.reader(f)
				# 			i = next(reader)
				# 			final_worker1.append(i[int(typecast1.join(index))])
						
				# 		with open(chk_job+total+'.csv', 'rt')as f:
				# 			comb = csv.reader(f)
				# 			#reader = csv.reader(f)
				# 			next(comb, None)
				# 			for row in comb:
				# 				final_time1.append(row[int(typecast.join(index))])
				#print ("----------------------------------")
				#print ("Worker compare", final_worker1)
				#print ("Time compare", final_time1)
				#print ("----------------------------------")
			# 	pca_sum = 0
			# 	pcb_sum = 0
			# 	pcc_sum = 0
			# 	pcd_sum = 0
			# 	pce_sum = 0
			# 	with open("./remove_zip/real_estimate.csv", 'rt')as f:
			# 		comb = csv.reader(f)
			# 		for row in comb:
			# 			print (row[0])
			# 			print (row[1])
			# 			print (row[2])
			# 			print (row[3])
			# 			print (row[4])
			# 			pca_sum = pca_sum+int(row[0])
			# 			pcb_sum = pcb_sum+int(row[1])
			# 			pcc_sum = pcc_sum+int(row[2])
			# 			pcd_sum = pcd_sum+int(row[3])
			# 			pce_sum = pce_sum+int(row[4])
			# 		print (pca_sum)
			# 		print (pcb_sum)
			# 		print (pcc_sum)
			# 		print (pcd_sum)
			# 		print (pce_sum)
					
			# 		with open("./remove_zip/output.csv", 'a')as csvfile:
			# 			fields = ['PC1', 'PC2', 'PC3', 'PC4', 'PC6'] 
			# 			csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
			# 			csvwriter.writeheader()
			# 			csvwriter.writerow({'PC1': pca_sum, 'PC2': pcb_sum, 'PC3': pcc_sum, 'PC4': pcd_sum, 'PC6': pce_sum})

			# 	final_worker = []
			# 	final_time = []
			# 	with open("./remove_zip/output.csv", 'rt')as f:
			# 		comb = csv.reader(f)
			# 		header = next(comb)
			# 		#ccount = 0
			# 		for rowa in header:
			# 			final_worker.append(rowa)
			# 	with open("./remove_zip/output.csv", 'rt')as f:
			# 		comb = csv.reader(f)
			# 		header = next(comb)
			# 		if header != None:
			# 			for row in comb:
			# 				final_time.append(row)
			# 	print ("Final Worker Compare", final_worker)
			# 	print ("Final Time Compare ", final_time)
			# 	smallest_duration = int(final_time[0])
			# 	smallest_index = 0
			# 	for i in range(len(final_time)):
			# 		if int(final_time[i])<smallest_duration:
			# 			smallest_duration = int(final_time[i])
			# 			smallest_index = int(i)
			# 	print ("The most efficient PC is ", final_worker[smallest_index], "and the working duration is ", convert(smallest_duration), "(", smallest_duration,")")
			# 	new_direct = './'+final_worker[smallest_index]+'_c/'
			# 	new_direct1 = './PC3_c/'
			# 	new_direct2 = './PC4_c/'
			# 	new_directa = './'+final_worker[smallest_index]+'_c_result/'
			# 	file_nn = os.listdir(inter_pc)

			# 	print ("----------------------------------")
			# 	standard = 0
			# 	with open(chk_job+'pc_time.csv', 'rt')as f:
			# 		comb = csv.reader(f)
			# 		for row in comb:
			# 			if row[0]==nn:
			# 				standard = row[int(typecast.join(re.findall('(\d+)', final_worker[smallest_index])))]
			# 			else:
			# 				print ("")
			# 	print ("The standard cpu time of checkpoint job(", nn, ")executing at current efficient worker(", final_worker[smallest_index], ")is ", convert(int(standard)), "(", standard,")")
			# 	print ("----------------------------------")
			# 	print ("Checkpoint job finishing percent before interrupt is ", done_percent, "%")
			# 	finish_percentage = int(float(float(standard)-((float(done_percent)/100)*float(standard))))
			# 	print ("The remaining time of ", nn, "if it will execute at", final_worker[smallest_index], "is ",convert(finish_percentage), "(", finish_percentage,")")
			# 	print ("----------------------------------")
			# 	print ("Suitable directory", chk_job)

			# 	os.rename(os.path.join(chk_job, jobs), os.path.join(chk_job,jobs+'_'+'c'))
			# 	file_nn = os.listdir(chk_job)
			# 	for file_name in file_nn:
			# 		name, ext = os.path.splitext(file_name)
			# 		if ext==".csv":
			# 			os.remove(chk_job+file_name)
			# 		else:
			# 			shutil.move(os.path.join(chk_job, file_name),new_directa)

			# 	dirName = directory+nn+"/"
			# 	os.makedirs(dirName)
			# 	subprocess.call(['chmod', '777', '-R', dirName])

			# 	files_count = connection.recv(5120).decode("utf8")
			# 	print ("Files count:", files_count)
			# 	time.sleep(5)

			# 	for account in range(int(files_count)):
			# 		filees_name = connection.recv(5120).decode("utf8")
			# 		time.sleep(5)
			# 		with open(dirName+filees_name, 'wb')as f:
			# 			datta = connection.recv(5120)
			# 			time.sleep(5)
			# 			if not datta:
			# 				f.close()
			# 				print ("File is closed.")
			# 			f.write(datta)
			# 		print ("Successfully get the file.")
			# 		time.sleep(5)
			# 	with open(measurement, 'a') as csvfile:
			# 		csvwriter = csv.writer(csvfile)
			# 		csvwriter.writerow(["------------------------------------"])
			# 		csvwriter.writerow(["Receive unsuccessful job - "+str(nn)+" from worker - "+str(foldName)])
			# 		csvwriter.writerow(["Number of received result file before interrupt"+str(files_count)])
			# 		csvwriter.writerow(["Check available worker ",final_worker])
			# 		csvwriter.writerow(["Calculate total cpu time of each worker ",final_time])
			# 		csvwriter.writerow(["The most efficient PC is ", final_worker[smallest_index], "and the working duration is ", convert(smallest_duration), "(", smallest_duration,")"])
			# 		csvwriter.writerow(["The standard cpu time of checkpoint job(", nn, ")executing at current efficient worker(", final_worker[smallest_index], ")is ", convert(int(standard)), "(", standard,")"])
			# 		csvwriter.writerow(["Checkpoint job finishing percent before interrupt is ", done_percent, "%"])
			# 		csvwriter.writerow(["The remaining time of ", nn, "if it will execute at", final_worker[smallest_index], "is ",convert(finish_percentage), "(", finish_percentage,")"])
			# 		csvwriter.writerow(["------------------------------------"])
	
			# back_data = connection.recv(5120).decode("utf8")
			# if "finish" in back_data:
			# 	print ("Check is there any other jobs")
			# 	time.sleep(5)
			# 	connection.close()
			# 	exit()
		else:
			print ("False")

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
if __name__=="__main__":
	main()	