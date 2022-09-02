# Nihon_Uni_UPC (multiple NS-Simulator jobs run a worker at the same time )
#  (Usage explanation),
### 1. Things to do at Server PC
```
1. Download the updated project from GitHub.

2. Open the master_operation_nssimulation.py under UPC_Master directory

3. Then, edit the number of thread usage in each worker pc (e.g. pc6_limitt=1 to pc6_limitt=6), and save it. 

4. Go to the UPC_Master directory, run the upc_master_v1.py, and choose '7' for processing NS-Simulation job

5. For submitting the jobs, go to the jobs directory and there are two sample jobs.
   Inside the job zip file, there is only input data file (e.g gunji_olsr-randam.cc)
   
6. Multiple jobs can be created by changing the parameters inside that file and they can be processed in a worker at the same time.

### 3. Things to do at Server PC (サーバーPCでできること)
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
   $docker pull pollen5005/upc_web_server:latest

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
### 4. Things to do at Client PCs (クライアント PC で行うこと)
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
## UPC System Overview (UPC制度の概要)
- user-PC Computing System (UPC) is a computing platform for executing complex computation project using idel resources of user-PCs at laboratory.
(ユーザー PC コンピューティング システム (UPC) は、実験室でユーザー PC のアイドル リソースを使用して複雑な計算タスクを実行するためのコンピューティング プラットフォームです。)
- Docker is used to run any computational project (job) to various computing platform (worker PCs).
(Docker は、さまざまなコンピューティング プラットフォーム (ワーカー PC) に対して任意の計算プロジェクト (ジョブ) を実行するために使用されます。)
![interface](https://user-images.githubusercontent.com/79504426/183276945-c8a0a311-fccd-4b89-8da3-b49f89b8b4dd.png)
## UPC System setup at Nihon Uni. (日本大学でのUPCシステムのセットアップ)
- seven PCs can be used for setting up UPC system and one for the server and six PCs for worker PCs.
(UPC システムのセットアップ用に 7 台の PC、サーバー用に 1 台、ワーカー PC 用に 6 台の PC を使用できます。)
![Nihon_Uni](https://user-images.githubusercontent.com/79504426/183277677-7c7d4165-55f7-4340-bc5f-b22cdef56827.png)
