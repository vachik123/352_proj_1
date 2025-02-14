import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    # handle initial handshake
    handshake = csockid.recv(9)  # "READY_CHK"
    if handshake.decode('utf-8') == "READY_CHK":
        csockid.send(b"READY_ACK")
        print("[S]: Sent ready acknowledgment to client")
    
    # first receive the file size
    size_data = csockid.recv(10)  # size won't be more than 10 digits
    file_size = int(size_data.decode('utf-8'))
    print("[S]: Expected file size:", file_size)
    
    # send acknowledgment
    csockid.send(b"SIZE_ACK")
    
    # now receive the actual data with proper buffer size
    data_from_client = csockid.recv(file_size)
    received_msg = data_from_client.decode('utf-8')
    print("[S]: Received message from client: {} \n".format(received_msg))

    reversed_lines = "\n".join(received_msg.splitlines()[::-1])
    received_msg = reversed_lines[::-1].swapcase()

    data_from_client = received_msg.encode('utf-8')

    # write to output file before sending
    with open("out-proj.txt", "w") as outfile:
        outfile.write(received_msg)
    print("[S]: Output contents:")
    print(received_msg)
    
    # # # send size of response first
    # response_size = len(data_from_client)
    # csockid.send(str(response_size).encode('utf-8'))
    
    # # # wait for client acknowledgment
    # csockid.recv(8)  # "SIZE_ACK"
    
    # # send actual response
    # csockid.send(data_from_client)
    # print("[S]: Echoed message back to client")
    
    csockid.close()

if __name__ == "__main__":
    server()