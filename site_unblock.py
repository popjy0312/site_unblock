from scapy.all import *
import socket
import thread
import logging as log

#log.basicConfig(level=log.DEBUG)

HOST = '127.0.0.1'
PORT = 8080

dummy = 'GET / HTTP/1.1\r\nHost: test.gilgil.net\r\n\r\n'

MAXBUF = 4096

def getHostName(data):
	tmp = data.split('\r\n')
	return tmp[1][tmp[1].find("Host: ")+6:]

def forward(data):
	new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handler(s, addr):
	data = s.recv(MAXBUF)
	log.debug("####################################")
	log.debug("HTTP connection")
	log.debug(data)
	log.debug("####################################")
	#log.debug(getHostName(data))

	new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	log.debug("new sock connect to " + getHostName(data))
	log.debug(getHostName(data))
	new_sock.connect( (getHostName(data), 80) )
	log.debug("connect ok")
	new_sock.send(dummy + data)

	while True:
		recv = new_sock.recv(MAXBUF)
		if not recv:
			break
		if recv.count("HTTP/1.1 ") > 1:
			recv = recv[1 + recv[1:].find("HTTP/1.1 "):]
		print "recv ok"
		print recv
		s.send(recv)

	new_sock.close()
	s.close()


if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind( (HOST, PORT) )
	s.listen(5)

	while True:
		c, addr = s.accept()
		log.debug("connect" + str(addr))
		thread.start_new_thread(handler, (c, addr))
