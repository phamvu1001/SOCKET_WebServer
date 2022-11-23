import socket
import config
from function.MethodParse import *


try:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.bind((config.HOST, config.PORT))
	server.listen(5)

	print("-------------------\n [SERVER]\n Listening on: http://%s:%d"%(config.HOST,config.PORT))

	while True:

		#Server things
		(client, address) = server.accept()

		print(f"-------------------\n [SERVER]\n {address} sent request to server.")

		#Get request
		request = getRequest(client)

		if not request.empty: 
			print(f"-------------------\n [LISTENED REQUEST]\n Request catched: %s with %s has content %s\n"%(request.method, request.path, request.content))
			if request.method == "POST":
				postMethod(client, request)
			else:
				getMethod(client, request)

		client.shutdown(socket.SHUT_RD)
		print("\n--------[Request done]--------\n\n")
except:
    print('Error')

client.close()
 	
