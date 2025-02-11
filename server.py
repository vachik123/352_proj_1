import socket
import threading 
import time 
import random

from client import client


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

    data_from_client = csockid.recv(230) #buffer increased because largest file input is no more than 200 bytes(characters)
    received_msg = data_from_client.decode('utf-8')
    print("[S]: Received message from client: {} \n".format(received_msg))

    reversed_lines = "\n".join(received_msg.splitlines()[::-1]) #added to keep file lines in the correct order(before swapping)
    received_msg = reversed_lines[::-1].swapcase()

    data_from_client = received_msg.encode('utf-8')
    
    csockid.send(data_from_client)
    print("[S]: Echoed message back to client")

    # Close the server socket
    ss.close()
    exit()
    
if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()

    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)
    print("Done.")