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
    print ("[S]: Got a connection request from a client at {}".format(addr))

    data_from_client = csockid.recv(100)
    received_msg = data_from_client.decode('utf-8')
    print("[S]: Received message from client: {}".format(received_msg))
    received_msg = received_msg[::-1].swapcase()

    data_from_client = received_msg.encode('utf-8')
    
    csockid.send(data_from_client)
    print("[S]: Echoed message back to client")

    # Close the server socket
    ss.close()
    exit()