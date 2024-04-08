import hashlib
import argparse
from pathlib import Path
from datetime import datetime

"""
Duplicates V1.7
"""

def get_file_hash(file_path):

    """
    Generate a hash for a file's contents to efficiently check for duplicates.
    Read the file and hash it in 4096-byte parts to mitigate potential memory issues.
    """
    
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for part in iter(lambda: f.read(4096), b""):
            hash_md5.update(part)
    return hash_md5.hexdigest()

def find_duplicates(start_directory):
    
    """
    Find and return a dictionary of duplicate files grouped by their content hash.
    Use of Pathlib instead of os.walk to prevent large file names.
    Except because some really large path + file names caused OS errors.
    """
    
    hashes = {}
    duplicates = {}

    for file_path in Path(start_directory).rglob('*'):
         try:
             if file_path.is_file():
                 file_hash = get_file_hash(str(file_path))
                 if file_hash in hashes:
                     if file_hash in duplicates:
                         duplicates[file_hash].append(str(file_path))
                     else:
                         duplicates[file_hash] = [hashes[file_hash], str(file_path)]
                 else:
                     hashes[file_hash] = str(file_path)
         except OSError as e:
             print(f"Error processing file {file_path}: {e}")

    return duplicates

def main(start_directory):
    duplicates = find_duplicates(start_directory)

    if duplicates:
        print("Duplicate files found, writing results to file.")
        
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M")
        filename = f"{timestamp}_Duplicates.txt"
        
        with open(filename, 'w') as f:
            f.write("Duplicate files found:\n")
            for file_hash, paths in duplicates.items():
                f.write(f"Hash: {file_hash} has {len(paths)} duplicates:\n")
                for path in paths:
                    f.write(f"\t{path}\n")
        print(f"Results written to file: {filename}")
    else:
        print("No duplicate files found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--directory',help='Path for duplicates research')
    args = parser.parse_args()
    
    if args.directory:
        main(args.directory)
