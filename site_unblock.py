import socket
import thread

HOST = '127.0.0.1'
PORT = 5959

dummy = 'GET / HTTP/1.1\r\nHost: test.gilgil.net\r\n\r\n'

def handler(s, addr):
	while True:
		print s.recv(1024)

	s.close()


if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind( (HOST, PORT) )
	s.listen(5)

	while True:
		c, addr = s.accept()
		print "connect" + str(addr)
		thread.start_new_thread(handler, (c, addr))
