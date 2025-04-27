import socket
import argparse
import os
import datetime
from io import BytesIO
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from zipfile import ZipFile

listen_IP = None
listen_port = None
encrypted_data = None

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("target", type=str)
    parser.add_argument("port", type=int)

    args = parser.parse_args()

    global listen_IP, listen_port

    listen_IP = args.target
    listen_port = args.port

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    global listen_IP, listen_port, encrypted_data
    server_address = (listen_IP, listen_port)
    sock.bind(server_address)

    sock.listen(1)

    print(f"Server listening on ip {listen_IP} and port {listen_port}")

    while True:
        client_sock, _ = sock.accept()

        data = []
        while True:
            chunk = client_sock.recv(4096)
            if not chunk:
                break
            data.append(chunk)

        encrypted_data = b"".join(data)
        client_sock.close()

        extract_data()

def extract_data():
    load_dotenv()

    key = os.getenv("KEY")
    fernet = Fernet(key)

    decrypted_archive = BytesIO(fernet.decrypt(encrypted_data))

    with ZipFile(decrypted_archive, "r") as file:
        dest_file = str(datetime.datetime.now()) + listen_IP
        file.extractall(dest_file)

def main():
    parse_args()

    if listen_IP == None or listen_port == None:
        return

    if listen_port < 0 or listen_port > 65535:
        return
    
    listen()

if __name__ == "__main__":
    main()