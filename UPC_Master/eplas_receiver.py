"""
Server receiver of the file
"""
import socket
import tqdm
import os

def receive_file(file_location, port, host):
    SERVER_HOST = host
    SERVER_PORT = int(port)
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print("[*] Listening as {}:{}".format(SERVER_HOST, SERVER_PORT))
    client_socket, address = s.accept() 
    print("[+] {} is connected.".format(address))
    base_directory = './'
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), "Receiving {}".format(filename), unit="B", unit_scale=True, unit_divisor=1024)
    with open(base_directory+file_location+filename, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    client_socket.close()
    s.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("file", help="File name to send")
    parser.add_argument("port", help="Port number of the receiver")
    parser.add_argument("host", help="The host/IP address of the receiver")
    args = parser.parse_args()
    sys_name = args.file
    port_num = args.port
    ip_address = args.host
    receive_file(sys_name,port_num, ip_address)