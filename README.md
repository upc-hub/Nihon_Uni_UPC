# Nihon_Uni_UPC
# To setup UPC system (UPCシステムをインストールするには),
### Prerequisite (前提条件)
```
1. install Docker on all PCs 
   (すべての PC に Docker をインストールする)
   -https://docs.docker.com/engine/install/ubuntu/  
   (参考のため)

2. install Python3 and pip on all PCs 
   (すべての PC に Python3 と pip をインストールする)
   $sudo apt-get update
   $sudo apt install python3-pip

3. install sshfs on server PC 
   (サーバー PC に sshfs をインストールする)
   $sudo apt install sshfs
   -https://www.digitalocean.com/community/tutorials/how-to-use-sshfs-to-mount-remote-file-systems-over-ssh   
   (参考のため)

4. download Nihon_Uni_UPC repository from github to server PC
   (Nihon_Uni_UPC リポジトリを github からサーバー PC にダウンロードします。)
   $git clone https://github.com/upc-hub/Nihon_Uni_UPC

5. go to the downloaded directory 
   (ダウンロードしたディレクトリに移動します)
   $ls -al (UPC_Client フォルダーを見つける)
   - copy UPC_Client folder to the all the PCs that will be used as client nodes 
   (UPC_Client フォルダーを、クライアント ノードとして使用されるすべての PC にコピーします)
```
### generate ns 3 simulator docker image (ns 3 シミュレーター docker イメージを生成する)
```
1. go to ns-3 docker directory under Nihon_Uni_UPC
   (Nihon_Uni_UPC の下の ns-3 docker ディレクトリに移動します)

2. run the following command to build the docker image.
   (次のコマンドを実行して、docker イメージをビルドします)
   $docker build -t pollen5005/nssimulationa:latest .

3. save the built docker image
   (ビルドした Docker イメージを保存する)
   $docker save -o ./nssimulationa pollen5005/nssimulationa:latest
   
   -This nssimulationa will become a job in UPC system to execute at client PCs.
   - この nssimulationa は、クライアント PC で実行する UPC システムのジョブになります。
   
*(I will explain how to prepare Dockerfile for building image.
Then, you can modify it for future usage.)
*(イメージをビルドするための Dockerfile の準備方法を説明します。
その後、将来の使用のために変更できます。)
```
### Things to do at Server PC (サーバーPCでできること)
```
1. go to the Nihon_Uni_UPC directory
   (Nihon_Uni_UPC ディレクトリに移動します)

2. find master_worker_infor.json, open, and edit
   (master_worker_infor.json を見つけて開き、編集します)
   - server and clients's IP address can be changed based on your environment
   - (サーバーとクライアントの IP アドレスは、環境に基づいて変更できます)
   *I already changed same environment at Nihon University
   *(は日本大学で同じ環境をすでに変えました)
   
3. download the upc web server docker image
   (upc Web サーバーの Docker イメージをダウンロードします)
   $docker pull upc_web_server:latest

4. run the web_master_connection.sh
   (web_master_connection.sh を実行します)
   $./web_master_connection.sh
   -web server will run at port 3000.
   -(Web サーバーはポート 3000 で実行されます)
   -open the browser and type the following.
   -(ブラウザを開き、次のように入力します)
   >https://192.168.0.140:3000

5. run the master program
   (マスタープログラムを実行する)
   $python3 ./UPC_Master/master.py
   
6. go to jobs docker directory under Nihon_Uni_UPC
   (Nihon_Uni_UPC の下の jobs ディレクトリに移動します)
   
7. see the schedule.csv file and modify for job assignment to client PCs
   (schedule.csv ファイルを参照し、クライアント PC へのジョブ割り当て用に変更します)

8. open the web interface https://192.168.0.140:3000 and upload the jobs to the web server 
   (Web インターフェイス https://192.168.0.140:3000 を開き、ジョブを Web サーバーにアップロードします)
   
9. job status can be seen through web interface
   (ジョブのステータスは Web インターフェイスから確認できます)

10. download the results, when it is recevied from client PCs.
    (クライアント PC から受信した結果をダウンロードします。)
```
### Things to do at Client PCs (クライアント PC で行うこと)
```
1. go to the UPC_Client directory
   (UPC_Client ディレクトリに移動します)

2. find master_worker_info_client.json
   (master_worker_info_client.json を見つける)
   -give server PC's IP address and client PC's IP address
   -(サーバーPCのIPアドレスとクライアントPCのIPアドレスを与える)

3. run the worker program
   (ワーカー プログラムを実行する)
   $python3 ./upc_client_v1.py
```
## UPC Web Server
![Picture11](https://user-images.githubusercontent.com/79504426/118064692-76a79700-b3d6-11eb-996c-3e35e58490c1.png)
- UPC web server is located under the local area network.
- User in the same network can access UPC Web interface directly through the web browser for submitting the jobs.
- For the EPLAS that doesn't have the public ip address for it's own server. In this case, they can submit the jobs by adding to the pCLoud.
- For the APLAS that has own public ip address for the server, it allows SSH connection for the UPC. UPC grabs the job from APLAS server using SSHFS protocol.
- According to the above figure, all necessary directories are needed to create at Web Server storage due to synchronize with the UPC Master.
## UPC Master
![Picture12](https://user-images.githubusercontent.com/79504426/118064888-e6b61d00-b3d6-11eb-92e9-4cbcd7bc621a.png)
- Every 3o seconds, UPC Master checks the jobs from the Web Server. If there is job, it is moved to the temporary queue. Jobs in the temporary queue are renamed and put in the common queue.
- Jobs in the common queue are extracted and read the Metadata of each job to differentiate docker image is needed to build or not. 
- After doing the necessary things on the jobs, they are waiting in the container queue until the workers are not joined 
- If the workers are already in the available worker list, jobs are assigned to the correspondance worker queue.
## UPC Worker
![Picture13](https://user-images.githubusercontent.com/79504426/118064996-1cf39c80-b3d7-11eb-9d55-ba5e11fb3fd9.png)
- user PC that joins to our UPC system, it only needs to setup the Docker client.
- Workers join the master and update the available worker list in the Master and check the jobs.
- Every five seconds, workers check new jobs are arrived or not.
### Brief explanation of User-PC Computing System(UPC) Study
1. We develop a platform named UPC.
2. Web Server is built upon Ubuntu16.04. Web server programs are built using JavaScript, HTML, and CSS.
3. UPC Master is also built upon Ubuntu16.04. UPC master program is built using Python.
4. UPC Workers can be Linux or Windows OS. UPC worker program is built using Python.
5. We study static and dynamic scheduling for the UPC system.
6. Scheduling algorithms are designed by Java.
7. We investigate the job migration when one user PC cannnot keep executing our UPC jobs.
8. Podman and CRIU(Checkpoin and Restore in Userspace) are adopted to implement the job migration function.
