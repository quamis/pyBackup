from fs.contrib.davfs import DAVFS
import httplib
import ssl

class UnsecureHTTPSConnection(httplib.HTTPSConnection):
    def __init__(self, host=None, port=None, key_file=None, cert_file=None, strict=None, timeout=None, source_address=None, context=None):
        context = ssl._create_unverified_context()
        #super(httplib.HTTPSConnection, self).__init__(host, port, key_file, cert_file, strict, timeout, source_address, context)
        httplib.HTTPSConnection.__init__(self, host, port, key_file, cert_file, strict, timeout, source_address, context)
        

# http://stackoverflow.com/questions/5319430/how-do-i-have-python-httplib-accept-untrusted-certs

credentials = {
	'username':'lucian.sirbu', 
	'password':'dAthAqu3Umu'
}
connection_classes = {
	"http":  httplib.HTTPConnection,
	"https": UnsecureHTTPSConnection,
}

dvfs = DAVFS("https://quamis.go.ro/owncloud/remote.php/webdav/", credentials=credentials, connection_classes=connection_classes )
print dvfs.getinfo("/")
print dvfs.listdir("/de lasat acasa/")
print dvfs.listdir("/GoogleDrive/")


# http://docs.pyfilesystem.org/en/latest/interface.html
