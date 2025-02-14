import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # send handshake and wait for acknowledgment
    cs.send(b"READY_CHK")
    ack = cs.recv(9)  # "READY_ACK"
    if ack.decode('utf-8') != "READY_ACK":
        print("[C]: Server not ready")
        cs.close()
        exit()
    print("[C]: Server ready, proceeding with file transfer")

    # read the file and get its size
    with open("in-proj.txt", "r") as opened:
        msg = opened.read()
    
    # send file size first
    file_size = len(msg.encode('utf-8'))
    cs.send(str(file_size).encode('utf-8'))
    
    # wait for server acknowledgment
    cs.recv(8)  # "SIZE_ACK"
    
    # send actual data
    cs.send(msg.encode('utf-8'))
    print("[C]: Sent message to server:{} \n".format(msg))

    # # first receive size of response
    # size_data = cs.recv(10)  # Size won't be more than 10 digits
    # response_size = int(size_data.decode('utf-8'))
    
    # # send acknowledgment
    # cs.send(b"SIZE_ACK")
    
    # # receive data from the server with proper buffer size
    # data_from_server = cs.recv(response_size)
    # print("[C]: Data received from server: {} \n".format(data_from_server.decode('utf-8')))

    cs.close()
    
    # # write received data to proper output file
    # with open("out-proj.txt", "w") as newout:
    #     newout.write(data_from_server.decode('utf-8'))
    
    exit()

if __name__ == "__main__":
    client()