import socket


def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to jthe server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    
    opened = open("in-proj.txt","r")
    read = opened.read(-1)
    msg = read
    cs.send(msg.encode('utf-8'))
    print("[C]: Sent message to server:{} \n".format(msg))

    # Receive data from the server
    data_from_server=cs.recv(230) #Buffer increased to 230 because all file inputs will be no more than 200 bytes(characters)
    print("[C]: Data received from server: {} \n".format(data_from_server.decode('utf-8')))

    # close the client socket
    cs.close()
    #Write recieved-data to proper output file
    newout = open("out-proj.txt","w")
    newout.writelines(data_from_server.decode('utf-8'))
    newout.close()
    exit()