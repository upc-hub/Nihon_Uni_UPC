import os
import shutil
import subprocess
import filetype
import json

global S1, S2, S3, S4, S5, S6
S1 = "BasicAppX1\n"
S2 = "BasicAppX2\n"
S3 = "ColorGameX\n"
S4 = "SoccerMatch\n"
S5 = "AnimalTour\n"
S6 = "MyLibrary\n"

def aplas_job_zipping(APLAS_dir, all_job_dir, com_job_dir):
	chk_aplas_jobs = []
	global token_counter_today
	APLAS_umount = './aplas_umount/'
	
	check_types_job(APLAS_dir)
	
	for aplas_umount in os.listdir(APLAS_dir):
		shutil.move(APLAS_dir+aplas_umount, APLAS_umount)
		chk_aplas_jobs.append(aplas_umount)
	print ("Current jobs list", chk_aplas_jobs)
	print ("******************************************")

	for file_name in chk_aplas_jobs:
		separate_ext = file_name.split('.')
		file = separate_ext[0]
		extension = separate_ext[1]
		if not os.path.exists(APLAS_umount+file):
			subprocess.call(['mkdir', APLAS_umount+file])
			subprocess.call(['chmod', '777', '-R', APLAS_umount+file])
	
	for file_name1 in chk_aplas_jobs:
		separate_ext1 = file_name1.split('.')
		file1 = separate_ext1[0]
		extension1 = separate_ext1[1]
		for file_name2 in chk_aplas_jobs:
			separate_ext2 = file_name2.split('.')
			file2 = separate_ext2[0]
			extension2 = separate_ext2[1]
			if file1 == file2:
				if extension1 !=extension2:
					try:
						subprocess.call(['mv', APLAS_umount+file_name1, APLAS_umount+file1])
						subprocess.call(['mv', APLAS_umount+file_name2, APLAS_umount+file1])
						shutil.make_archive(APLAS_umount+file1, 'zip', APLAS_umount+file1)
						subprocess.call(['rm', '-r', APLAS_umount+file1])
						subprocess.call(['chmod', '777', '-R', APLAS_umount+file1+'.zip'])
						subprocess.call(['mv', APLAS_umount+file1+'.zip', all_job_dir])
					except OSError as e:
						print ("<<<There is no problem for this above statement>>>")

def check_types_job(APLAS_dir):
	typea_count = 0
	typeb_count = 0
	typec_count = 0
	typed_count = 0
	typee_count = 0
	typef_count = 0
	global S1, S2, S3, S4, S5, S6
	jobs_type = []
	extract = ""
	for jobs in os.listdir(APLAS_dir):
	  extract_job = jobs.split('.')
	  if extract_job[1]=="manifest":
	    manifest = open(APLAS_dir+jobs, 'rb')
	    for line in manifest:
	      line = line.decode('UTF-8')
	      extract = line
	      split_extract = extract.split('=')
	      if split_extract[0]=='PROJECT' and split_extract[1]==S1:
	        typea_count+=1
	      elif split_extract[0]=='PROJECT' and split_extract[1]==S2:
	        typeb_count+=1
	      elif split_extract[0]=='PROJECT' and split_extract[1]==S3:
	        typec_count+=1
	      elif split_extract[0]=='PROJECT' and split_extract[1]==S4:
	        typed_count+=1
	      elif split_extract[0]=='PROJECT' and split_extract[1]==S5:
	        typee_count+=1
	      elif split_extract[0]=='PROJECT' and split_extract[1]==S6:
	        typef_count+=1

	print ("******************************************")
	print ("Types of APLAS jobs 	>>>", "No. of jobs")
	print ("	BasixAppX1	>>>	", typea_count)
	print ("	BasixAppX2	>>>	", typeb_count)
	print ("	ColorGameX	>>>	", typec_count)
	print ("	SoccerMatch	>>>	", typed_count)
	print ("	AnimalTour	>>>	", typee_count)
	print ("	MyLibrary	>>>	", typef_count)
	print ("******************************************")
	#subprocess.call(['python3', './call_sam_scheduling.py', str(typea_count), str(typeb_count), str(typec_count), str(typed_count), str(typee_count), str(typef_count)])

def aplas_job_preparation(common_queue, detect_systemb, sys_name, base_directory, detect_systema, container_queue, job_dir):
	print (detect_systemb[2]+'-'+detect_systema[1]+" is the APLAS job. It doesn't need to check Metadata.")
	global S1, S2, S3, S4, S5, S6
	subprocess.call(['scp', '-r', common_queue+sys_name, base_directory+str(detect_systemb[2]).upper()+'/jobStatus/waiting/'])          #after necessary checking, jobs are moved to the waiting queue of correspondance system. It can be seen on Web interface.
	#print (job_dir+'/'+detect_systemb[2]+'-'+detect_systema[1]+'.manifest')
	value = extract_aplas_manifest(job_dir+'/'+detect_systemb[2]+'-'+detect_systema[1]+'.manifest')
	job_data = './data.json'
	if value==S1:
		type_job = 'S1'
		aplas_job_type_preprocess(common_queue, detect_systemb, type_job, job_dir, container_queue, detect_systema, job_data)
	elif value==S2:
		type_job = 'S2'
		aplas_job_type_preprocess(common_queue, detect_systemb, type_job, job_dir, container_queue, detect_systema, job_data)
	elif value==S3:
		type_job = 'S3'
		aplas_job_type_preprocess(common_queue, detect_systemb, type_job, job_dir, container_queue, detect_systema, job_data)
	elif value==S4:
		type_job = 'S4'
		aplas_job_type_preprocess(common_queue, detect_systemb, type_job, job_dir, container_queue, detect_systema, job_data)
	elif value==S5:
		type_job = 'S5'
		aplas_job_type_preprocess(common_queue, detect_systemb, type_job, job_dir, container_queue, detect_systema, job_data)
	else:
		type_job = 'S6'
		aplas_job_type_preprocess(common_queue, detect_systemb, type_job, job_dir, container_queue, detect_systema, job_data)

def aplas_job_type_preprocess(common_queue, detect_systemb, type_job, job_dir, container_queue, detect_systema, job_data):
	#print (type_job)
	shutil.make_archive(common_queue+detect_systemb[0]+'_'+detect_systemb[1]+'_'+type_job+'_'+detect_systemb[2]+'-'+detect_systema[1], 'zip', job_dir)
	subprocess.call(['rm', '-r', job_dir])
	shutil.move(common_queue+detect_systemb[0]+'_'+detect_systemb[1]+'_'+type_job+'_'+detect_systemb[2]+'-'+detect_systema[1]+'.zip', container_queue)                              #All checked jobs are reached to the container queue and then, moved to the correspondance worker queue
	subprocess.call(['chmod', '777', '-R', container_queue])
	current_job = container_queue+detect_systemb[0]+'_'+detect_systemb[1]+'_'+type_job+'_'+detect_systemb[2]+'-'+detect_systema[1]+'.zip'
	assign_correspondance_job(type_job, job_data, current_job)

def assign_correspondance_job(job_type, job_data, current_job):
	pc_dir = './' 
	if job_type=="S1":
		worker_num = 0
		assign_correspondance_worker(current_job, job_data, job_type, worker_num, pc_dir)
		
	elif job_type=="S2":
		worker_num = 1
		assign_correspondance_worker(current_job, job_data, job_type, worker_num, pc_dir)

	elif job_type=="S3":
		worker_num = 2
		assign_correspondance_worker(current_job, job_data, job_type, worker_num, pc_dir)

	elif job_type=="S4":
		worker_num = 3
		assign_correspondance_worker(current_job, job_data, job_type, worker_num, pc_dir)

	elif job_type=="S5":
		worker_num = 4
		assign_correspondance_worker(current_job, job_data, job_type, worker_num, pc_dir)

	else:
		worker_num = 5
		assign_correspondance_worker(current_job, job_data, job_type, worker_num, pc_dir)

def assign_correspondance_worker(current_job, job_data, job_type, worker_num, pc_dir):
	ff = open(job_data, 'r')
	data = json.loads(ff.read())
	pc6_S_jobs_amount = data['data'][worker_num]['result_details'][0]['job_amount']
	pc6_S_current_no = check_no_jobs_type_PC(job_type, "PC66")

	pc5_S_jobs_amount = data['data'][worker_num]['result_details'][1]['job_amount']
	pc5_S_current_no = check_no_jobs_type_PC(job_type, "PC55")

	pc4_S_jobs_amount = data['data'][worker_num]['result_details'][2]['job_amount']
	pc4_S_current_no = check_no_jobs_type_PC(job_type, "PC44")

	pc3_S_jobs_amount = data['data'][worker_num]['result_details'][3]['job_amount']
	pc3_S_current_no = check_no_jobs_type_PC(job_type, "PC33")

	pc2_S_jobs_amount = data['data'][worker_num]['result_details'][4]['job_amount']
	pc2_S_current_no = check_no_jobs_type_PC(job_type, "PC22")

	pc1_S_jobs_amount = data['data'][worker_num]['result_details'][5]['job_amount']
	pc1_S_current_no = check_no_jobs_type_PC(job_type, "PC11")

	if int(pc6_S_current_no)<=int(pc6_S_jobs_amount):
		shutil.move(current_job, pc_dir+"PC66")
	elif int(pc5_S_current_no)<=int(pc5_S_jobs_amount):
		shutil.move(current_job, pc_dir+"PC55")
	elif int(pc4_S_current_no)<=int(pc4_S_jobs_amount):
		shutil.move(current_job, pc_dir+"PC44")
	elif int(pc3_S_current_no)<=int(pc3_S_jobs_amount):
		shutil.move(current_job, pc_dir+"PC33")
	elif int(pc2_S_current_no)<=int(pc2_S_jobs_amount):
		shutil.move(current_job, pc_dir+"PC22")
	else:
		shutil.move(current_job, pc_dir+"PC11")


def check_no_jobs_type_PC(job_type, PC):
	container_queue = './'
	path_name = ""
	count = 0
	#print (job_type, PC)
	for path in os.listdir(container_queue+PC+"/"):
		path_name = path
		check_type = path_name.split('.')
		check_typea = check_type[0].split('_')
		#print (path_name)
		if os.path.isfile(os.path.join(container_queue+PC+"/", path)) and check_typea[2]==job_type:
			count += 1
	return count

def extract_aplas_manifest(file1):
	manifest = open(file1, 'rb')
	S1 = "BasicAppX1\n"
	S2 = "BasicAppX2\n"
	for line in manifest:
		line = line.decode('UTF-8')
		extract = line
		split_extract = extract.split('=')
		if split_extract[0]=='PROJECT':
			if split_extract[1]==S1:
				f = open(file1, 'r')
				list_of_lines = f.readlines()
				list_of_lines[2] = "PROJECT=BasicAppX\n"
				g = open(file1, 'w')
				g.writelines(list_of_lines)
				g.close()
				return split_extract[1]
			elif split_extract[1]==S2:
				f = open(file1, 'r')
				list_of_lines = f.readlines()
				list_of_lines[2] = "PROJECT=BasicAppX\n"
				g = open(file1, 'w')
				g.writelines(list_of_lines)
				g.close()
				return split_extract[1]
			else:
				return split_extract[1]