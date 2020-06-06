#!/usr/bin/env python3
import socket
import threading

import pickle

class SocketHost():
    def __init__(self, pos, ball):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Get server IP
        #returns the host name of the current system running server  
        host_name = socket.gethostname()
        #returns ip address of host
        self.server_IP_address = socket.gethostbyname(host_name)
        print("Server Ipv4: " + self.server_IP_address)
        #Establish port
        self.port = 5555
        #Designates ip as server ip address via bind
        self.s.bind((self.server_IP_address, self.port))
        print("socket binded to %s" %(self.port))
        #prepares socket for accepting connectiooons
        self.s.listen(100)
        print("socket is listening")
        self.pos_other = 250
        self.pos = pos
        self.ball = ball
        #Recieve client data
        # Establish connection with client.
        self.c, addr = self.s.accept()
        print("Socket connected")


    def recv_msg(self):
        data = self.c.recv(4096)
        if data:
            self.pos_other = data.decode('utf-8')
        else:
            pass

    def send_msg(self):
        data_send = {"block":self.pos, "ball":self.ball}
        self.c.send(pickle.dumps(data_send))
    
    def set_pos(self, pos):
        self.pos = pos
