import config
import random

class Response:
	def __init__(self, path):

		self.file_buff = ''
		self.status = 200

		self.ChunkedSend = True			
   	
		# get file name and file type
		self.loc_of_file = path		# duong dan toi file					
		file_info = path.split('/')[-1].split('.')		
		self.file_type = file_info[-1]		# file type


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

		# khoi tao header
		header = ""	
		header += "HTTP/1.1 404 NOT FOUND\n" if(self.status == 404) else "HTTP/1.1 200 OK\n"
		if self.file_type in ["html","htm"]:
			header += 'Content-Type: text/%s\n'%self.file_type
		elif self.file_type == "txt":
			header += 'Content-Type: text/plain\r\n'
		elif self.file_type == "css":
			header += 'Content-Type: text/%s\n'%self.file_type
		elif self.file_type == "jpg":
			header += 'Content-Type: image/jpeg\r\n'
		elif self.file_type in ["png","jpeg","gif"]:
				header += 'Content-Type: image/%s\n'%self.file_type
		else:
				header += 'Content-Type: application/octet-stream\r\n'
		header += 'Connection: close\r\n' 
		self.header = header
		print(f'-------------------\n [HEADER RESPONSE] \n {header}')

	def makeResponse(self):
		# truong hop file duoc gui theo cach thong thuong
		if self.ChunkedSend == False:
		#normal send file
			
			if(self.file_buff != ''):
				content = self.file_buff.encode('utf-8')
			else:
				content = self.buffer.read()

			self.header += "Content-Length: %d\r\n\r\n"%len(content)
			header = self.header.encode('utf-8') + content + "\r\n".encode('utf-8')
			print(f"-------------------\n [SEND RESPONSE] \n Transfer {self.loc_of_file} with normal mode")
			return header
		# truong hop file duoc gui theo kieu chunked
		else:
			self.header += "Transfer-Encoding: chunked\r\n\r\n"

		#render chunk
			# moi chuck co do lon la 50kb
			BUFF_SIZE = config.buffer_size
			# ma hoa noi dung voi fomat la 'utf-8'
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
			self.chunked_content = content

		#send chunk
			header = self.header.encode('utf-8') + self.chunked_content + "\r\n\r\n".encode('utf-8')
			print(f"-------------------\n [SEND RESPONSE] \n Transfer {self.loc_of_file} with chunked transfer encoding mode")
			return header