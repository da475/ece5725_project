import bluetooth
import RPi.GPIO as gp

###### CLIENT - RPi0 ###########

RECV_SIZE = 1024

ack_recvd = 0

# setup port number and address
server_port = 71

# restart the server
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# create a client socket and connect to the server
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect(("B8:27:EB:7E:2A:D0", 3))
client_socket.send("Horrible Ani")
print "Horrible Ani finished"


"""
# start loop to receive msgs from server
while True:
    msg_buffer = client_socket.recv(RECV_SIZE)
    print ('C: recvd msg: {}'.format(msg_buffer))
    if msg_buffer == '':
        break

    if ack_recvd == 0 and msg_buffer == 'ACK':
        print ('ACK received fromt the server')
        ack_recvd = 1
    else:
        client_socket.send(count)
        time.sleep(0.2)
        count = count+1
        
    
    #time.sleep(0.5)
"""

# close the sockets
client_socket.close()
gp.cleanup()



