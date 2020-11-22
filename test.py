# -*- coding:utf-8 -*-
#webカメラの映像から顔を探し白の枠線をつけて保存するプログラム

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


# class Button(Serial):
#     def __init__(self, pid):
#         super().__init__(port=self._find_port_names(pid=pid)[0], baudrate=9600)
#         # print(self.readline())
#         # print(self.readline())
#         # self.thread_end = False
#         # self._thread = Thread(target=self.check_button)
#         # self._thread.daemon = True
#         # self._thread.start()
#         # self.num_command_queue = 0
#         # self.qtkey=qtkey
#         # self.thread=thread
#         # self.layer=None
#
#     def check_button(self):
#         print("SS")
#         while True:
#             # if self.thread_end:
#             #     break
#             # ret, frame = capture.read()
#             # windowsize = (800, 600)
#             # frame = cv2.resize(frame, windowsize)
#             # cv2.imshow('title', frame)
#
#             # if cv2.waitKey(1) & 0xFF == ord("q"):
#             line = str(self.readline())
#             result = re.findall("switched", line)
#             print(line)
#             print(result)
#             if len(result)!=0: # first readline
#                 yield 0
#                 # cv2.destroyAllWindows()
#                 signal = str(self.readline())  # second readline
#                 # print(signal)
#                 which_switch = re.findall(r'[0-9]', signal)
#                 print(which_switch[0])
#                 # assert len(which_switch)!=0, "button no mutch"
#                 if which_switch[0] == "1":
#                     print("green!")
#                     self.take_photo("green")
#                     # capture.release()
#                     # cv2.destroyAllWindows()
#                     # capture = cv2.VideoCapture(2)
#                     yield 0
#                 elif which_switch[0] == "3":
#                     print("red!")
#                     self.take_photo("red")
#                     # capture.release()
#                     # cv2.destroyAllWindows()
#                     # capture = cv2.VideoCapture(2)
#                     yield 0
#                 elif which_switch[0] == "4":
#                     print("brack!")
#                     self.take_photo("brack")
#                     # capture.release()
#                     # cv2.destroyAllWindows()
#                     # capture = cv2.VideoCapture(2)
#                     yield 0
#                 else:
#                     # capture.release()
#                     # cv2.destroyAllWindows()
#                     # capture = cv2.VideoCapture(2)
#                     yield 0
#                     pass
#             time.sleep(0.01)
#
#     def start_on_click(self):
#         if self.thread.isRunning():
#             self.qtkey.signal.emit(KeyCode.START)
#         else:
#             while True:
#                 self.write(b"toggle-mode/n")
#                 line_mode = str(self.readline())  # first readline
#                 result_mode = re.findall("toggle-mode", line_mode)
#                 if len(result_mode) != 0:
#                     break
#             signal_mode = str(self.readline())  # second readline
#             which_switch_mode = re.findall(r'[0-9]', signal_mode)
#             assert len(which_switch_mode) != 0, "mode-no-mutch"
#             if which_switch_mode[0] == "1":
#                 self.thread.mode = Mode.MAIN
#             elif which_switch_mode[0] == "2":
#                 self.thread.mode = Mode.CALIBRATION_REALSENSE
#             elif which_switch_mode[0] == "3":
#                 self.thread.mode = Mode.CALIBRATION_WEBCAM
#             else:
#                 pass
#
#             while True:
#                 self.write(b"toggle/n")
#                 line_layer = str(self.readline())  # first readline
#                 print(line_layer)
#                 result_layer = re.findall("toggle!", line_layer)
#                 if len(result_layer) != 0:
#                     break
#             signal_layer = str(self.readline())  # second readline
#             print(signal_layer)
#             which_switch_layer = re.findall(r'[0-9]', signal_layer)
#             assert len(which_switch_layer) != 0, "layer-no-mutch"
#             if which_switch_layer[0] == "1":
#                 self.thread.layer = Layer.TOP
#                 print("TOP!")
#             elif which_switch_layer[0] == "0":
#                 self.thread.layer = Layer.BOTTOM
#                 print("BOTTOM!")
#             else:
#                 pass
#             self.thread.mode = Mode.CALIBRATION_REALSENSE
#             self.thread.start()
#
#     def stop_on_click(self):
#         self.qtkey.signal.emit(KeyCode.STOP)
#
#     def emergency_on_click(self):
#         self.qtkey.signal.emit(KeyCode.EMERGENCY)
#
#     def quit_on_click(self):
#         os._exit(0)
#
#     def thread_close(self):
#         self.thread_end = True
#         self._thread.join()
#
#     def readlines(self, num: int):
#         lines = []
#         for _ in range(num):
#             lines.append(self.wait_until_read())
#         return lines
#
#     def _find_port_names(self, pid):
#         ports = list_ports.comports()
#         found_port_names = []
#         for port in ports:
#             if port.pid == pid:
#                 found_port_names.append(port.device)
#         # print(found_port_names)
#         return found_port_names
#
#     def wait_until_read(self, message=None):
#         mes = b""
#         while mes == b"":
#             mes = self.readline()
#         mes = mes.decode('utf-8')
#         print(mes)
#         assert message == None or message == mes
#         return mes
#
#     def take_photo(self, color):
        # stop(Video())
        # import datetime
        # dt_now = datetime.datetime.now()
        #
        # dir_path = "data/" + color + "/"
        # basename = "camera_capture"
        #
        # cap = cv2.VideoCapture(2)
        # if not cap.isOpened():
        #     return
        #
        # # os.makedirs(dir_path, exist_ok=True)
        # # base_path = os.path.join(dir_path, basename)
        #
        # ret, frame = cap.read()
        # # cv2.imshow("frame", frame)
        # cv2.imwrite(
        #     dir_path + "{}.png".format(dt_now.strftime('%Y-%m-%d_%H-%M-%S')), frame)

# class Video(threading.Thread):
#     def run(self):
#         cap = cv2.VideoCapture(2)
#         # key=cv2.waitKey(1)
#
#         while (cap.isOpened()):
#             # cap = cv2.VideoCapture(2)
#             ret, frame = cap.read()
#             # cv2.imshow("camera capture", frame)
#
#             windowsize = (800, 600)
#             frame = cv2.resize(frame, windowsize)
#
#             key = cv2.waitKey(1)
#
#             cv2.imshow("camera capture", frame)
#             # if key!=-1:
#             #     break
#         capture.release()
#         cv2.destroyAllWindows()


class Button(Serial):
    def __init__(self, pid):
        super().__init__(port=self._find_port_names(pid=pid)[0], baudrate=9600)

    def _find_port_names(self, pid):
        ports = list_ports.comports()
        found_port_names = []
        for port in ports:
            if port.pid == pid:
                found_port_names.append(port.device)
        print(found_port_names)
        return found_port_names

    def check_state(self):
        line = str(self.readline())
        result = re.findall("switched", line)
        print(line)
        print(result)
        if len(result)!=0: # first readline
            # cv2.destroyAllWindows()
            signal = str(self.readline())  # second readline
            # print(signal)
            which_switch = re.findall(r'[0-9]', signal)
            print(which_switch[0])
            # assert len(which_switch)!=0, "button no mutch"
            if which_switch[0] == "1":
                print("green!")
                # self.take_photo("green")
                # capture.release()
                # cv2.destroyAllWindows()
                # capture = cv2.VideoCapture(2)
                return "green"
            elif which_switch[0] == "3":
                print("red!")
                # self.take_photo("red")
                # capture.release()
                # cv2.destroyAllWindows()
                # capture = cv2.VideoCapture(2)
                return "red"
            elif which_switch[0] == "4":
                print("black!")
                # self.take_photo("brack")
                # capture.release()
                # cv2.destroyAllWindows()
                # capture = cv2.VideoCapture(2)
                return "black"
            else:
                # capture.release()
                # cv2.destroyAllWindows()
                # capture = cv2.VideoCapture(2)
                return None


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
                cv2.imshow("title", frame)

            if self.shot_image is not None:
                cv2.imwrite(f"./{self.shot_image}.jpg", frame)
                self.shot_image = None

    def start(self):
        self.thread_monitoring_button_state = threading.Thread(target=self.monitoring_button_state)
        self.thread_streaming = threading.Thread(target=self.streaming)

        self.thread_monitoring_button_state.start()
        self.thread_streaming.start()

    def stop(self):
        self.finish_flag = True
        self.thread_monitoring_button_state.join()
        self.thread_streaming.join()







if __name__ == "__main__":
    pid = 29987
    camera_id = 0

    # button = Button(pid)
    # camera = Camera(camera_id)
    camerashot = CameraShot(pid, camera_id)
    camerashot.start()
    camerashot.stop()
