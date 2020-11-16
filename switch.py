import cv2
import threading
from datetime import datetime
from typing import List
import os
from threading import Thread
import time
from serial import Serial
from serial.tools import list_ports
from util import Frame, wait_until, wait, KeyCode, Mode, Layer
import cv2
import re

class Button(Serial):
    def  __init__(self, pid):
    super().__init__(port=self._find_port_names(pid=pid)[0], baudrate=9600)

    def _find_port_names(self, pid):
        ports = list_ports.comports()
        found_port_names = []
        for port in ports:
            if port.pid == pid:
                found_port_names.append(port.device)
        print(found_port_names)
        return found_port_names
    
    def

class Camera:
    def __init__(self, camera_id):
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)

class CameraShot:
    def __init__(self, pid, camera_id):
        self.button = Button(pid)
        self.camera = Camera(camera_id)
        self.shot_image = None
        self.finish_flag = False
        self.thread_monitoring_button_state = None
        self.thread_streaming = None
    
    def monitoring_button_state(self):
        while not self.finish_flag:
            self.shot_image = self.button.check_state()

    def streaming(self):
        while not self.finish_flag:
            _, frame = self.camera.cap.read()
            if frame is not None:
                cv2.imshow('title', frame)
            
            if self.shot_image is not None:
                cv2.imwrite()