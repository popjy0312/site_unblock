#-*- coding: utf-8 -*-

import socket
import thread
import logging as log
import sys

log.basicConfig(filename='./error.log',level=log.ERROR)
#log.basicConfig(filename='./debug.log',level=log.DEBUG)

HOST = '127.0.0.1'
PORT = 8080

dummy = 'GET / HTTP/1.1\r\nHost: test.gilgil.net\r\n\r\n'

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

MAXBUF = 16000

def getHostName(data):
	hostIndex = data.find("Host: ")
	return data[hostIndex:].split('\r\n')[0][len("Host: "):]

def parsePort(data):
	#CONNECT client-lb.dropbox.com:443 HTTP/1.1
	tmp = data.split()[1]
	return int(tmp[tmp.find(':')+1:])



def handler(s, addr):
	data = s.recv(MAXBUF)
	#log.debug("####################################")
	#log.debug("HTTP connection")
	log.debug(data)
	#log.debug("####################################")
	#log.debug(getHostName(data))
	if not data:
		return


	new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	outport = 80
	try:
		new_sock.connect( (getHostName(data), outport) )
	except Exception as e:
		log.error(e)
		log.error("getHostName data error")
		#log.error(getHostName(data))
		log.error("\n############################################\n")
		log.error("data is\n")
		log.error(data)
		log.error("\n############################################\n")
		new.sock.close()
		return
	#log.debug("connect ok")
	new_sock.send(dummy + data)
	while True:
		recv = new_sock.recv(MAXBUF)
		if not recv:
			break
		if recv.count("HTTP/1.1 ") > 1:
			recv = recv[1 + recv[1:].find("HTTP/1.1 "):]
		log.debug(recv)
		try:
			s.send(recv)
		except Exception as e:
			log.error(e)
			log.error("s.send(recv) error")
			log.error("\n############################################\n")
			log.error("data was\n")
			log.error(data)
			log.error("\n############################################\n")
			log.error("recv is\n")
			log.error(recv)
			log.error("\n############################################\n")
			break

	new_sock.close()


if __name__ == '__main__':
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind( (HOST, PORT) )
		s.listen(5)

		while True:
			c, addr = s.accept()
			print "connect" + str(addr)
			thread.start_new_thread(handler, (c, addr))
	except Exception as e:
		log.error(e)
	finally:
		s.close()