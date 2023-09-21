# -*- coding: utf8 -*-
import cv2
import socket
import numpy as np
from Object_detect.Socket_Server.constants import *
import pickle

class UDP_connector():
    def __init__(self, info):
        self.info = info
        self.IP = info.get_IP()
        self.PORT = info.get_tcp_PORT()

    def client_sock(self, status):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        status[0] = True
        return

    def send(self, frame):
        flatten_frame = frame.flatten()
        string_frame = flatten_frame.tostring()

        for i in range(20):
            self.sock.sendto(bytes([i]) + string_frame[i*46080:(i+1)*46080],
                             (self.IP, self.PORT))
        return
    
    def recive(self):
        data, _ = self.sock.recvfrom(46081)
        result = pickle.loads(data)

        boxes = result[0]
        scores = result[1]
        classes = result[2]
        width = result[3]
        height = result[4]
        return boxes, scores, classes, width, height
