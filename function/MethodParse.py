import socket
import config
from function.Response import *

# Get request from client
# Lay yeu cau tu client (browsers)
def getRequest(client):
	request = ''
	client.settimeout(1)

	try:
		#nhan request tu client (browsers)
		request = client.recv(1024).decode()
		while (request):
			request += client.recv(1024).decode()
	except socket.timeout:
		# neu het thoi gian nhan request
		#if timed out
		if not request:
			print("-------------------\n [SERVER]\n No request from client")
	finally:
		# phan tich request
		return RequestParse(request)

# phan tich cu phap cua request
class RequestParse:
	def __init__(self, request):
		print(request)
		# cat den truoc noi dung cua file yeu cau trong request
		requestArray = request.split("\n")
		# print(requestArray)
		if request == "":
			self.empty = True	# truong hop request khong co noi dung
		else:
			self.empty = False
			# method o day co the la GET hoac POST
			self.method = requestArray[0].split(" ")[0]		#get method
			self.path = requestArray[0].split(" ")[1]		#get path
			self.content = requestArray[-1]					#get request content
			# Ex: requestArray[0] = 'GET /css/style.css HTTP/1.1\r'
			# => .method = GET; .path = /css/style.css; 
   			# vi requestArray duoc cat toi truoc noi dung cua file yeu cau nen .content = '' 
		
		#print(self.content)
		#print(self.path)	


#POST Method Parser
def postMethod(client, request):
	if(request.path == '/images.html' and request.content == "uname=%s&psw=%s&remember=%s"%(config.uname,config.psw,config.remember)):
		client.sendall(Response(config.get_images).makeResponse())
		return
	elif (request.path == '/images.html' and request.content == "uname=%s&psw=%s"%(config.uname,config.psw)):
		client.sendall(Response(config.get_images).makeResponse())
		return		
	else:
		client.sendall(Response(config.get_401).makeResponse())
		return


#GET method parser
def getMethod(client, request):
	#Return to homepage first time connect
	if request.path in ['/','/index.html']:
		request.path = config.get_index
	elif request.path == '/favicon.ico':
		request.path = config.get_favicon
	elif request.path == '/css/style.css':
		request.path = config.get_style
	elif request.path == '/css/utils.css':
		request.path = config.get_utils
	elif request.path == '/401.html':
		request.path = config.get_401
	elif request.path == '/images/images1.jpg':
		request.path = "/web_src/images/images1.jpg"
	elif request.path == '/images/images2.jpg':
		request.path = "/web_src/images/images2.jpg"
	elif request.path == '/images/images3.jpg':
		request.path = "/web_src/images/images3.jpg"
	elif request.path == '/images/images4.jpg':
		request.path = "/web_src/images/images4.jpg"
	elif request.path in ['/avatars/1.png', '/avatars/2.png', '/avatars/3.png', '/avatars/4.png']:
		request.path = "/web_src" + request.path
	elif request.path in ['/avatars/5.png', '/avatars/6.png', '/avatars/7.png', '/avatars/8.png']:
		request.path = "/web_src" + request.path
	else:
		request.path = config.get_404
    	

	#print(request.path)
	
	#input the file path to send to to client
	client.sendall(Response(request.path).makeResponse())
