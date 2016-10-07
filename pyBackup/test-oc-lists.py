from fs.contrib.davfs import DAVFS
import httplib
import ssl
import time
import hashlib
import os

class UnsecureHTTPSConnection(httplib.HTTPSConnection):
    def __init__(self, host=None, port=None, key_file=None, cert_file=None, strict=None, timeout=None, source_address=None, context=None):
        context = ssl._create_unverified_context()
        #super(httplib.HTTPSConnection, self).__init__(host, port, key_file, cert_file, strict, timeout, source_address, context)
        httplib.HTTPSConnection.__init__(self, host, port, key_file, cert_file, strict, timeout, source_address, context)
        

# http://stackoverflow.com/questions/5319430/how-do-i-have-python-httplib-accept-untrusted-certs

credentials = {
	'username':os.environ['OC_USER'],
	'password':os.environ['OC_PASS']
}
connection_classes = {
	"http":  httplib.HTTPConnection,
	"https": UnsecureHTTPSConnection,
}

dvfs = DAVFS("https://quamis.go.ro/owncloud/remote.php/webdav/", credentials=credentials, connection_classes=connection_classes )
#print dvfs.getinfo("/")
#print dvfs.listdir("/de lasat acasa/")
#print dvfs.listdir("/GoogleDrive/")


# http://docs.pyfilesystem.org/en/latest/interface.html

#dirs = dvfs.ilistdirinfo("/")
#for d in dirs:
#    print d

t1 = time.time()
files = []
for (ocd, ocf) in dvfs.walk("/de lasat acasa/"):
    for f in ocf:
        files.append("%s/%s" % (ocd, f))
t2 = time.time()

print files
print "  > took %.2fs" % (t2 - t1)

for f in files:
    #t1 = time.time()
    #l = len(dvfs.getcontents(f))
    #print "file %s has %s bytes" % (f, l)
    #t2 = time.time()
    #print "  > took %.2fs => %.3fMb/s" % (t2 - t1, l/(t2 - t1)/(1024*1024))
    
    t1 = time.time()
    hashObj = hashlib.sha1()

    fp = dvfs.open(f, mode='rb', encoding=None)
    while True:
        data = fp.read(1*1024*1024)
        if len(data)==0:
            break
                
        hashObj.update(data)
        
        fp.seek(264*1024*1024, os.SEEK_CUR)
    fp.close()    
    print hashObj.hexdigest()
    
    l = dvfs.getsize(f)
    print "file %s has %s bytes" % (f, l)
    t2 = time.time()
    print "  > took %.2fs => %.3fMb/s" % (t2 - t1, l/(t2 - t1)/(1024*1024))
    
