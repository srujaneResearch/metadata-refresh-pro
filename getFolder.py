from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

gauth.LoadCredentialsFile('kevin.json')

if gauth.access_token_expired:
    print("Expire, Refreshing token")

    # Refresh them if expired

    gauth.Refresh()
else:
    print("good")
    gauth.Authorize()


drive = GoogleDrive(gauth)

# Auto-iterate through all files in the root folder.
file_list = drive.ListFile({'q': "'1-JtstcTGro6S0S9zQqBqqKayUoTdNB0N' in parents and trashed=false"}).GetList()

id = 'https://drive.google.com/uc?id=1nmF_A9ZD9Mr4cvc6bmWZeAbKO6NTVjQp'

file = drive.CreateFile({'id':'1nmF_A9ZD9Mr4cvc6bmWZeAbKO6NTVjQp'})

file.GetContentFile('tele.mp4')




l = drive.CreateFile({'title':'test.mp4'})
l.SetContentFile('file_52.MP4')

l


folder = drive.CreateFile({'title':'MetadataRefreshPro','mimeType':'application/vnd.google-apps.folder'})
folder.Upload()

id = folder['id']
print(id)


"""

nfile = drive.CreateFile({'parents':[{'id':id}],'title':'joy.mp3'})

nfile.SetContentFile('joy.mp3')
nfile.Upload()

nfile.InsertPermission({'type':'anyone',
                        'value':'anyone',
                        'role':'reader'
                        })

"""
"""
file1 = drive.CreateFile({'title': 'HelloFromPython.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Hello World!') # Set content of the file from given string.
file1.Upload()
"""    # Initialize the saved creds
