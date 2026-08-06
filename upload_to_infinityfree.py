# -*- coding: utf-8 -*-
"""
upload_to_infinityfree.py
FTP Deployment script with directory navigation & connection pool auto-reconnect logic.
Uploads backend/, webpage/, and intel/ to InfinityFree web server.
"""

import os
import sys
import ftplib
import time

FTP_HOST = "ftpupload.net"
FTP_USER = "if0_41366642"
FTP_PASS = "ySp2t8afpDyv"
LOCAL_ROOT = os.path.dirname(os.path.abspath(__file__))

def ensure_remote_dir(ftp, remote_dir):
    dirs = remote_dir.strip('/').split('/')
    current = ""
    for d in dirs:
        if not d:
            continue
        current += "/" + d
        try:
            ftp.cwd(current)
        except Exception:
            try:
                ftp.mkd(current)
                ftp.cwd(current)
            except Exception:
                pass

def safe_upload_file(get_ftp_func, local_path, remote_path, max_retries=5):
    filename = os.path.basename(remote_path)
    remote_dir = os.path.dirname(remote_path)
    for attempt in range(max_retries):
        try:
            ftp = get_ftp_func()
            ensure_remote_dir(ftp, remote_dir)
            print(f"Uploading: {remote_dir}/{filename}")
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {filename}", f)
            return True
        except (ftplib.error_proto, ftplib.error_perm, EOFError, TimeoutError, OSError) as e:
            print(f"FTP Error ({e}) on {remote_path}, retrying attempt {attempt+1}/{max_retries}...")
            time.sleep(2)
            get_ftp_func(reconnect=True)
    print(f"FAILED to upload {remote_path} after {max_retries} retries.")
    return False

def upload_directory(get_ftp_func, local_dir, remote_dir):
    for root, dirs, files in os.walk(local_dir):
        rel_path = os.path.relpath(root, local_dir)
        if rel_path == ".":
            target_remote_dir = remote_dir
        else:
            target_remote_dir = (remote_dir + "/" + rel_path).replace("\\", "/")

        for f_name in files:
            if f_name.endswith(('.pyc', '.git', '.db')):
                continue
            local_file = os.path.join(root, f_name)
            if os.path.getsize(local_file) > 9 * 1024 * 1024:
                print(f"Skipping large binary file: {f_name}")
                continue
            remote_file = (target_remote_dir + "/" + f_name).replace("\\", "/")
            safe_upload_file(get_ftp_func, local_file, remote_file)

def main():
    print("Connecting to InfinityFree FTP server...")
    ftp_conn = [None]

    def get_ftp(reconnect=False):
        if reconnect or ftp_conn[0] is None:
            try:
                if ftp_conn[0]:
                    try:
                        ftp_conn[0].quit()
                    except Exception:
                        pass
            except Exception:
                pass
            print("Connecting to FTP...")
            f = ftplib.FTP(FTP_HOST)
            f.login(FTP_USER, FTP_PASS)
            ftp_conn[0] = f
        return ftp_conn[0]

    get_ftp()
    print("FTP Login successful!")

    # 1. Upload webpage/ application
    webpage_local = os.path.join(LOCAL_ROOT, "webpage")
    if os.path.exists(webpage_local):
        upload_directory(get_ftp, webpage_local, "shunyakikhoj.co.in/htdocs/webpage")

    # 2. Upload intel/ reasoning engine
    intel_local = os.path.join(LOCAL_ROOT, "intel")
    if os.path.exists(intel_local):
        upload_directory(get_ftp, intel_local, "shunyakikhoj.co.in/htdocs/intel")

    if ftp_conn[0]:
        try:
            ftp_conn[0].quit()
        except Exception:
            pass
    print("SUCCESS: All files successfully uploaded to InfinityFree server!")

if __name__ == "__main__":
    main()
