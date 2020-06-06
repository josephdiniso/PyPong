#!/usr/bin/env python3
import socket
import threading

import pickle

class SocketClient():
    def __init__(self, pos):
        self.s = socket.socket() 
        self.s.connect(('192.168.86.32', 5555))
        self.pos = pos
        self.pos_other = 250
        self.ball = (250,250)

    def recv_msg(self):
        data = self.s.recv(4096)
        if data:
            data = pickle.loads(data)
            self.pos_other = data["block"]
            self.ball = data["ball"]
        else:
            pass

    
    def send_msg(self):
        self.s.send(str(self.pos).encode('utf-8')) 
