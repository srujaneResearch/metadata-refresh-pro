client_sec="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"
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
code = gauth.GetAuthUrl()
print(code)

u_code = input("Emter Code\n")
gauth.Auth(u_code)

print(os.getcwd())
gauth.SaveCredentialsFile('kevin.json')



#gauth.CommandLineAuth()
