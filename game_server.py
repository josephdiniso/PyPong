#!/usr/bin/env python3

import socket
import pickle
import threading
import sys
import os

class Socket():
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
        while len(self.clients)<2:
            c, addr = self.s.accept()
            print("CONNECTed")
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

    
    def recv_msg(self, c, addr):
        while(1):
            data = c.recv(4096)
            if data:
                try:
                    data = pickle.loads(data)
                    if self.clients.index(c) == 1:
                        self.pos_right = int(data[1])
                    else:
                        self.pos_left = int(data[0])
                        self.ball_x = int(data[2])
                        self.ball_y = int(data[3])
                except:
                    pass
            else:
                pass


    def send_msg(self):
        while 1:
            msg = [self.pos_left, self.pos_right, self.ball_x, self.ball_y]
            msg = pickle.dumps(msg)
            for client in self.clients:
                client.send(msg)
    
    
    # def remove(self, connection):
    #     if connection in self.clients: remove(self.clients)


def main():
    server = Socket()
if __name__ == "__main__":
    main()