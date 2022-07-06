import socket
import ssl

class Request():
	def __init__(self, url):
		parsed_url = self.parse_url(url)
		if not parsed_url:
			return "INVALID URL"
		host, port, path, secure = parsed_url
		host = host.replace("?", "")

		web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if secure:
			context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
			self.web_conn = context.wrap_socket(web_sock, server_hostname=host)
		else:
			self.web_conn = web_sock
		self.secure = secure
		self.port = port
		self.request = f'GET /{path} HTTP/1.1\r\n'
		self.request_headers = {
			'User-Agent': 'python-requests/2.26.0',
			'Accept': '*/*',
			'Connection': 'keep-alive'
		}
		self.request_headers['Host'] = host

	def send(self):
		self.web_conn.connect((self.request_headers['Host'], self.port))
		raw_headers = (self.request + self.raw_headers(self.request_headers)).encode()
		self.web_conn.send(raw_headers)
		response = b''
		PACKET = "NULL"
		while PACKET and (not response.endswith(b"\r\n\r\n")):
			PACKET = self.web_conn.recv(1024*1024*10) # 10 MB
			response += PACKET
			# print(PACKET)
			# input()
		# print("COMPLETED RECEIVING ......................................................")
		self.web_conn.close()
		response = response.split(b"\r\n\r\n", 1)
		response[0] = self.process_headers(response[0])
		# if not header:
		# 	self.data = self.data[self.data.find(b'\r\n\r\n') + 4:]
		return response


	def raw_headers(self, headers):
		raw_request_headers = ''
		for head in headers:
			raw_request_headers += f'{head}: {headers[head]}\r\n'
		raw_request_headers += "\r\n"
		return raw_request_headers

	# Function to convert raw headrs to dictionary
	def process_headers(self, headers):
		headers = headers.decode()
		headers = headers.split("\r\n")
		self.response = headers[0]
		headers.pop(0)
		dict_headers = {}
		for head in headers:
			one_head = head.split(": ")
			dict_headers[one_head[0]] = one_head[1]
		return dict_headers

	def parse_url(self, url):
		if url.startswith("http:"):
			port = 80
			secure = ""
		elif url.startswith("https:"):
			port = 443
			secure = "s"
		else:
			return
		to_find = f"http{secure}://"
		position = url.find(to_find) + len(to_find)
		url = url[position:]
		url = url.split("/", 1)
		host = url[0]
		if len(url) == 1:
			path = ""
		else:
			path = url[1]
		if ":" in host:
			host, port = host.split(":")
			port = int(port)
		if secure:
			secure = True
		else:
			secure = False
		return (host, port, path, secure)


if __name__ == "__main__":
	r = Request("http://127.0.0.1/main.js")
	print(r.send()[1])
	