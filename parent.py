#!/usr/bin/env python3
import socket
import threading

import pickle

class Parent():
    def __init__(self):
        self.clients = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.s.settimeout(20)    
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host_name = socket.gethostname()
        self.server_IP_address = socket.gethostbyname(host_name)
        print("Server Ipv4: " + self.server_IP_address)
        self.port = 5555
        self.s.bind((self.server_IP_address, self.port))
        print("socket binded to %s" %(self.port))
        self.s.listen(100)
        self.pos_left = 250
        self.pos_right = 250
        self.ball_x = 250
        self.ball_y = 250
        print("socket is listening")
        first = True
        while True:
            c, addr = self.s.accept()
            c.setblocking(1)
            if c not in self.clients:
                self.clients.append(c)
                if first:
                    c.send(pickle.dumps('L'))
                    first = False
                else:
                    c.send(pickle.dumps('R'))
                threading.Thread(target=self.recv_msg, args=(c,addr)).start()
                threading.Thread(target=self.send_msg).start()


def main():
    parent = Parent()

if __name__ == "__main__":
    main()