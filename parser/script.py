import socket
from serverthread import ServerThread


PORT = 5001
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind((socket.gethostname(), PORT))
# become a server socket
serversocket.listen(10)

while True:
	# accept connections from outside
    print('Waiting for connections')
    (clientsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    st = ServerThread(clientsocket).start()
