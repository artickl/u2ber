#!/usr/bin/python3

# pip3 install --upgrade pydrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import argparse
import os.path

#arguments setup
parser = argparse.ArgumentParser()
parser.add_argument('--user_id',default='123',help="Telegram User ID for keeping files in separate folder")
parser.add_argument('--file',default='youtube-dl test video \'\'_ä↭𝕐-BaW_jenozKc.mp3',help="Output file to upload to Google Drive")
parser.add_argument('--root',default='1H87w9gaG_g-RnXo8TiGKp-KJIkcki73E',help="Root folder where other folders will be placed")
args = parser.parse_args()

if not os.path.exists('client_secrets.json'):
    print('[W] Please follow to https://console.cloud.google.com/apis/credentials to download client_secrets.json for "OAuth 2.0 Client IDs"')
    quit()

#google drive auth with saving locally
#TODO: not sure if this will work remotely or we will need to place the settings.yaml + clients_secrets.json + creds.json
gauth = GoogleAuth()    

#gauth.CommandLineAuth()
# service account from local file
##gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)

#checking if folder for the user already exist and getting id for it
folder_list = drive.ListFile({'q': "'"+args.root+"' in parents and trashed=false"}).GetList()
for folder in folder_list:
    print('Folder: %s, ID: %s' % (folder['title'], folder['id']))
    if(folder['title'] == args.user_id):
        folder_id = folder['id']
        file_list = drive.ListFile({'q': "'"+folder_id+"' in parents and trashed=false"}).GetList()
        for file in file_list:
            print('File: %s, ID: %s' % (file['title'], file['id']))
            if(file['title'] == args.file):
                print('File already has been uploaded before')
                print('Folder id: %s\nFile id: %s' % (folder_id, file['id']))
                quit()
        break

#creating a new folder if no folder has been found
if (folder_id == ""):
    folder = drive.CreateFile({'title' : args.user_id, 'mimeType' : 'application/vnd.google-apps.folder', 'parents': [{'id': '1H87w9gaG_g-RnXo8TiGKp-KJIkcki73E'}]})
    folder.Upload()
    folder_id=folder['id']

#uploading file to selected folder
gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
gfile.SetContentFile(args.file)
gfile.Upload()

#printing out folder and file ids
print('Folder id: %s\nFile id: %s' % (folder_id, gfile['id']))
