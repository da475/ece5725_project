import bluetooth
import RPi.GPIO as gp

pin_bt = 13
gp.setmode(gp.BCM)
gp.setup(pin_bt, gp.OUT)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

RECV_SIZE = 1024

# setup port number and address
server_port = 71
server_addr = ""

# restart the server
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# create welcoming socket and listen to 1 client
server_socket.bind((server_addr, server_port))
server_socket.listen(1)

# look for the client connection
client_socket, client_address = server_socket.accept()
print ('recevied connection from ', client_address)

# send the ack
client_socket.send('ACK')

# start loop to receive msgs until client closes
while True:
    msg_buffer = client_socket.recv(RECV_SIZE)
    if msg_buffer == '':
        break

    print ('recvd the msg ', msg_buffer)
    client_socket.send('ACK_MSG')

# close the sockets
client_socket.close()
server_socket()
gp.cleanup()
