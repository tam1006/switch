from typing import List
import os
from threading import Thread
import time
from serial import Serial
from serial.tools import list_ports
import cv2
import re
import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
import numpy as np


class Button(Serial):
    def __init__(self, pid):
        super().__init__(port=self._find_port_names(
            pid=pid)[0], baudrate=9600, timeout=0)

    def check_button(self):
        print("SS")
        while True:
            line = str(self.readline())
            result = re.findall("switched", line)
            if len(result) != 0:  # first readline
                signal = str(self.readline())  # second readline
                which_switch = re.findall(r'[0-9]', signal)
                if which_switch[0] == "1":
                    return "green"
                elif which_switch[0] == "3":
                    return "red"
                elif which_switch[0] == "4":
                    return "black"
                else:
                    return None
            time.sleep(0.01)

    def _find_port_names(self, pid):
        ports = list_ports.comports()
        found_port_names = []
        for port in ports:
            if port.pid == pid:
                found_port_names.append(port.device)
        return found_port_names


class Camera:
    def __init__(self, camera_id):
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)


class CameraShot:
    def __init__(self, pid, camera):
        self.button = Button(pid=pid)
        self.camera = camera
        self.shot_image = None
        self.finish_flag = False
        self.thread_monitoring_button_state = None
        self.thread_streaming = None
        self.tpe = ThreadPoolExecutor(max_workers=2)
        self.image_color = None
        self.image_name = None
        self.image_location = None

    def monitoring_button_state(self):
        while not self.finish_flag:
            if not self.shot_image:
                self.shot_image = self.button.check_button()
                self.image_color = self.shot_image
                if not self.shot_image:
                    self.finish_flag = True
                    break
                print(f"image = {self.shot_image}")
                cv2.waitKey(1000)

    def streaming(self):
        # _, frame = self.camera.cap.read()
        while not self.finish_flag:
            _, frame = self.camera.cap.read()
            # if frame is not None:

            # cv2.imshow("title", frame)
            # cv2.waitKey(1)
            # App.update()

            if self.shot_image is not None:
                # print('AA')
                dt_now = datetime.datetime.now()

                dir_path = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/image_data/{self.shot_image}/"
                print(dir_path)
                os.makedirs(dir_path, exist_ok=True)

                image_date = dt_now.strftime('%Y-%m-%d_%H-%M-%S')
                cv2.imwrite(f"{dir_path}{image_date}.png", frame)

                self.image_name = image_date
                self.shot_image = None

    def taken_image(self):
        while not self.finish_flag:
            if not self.image_color:
                dir_path = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/image_data/{self.image_color}/"
                self.image_location = f"{dir_path}{image_name}.png"

                image_color = None

    def start(self):
        self.thread_monitoring_button_state = threading.Thread(
            target=self.monitoring_button_state)
        self.thread_streaming = threading.Thread(target=self.streaming)
        self.thread_taken_image = threading.Thread(target=self.taken_image)

        self.thread_monitoring_button_state.start()
        self.thread_streaming.start()

    def stop(self):
        self.finish_flag = True

        self.thread_monitoring_button_state.join()
        # self.thread_straeming.join()


class App():
    def __init__(self, window, window_title, camera):
        self.window = window
        self.window.title(window_title)
        self.camera = camera

        self._, self.vcap = self.camera.cap.read()
        # self.width = self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # カメラモジュールの映像を表示するキャンバスを用意する
        # self.canvas = tkinter.Canvas(window, width=self.width, height=self.height)
        self.canvas = tkinter.Canvas(window)

        self.canvas.pack()

        # Closeボタン
        self.close_btn = tkinter.Button(window, text="Close")
        self.close_btn.pack()
        self.close_btn.configure(command=self.destructor)

        # update()関数を15ミリ秒ごとに呼び出し、
        # キャンバスの映像を更新する
        self.delay = 15
        self.update()

        self.window.mainloop()

    # キャンバスに表示されているカメラモジュールの映像を
    # 15ミリ秒ごとに更新する
    def update(self):
        _, frame = self.camera.cap.read()

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    # Closeボタンの処理
    def destructor(self):
        self.window.destroy()
        self.vcap.release()


if __name__ == "__main__":
    pid = 29987
    camera_id = 0

    # camerashot = CameraShot(pid, camera_id)
    # camerashot.start()

    camera = Camera(camera_id)
    camera_shot = CameraShot(pid, camera)
    app = App(tkinter.Tk(), "Camera Capture", camera)

    while True:
        if camera_shot.finish_flag:
            camera_shot.stop()
            break

    # print(2)
    # camerashot.stop()


# python Desktop/Rutilea/switch/button.py
