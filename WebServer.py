import socket
import config
from function.MethodParse import *
from threading import Thread

def Method(client):
    request=getRequest(client)
    if not request.empty:
        print(f"-------------------\n [LISTENED REQUEST]\n Request catched: %s with %s has content %s\n"%(request.method, request.path, request.content))
        if request.method == "POST":
            postMethod(client, request)
        else:
            getMethod(client, request)
	
def Connections():
    while True:
        (client,address)=server.accept()
        print(f"-------------------\n [SERVER]\n {address} sent request to server.")
        Thread(target=Method,args=(client,)).start()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
server.bind(('localhost', 8080))


try:
    server.listen(5)
        #client,addr=server.accept()
    ACCEPT_THREAD=Thread(target=Connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
except:
    print("error\n")
finally:
    server.close()
 	
