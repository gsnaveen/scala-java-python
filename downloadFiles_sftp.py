import pysftp
import re
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
fileDate = "20180826"
with pysftp.Connection('download.myweb.com', username='myusername', password='mypassword', cnopts=cnopts) as sftp:
    with sftp.cd('mastersurge'):             # temporarily chdir to public
        for filename in sftp.listdir():
            if re.search("data_"+ fileDate +".*\.csv\.gz", filename):
                print(filename)
                sftp.get(filename, "./data/"+ filename, preserve_mtime=True)
                
try:
    call(["gunzip", "*" + fileDate + "*"]) 
except:
    print("Error while Unzipping")
