from typing import List
import os
from threading import Thread
import time
from serial import Serial
from serial.tools import list_ports
from util import Frame, wait_until, wait, KeyCode, Mode,Layer
import cv2
import re
import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path



class Button(Serial):
    def __init__(self, pid):
        super().__init__(port=self._find_port_names(
            pid=pid)[0], baudrate=9600, timeout=0)
    
    def check_button(self):
        print("SS")
        while True:
            line = str(self.readline())
            result = re.findall("switched", line)
            # print(line)
            # print(result)
            if len(result)!=0: # first readline
                signal = str(self.readline()) # second readline
                # print(signal)
                which_switch = re.findall(r'[0-9]',signal)
                print(which_switch[0])
                # assert len(which_switch)!=0, "button no mutch"
                if which_switch[0]== "1":
                    print("green!")
                    return "green"
                elif which_switch[0]== "3":
                    print("red!")
                    return "red"
                elif which_switch[0]== "4":
                    print("black!")
                    return "black"
                else:
                    return 
            time.sleep(0.01)

    def _find_port_names(self, pid):
        ports = list_ports.comports()
        found_port_names = []
        for port in ports:
            if port.pid == pid:
                found_port_names.append(port.device)
        # print(found_port_names)
        return found_port_names

class Camera:
    def __init__(self, camera_id):
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)

class CameraShot:
    def __init__(self, pid, camera_id):
        self.button = Button(pid=pid)
        self.camera = Camera(camera_id=camera_id)
        self.shot_image = None
        self.finish_flag = False
        self.thread_monitoring_button_state = None
        self.thread_streaming = None
        self.tpe = ThreadPoolExecutor(max_workers=2)

        # self.dir_path = Path(__file__).resolve().parent / "data" / self.shot_image
    
    def monitoring_button_state(self):
        while not self.finish_flag:
            if not self.shot_image:
                self.shot_image = self.button.check_button()
                print(f"image = {self.shot_image}")
                cv2.waitKey(1000)
    
    def streaming(self):
        while not self.finish_flag:
            # print('bb')
            _, frame = self.camera.cap.read()
            if frame is not None:
                cv2.imshow("title", frame)
                cv2.waitKey(1)
            
            if self.shot_image is not None:
                # print('AA')
                dt_now = datetime.datetime.now()

                dir_path = f"data/{self.shot_image}/"
                # dir_path = Path(__file__).resolve().parent / "data" / self.shot_image
                # print(dir_path)
                os.makedirs(dir_path, exist_ok=True)
                print('hh')
                # cv2.imwrite(f"{dir_path / }{dt_now.strftime('%Y-%m-%d_%H-%M-%S')}.png", frame)
                cv2.imwrite(f"{dir_path}{dt_now.strftime('%Y-%m-%d_%H-%M-%S')}.png", frame)
                print('gg')
                # self.camera.cap.release()
                # cv2.destroyAllWindows()

                self.shot_image = None
    
    def start(self):
        self.thread_monitoring_button_state = threading.Thread(
            target=self.monitoring_button_state)
        self.thread_streaming = threading.Thread(target=self.streaming)

        # tpe = ThreadPoolExecutor(max_workers=2)

        self.thread_monitoring_button_state.start()
        self.thread_streaming.start()

        # self.tpe.submit(self.monitoring_button_state)
        # self.tpe.submit(self.streaming)
    
    def stop(self):
        self.finish_flag = True
        self.thread_monitoring_button_state.join()
        self.thread_straeming.join()

        # self.tpe.shutdown()

if __name__ == "__main__":
    # os.chdir(os.path.dirname(os.path.abspath('__file__')))
    pid = 29987
    camera_id = 2

    camerashot = CameraShot(pid, camera_id)
    # print(1)
    camerashot.start()
    # print(2)
    # camerashot.stop()


# python Desktop/Rutilea/switch/button.py
