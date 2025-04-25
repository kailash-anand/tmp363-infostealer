import argparse
from scan_files import scan_device, set_ip_and_port
from cryptography.fernet import Fernet

server_IP = None
server_port = None

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("target", type=str)
    parser.add_argument("port", type=int)

    args = parser.parse_args()

    global server_IP, server_port

    server_IP = args.target
    server_port = args.port

def main():
    global server_IP, server_port

    parse_args()
    
    if server_IP == None or server_port == None:
        return 
    
    if server_port < 0 or server_port > 65535:
        return   
    
    set_ip_and_port(server_IP, server_port)
    scan_device()

if __name__ == "__main__":
    main()