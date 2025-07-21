from hashlib import sha256
import pandas as pd
import qrcode as qr
import logging
import argparse
import pathlib


def generate_hash_key(am, name):
    input_str = f"{am}-{name.lower().strip()}"
    return sha256(input_str.encode('utf-8')).hexdigest()

def generate_qr_file(hash):
    
    print(f"Trying to read file: {args.source}")
    df = pd.read_excel(args.source) 
    
    for i, row in df.iterrows():
        qr_image = qr.make(hash)
        qr_image.save('qr.png')
        break


def main():
    am = 'Α/Α             ΔΕΛΤΙΟΥ'
    name = 'EΠΩΝΥΜΟ'
    hash = generate_hash_key(am, name)
    generate_qr_file(hash)
    
if __name__ == "__main__":

    log = logging.getLogger()
    log.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.set_name('stdout')
    formatter = logging.Formatter('[%(levelname)s:%(funcName)s] %(message)s')
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    args = argparse.ArgumentParser()
    args.add_argument("--source", action="store", required=True)
    args.add_argument("--ignore_names", action="store", type=pathlib.Path, default="ignore.txt")
    args = args.parse_args()
    
    main()

