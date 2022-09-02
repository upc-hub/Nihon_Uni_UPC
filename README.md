# Nihon_Uni_UPC
#  (UPCシステムをインストールするには),
### 1. Prerequisite (前提条件)
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
### 2. generate ns 3 simulator docker image (ns 3 シミュレーター docker イメージを生成する)
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
