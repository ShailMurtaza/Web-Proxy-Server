#  import socket, ssl

#  HOST = "www.google.com"
#  PORT = 443

#  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
#  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  s_sock = context.wrap_socket(s, server_hostname=HOST)
#  s_sock.connect((HOST, PORT))
#  s_sock.send("GET / HTTP/1.1\r\nHost:www.google.com\r\nUser-Agent: python-requests/2.26.0\r\n\r\n".encode())

#  DATA = b''
#  PACKET = "NULL"
#  while PACKET:
    #  PACKET = s_sock.recv(1024*1024*10) # 10 MB
    #  DATA += PACKET
    #  print(PACKET)

#  open("test.html", "wb").write(DATA)
#  s_sock.close()

