#!/usr/bin/env python3
import socket
import threading

import pickle

class SocketClient():
    def __init__(self, pos_left, pos_right, ip):
        self.s = socket.socket() 
        self.s.connect((ip, 5555))
        side = pickle.loads(self.s.recv(4096))
        if side == 'L':
            self.left = True
        else:
            self.left = False
        self.pos_left = pos_left
        self.pos_right = pos_right
        self.ball_x = 250
        self.ball_y = 250
        threading.Thread(target=self.recv_msg).start()       
        threading.Thread(target=self.send_msg).start()

    def recv_msg(self):
        while 1:
            data = self.s.recv(4096)
            if data and len(data)>20:
                try:
                    data = pickle.loads(data)
                    if int(data[1]) < 500:
                        try:
                            self.pos_left = int(data[0])
                            self.pos_right = int(data[1])
                            self.ball_x = int(data[2])
                            self.ball_y = int(data[3])
                        except ValueError:
                            pass
                except:
                    pass
            else:
                pass

    def send_msg(self):
        while 1:
            msg = [self.pos_left, self.pos_right, self.ball_x, self.ball_y]
            msg = pickle.dumps(msg)
            self.s.send(msg)