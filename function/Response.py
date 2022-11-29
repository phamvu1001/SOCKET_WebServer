import config
import random

class Response:
	def __init__(self, path):

		self.file_buff = ''
		self.status = 200

		#if case below define some files to transfer normally
		self.ChunkedSend = True			#Mac dinh la gui theo cach thong thuong (ChuckedSend = Flase)
		# if path in ['/','/index.html']: #index here
		# 	path = config.get_index
		# 	self.ChunkedSend = False
		# if path == '/images.html': #images page after login
		# 	path = config.get_images
		# 	self.ChunkedSend = False
		# if path == '/css/utils.css':
		# 	path = config.get_utils
		# 	self.ChunkedSend = False
		# if path == '/401.html':
		# 	path = config.get_401					
		# if path == '/css/style.css':
		# 	path = config.get_style
		# 	self.ChunkedSend = False
		# if path in ['/avatars/1.png', '/avatars/2.png', '/avatars/3.png', '/avatars/4.png']:
		# 	path = "/web_src" + path
		# 	self.ChunkedSend = False
		# if path in ['/avatars/5.png', '/avatars/6.png', '/avatars/7.png', '/avatars/8.png']:
		# 	path = "/web_src" + path
		# 	self.ChunkedSend = False
		# if path == '/404.html': #error page
		# 	path = config.get_404
		# 	self.status = 404		# change status code
		# 	self.ChunkedSend = False
   	
		# Split path into array to get file name and file type
		self.loc_of_file = path							
		file_info = path.split('/')[-1].split('.')		
		self.file_type = file_info[-1]		# Get file type from array


		# co gang mo file da cung cap duong dan o tren, neu false tra ve status code 404 va 404.html
		try:
			if(self.file_buff == ''):
				if(self.ChunkedSend != True):
					self.buffer = open(path[1:],"rb")
				else:
					self.buffer = open(path[1:].replace("%20"," "),"rb")	# Get data buffer from file
		except:
			self.status = 404
			self.ChunkedSend = False
			self.buffer = open(config.get_404[1:],"rb")

		#make header
		header = ""	
		header += "HTTP/1.1 404 NOT FOUND\n" if(self.status == 404) else "HTTP/1.1 200 OK\n"
		if self.file_type in ["html","txt"]:
			header += 'Content-Type: text/%s\n'%self.file_type
		elif self.file_type == "css":
			header += 'Content-Type: text/%s\n'%self.file_type
		elif self.file_type in ["png","jpg","jpeg","gif"]:
				header += 'Content-Type: image/%s\n'%self.file_type
		else:
				header += 'Content-Type: application/octet-stream\r\n'
		header += 'Connection: close\r\n' 
		self.header = header
		print(f'-------------------\n[HEADER RESPONSE]\n {header}')

	def makeResponse(self):
		#Self.ChunkedSend is detect to send normal or with chunked transfer

		if self.ChunkedSend == False:
		#normal send file
			
			if(self.file_buff != ''):
				content = self.file_buff.encode('utf-8')
			else:
				content = self.buffer.read()

			self.header += "Content-Length: %d\r\n\r\n"%len(content)
			header = self.header.encode('utf-8') + content + "\r\n".encode('utf-8')
			print(f"-------------------\n [SEND RESPONSE]\n Transfer {self.loc_of_file} with normal mode")
			return header
		else:
			self.header += "Transfer-Encoding: chunked\r\n\r\n"

		#render chunk
			BUFF_SIZE = config.buffer_size
			content = "".encode('utf-8')
			L = self.buffer.read(BUFF_SIZE)
			while(len(L) == BUFF_SIZE):
				size = len(L)
				content += ("{:X}\r\n".format(size)).encode('utf-8')
				content += L 
				content += "\r\n".encode()
				L = self.buffer.read(BUFF_SIZE)
			size = len(L)
			content += ("{:X}\r\n".format(size)).encode('utf-8')
			content += L
			content += "\r\n0".encode('utf-8')
			self.chunkedcontent = content

		#send chunk
			header = self.header.encode('utf-8') + self.chunkedcontent + "\r\n\r\n".encode('utf-8')
			print(f"-------------------\n [SEND RESPONSE]\n Transfer {self.loc_of_file} with chunked transfer encoding mode")
			return header