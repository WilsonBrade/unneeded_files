#!python3

import os
import sys 
from pathlib import Path
from send2trash import send2trash




def get_path(base_path) -> list[Path]: 
    base_path = Path(base_path)

    if not base_path.is_dir() : 
        print("It is not a valid path for directory")
        sys.exit(1)

    elem = [f for f in base_path.iterdir()]

    return elem

def check_oversized(file_path : Path) -> bool:
    size = os.path.getsize(file_path)
    limit = 100 *(2**20) 

    if size > limit : 
        return True
     
    return False


def list_files_in_path(path : Path) -> list[Path] : 
    paths = []
    if path.is_dir() : 
        for root, subfolders, files in os.walk(path) : 
            for file in files:
                paths.append(Path(os.path.join(root, file)))

        return paths
    
    paths.append(Path(path))
    return paths


def delete(file_path : Path) -> None:
    try :  
        send2trash(file_path)
    except Exception as e : 
        print(f"Error : {e}")



def main() : 

    if len(sys.argv) < 2 : 
        print("Usage : python unneeded_files [path]")
        sys.exit(1)
    

    base_path = sys.argv[1]

    elem = get_path(base_path)

    try : 
        for e in elem : 

            for path in list_files_in_path(e) : 
                if check_oversized(path) : 
                    delete(path)

    except Exception as e : 
        print(f"Error: {e}")







