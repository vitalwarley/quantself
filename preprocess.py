import os
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Setup Google Drive API
def auth_drive():
    gauth = GoogleAuth()
    creds = 'creds.txt'
    if os.path.exists(creds):
        print(f'Loading credentials from file {creds}...')
        gauth.LoadCredentialsFile(creds)
    else:
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        gauth.SaveCredentialsFile(creds)
    return drive


def get_files(drive, folder_id):
    try:
        files = drive.ListFile({'q': f"'{folder_id}' in parents"}).GetList()
    except NameError:
        print("Couldn't access Google Drive.")
        return []

    return files

def get_health_data(drive):
    data_dir = 'data/health'
    os.makedirs(data_dir, exist_ok=True)

    folder_id = '152iBBZjg9YZSvvuxtMHg5AvrptqGe18k'
    files = get_files(drive, folder_id)

    for file in files:
        # TODO: get latest fat secret and strongapp exports
        f = drive.CreateFile({'id': file['id']})
        fname = 'fs' if file['title'][:2] == 'fs' else 'strong'
        f.GetContentFile(os.path.join(data_dir, fname + '.csv'))

if __name__ == '__main__':
    drive = auth_drive()
    get_health_data(drive)
