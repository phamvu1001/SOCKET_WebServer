import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080

uname = "admin"
psw = "123456"
remember = "on"

buffer_size = 1024*50#50kb  size per chunk 

get_favicon = "/web_src/favicon.ico"
get_index = "/web_src/index.html"
get_404 = "/web_src/404.html"
get_401 = "/web_src/401.html"
get_images = "/web_src/images.html"
get_images1 = "/web_src/images/images1.jpg"
get_images2 = "/web_src/images/images2.jpg"
get_images3 = "/web_src/images/images3.jpg"
get_images4 = "/web_src/images/images4.jpg"
get_style = "/web_src/css/style.css"
get_utils = "/web_src/css/utils.css"

