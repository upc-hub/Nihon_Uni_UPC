# Nihon_Uni_UPC (multiple NS-Simulator jobs run a worker at the same time )
#  Usage explanation(使用説明),
### 1. Things to do at Server PC (サーバーPCでできること)
```
1. Download the updated project from GitHub.
   (更新されたプロジェクトを GitHub からダウンロードします。)

2. Open the master_operation_nssimulation.py under UPC_Master directory
   (UPC_Master ディレクトリの下にある master_operation_nssimulation.py を開きます。)

3. Then, edit the number of thread usage in each worker pc (e.g. pc6_limitt=1 to pc6_limitt=6), and save it. 
   (次に、各ワーカー pc のスレッド使用数を編集 (例: pc6_limitt=1 から pc6_limitt=6) し、保存します。)

4. Go to the UPC_Master directory, run the upc_master_v1.py, and choose '7' for processing NS-Simulation job
   (UPC_Master ディレクトリに移動し、upc_master_v1.py を実行し、NS-Simulation ジョブを処理するために「7」を選択します。)

5. For submitting the jobs, go to the jobs directory and there are two sample jobs.
   (ジョブを送信するには、ジョブ ディレクトリに移動します。2 つのサンプル ジョブがあります。)
   Inside the job zip file, there is only input data file (e.g gunji_olsr-randam.cc)
   (ジョブ zip ファイル内には、入力データ ファイル (例: gunji_olsr-randam.cc) のみがあります。)
   
6. Multiple jobs can be created by changing the parameters inside that file and they can be processed in a worker at the same time.
   (そのファイル内のパラメーターを変更することで複数のジョブを作成し、ワーカーで同時に処理することができます。)
```

### 2. Things to do at Client PCs (クライアント PC で行うこと)
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
