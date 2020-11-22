from serial import Serial
from serial.tools import list_ports
import cv2
import re
import datetime
from pathlib import Path
from threading import Thread
import tkinter
from PIL import Image, ImageTk
import numpy as np
import PIL
import time
import sys
import os

class Button(Serial):
    def __init__(self, pid):
        try:
            super().__init__(port=self._find_port_names(pid=pid)[0], baudrate=9600, timeout=0.5)
        
        except IndexError:
            print('スイッチが接続されていません')
            print('スイッチを接続して再度アプリを起動してください')
            time.sleep(5) 
            sys.exit(1)

    # check what color of button is pushed
    def check_button(self):
        try:
            msg = self.readline()
        except:
            print('スイッチとの接続が遮断されました')
            print('スイッチを接続して再度アプリを起動してください')
            return "error"

        line = str(msg)
        result = re.findall("switched", line)

        if len(result)!=0: # first readline
            signal = str(self.readline()) # second readline
            which_switch = re.findall(r'[0-9]',signal)
            if which_switch[0]== "3":
                return "green", u"良品"
            elif which_switch[0]== "1":
                return "red", u"不良品"
            elif which_switch[0]== "0":
                return "black", u"判別不能"
            else:
                return "", ""
        else:
            return None

        time.sleep(0.01)

    @staticmethod
    def _find_port_names(pid):
        ports = list_ports.comports()
        found_port_names = []
        for port in ports:
            if port.pid == pid:
                found_port_names.append(port.device)
        return found_port_names

class Camera:
    def __init__(self, camera_id):
        # return Error if the camera is not connected
        try:
            self.cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
            self.cap.read()[1].shape[0:2]
        except AttributeError:
            print('カメラが接続されていません')
            print('カメラを接続して再度アプリを起動してください')
            time.sleep(5)
            sys.exit(1)

        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        
    def get_size(self):
        return self.cap.read()[1].shape[0:2]

    def shot(self):
        return self.cap.read()[1]

class CameraShot:
    def __init__(self, pid, camera_id):
        self.button = Button(pid=pid)
        self.camera = Camera(camera_id)
        self.gui = GUI(camera=self.camera)
        self.gui_thread = Thread(target=self.gui.start)
        self.gui_thread.start()
        self.finish_flag = False
        self.base_dir = Path(__file__).resolve().parent.joinpath("image_data")
    
    # monitor button state
    # if button is pushed: save image
    # if finish button is pushed: finish
    def monitoring_button_state(self):
        while not self.finish_flag:
            pushed_color = self.button.check_button()
            if pushed_color is None:
                pass
            elif pushed_color == "error":
                self.stop()
                time.sleep(1)
                break
            elif pushed_color[0] == "":
                # print('\nFinish')
                self.stop()
                time.sleep(5)
                break
            elif pushed_color is not None:
                # print(f"{pushed_color[0]} is pushed")
                frame = self.camera.shot()
                self.save_image(pushed_color[1], frame)
                self.gui.change_image(frame, pushed_color[1])
                time.sleep(1)
            
    # save image in each directory
    def save_image(self, color: str, frame: np.ndarray):
        save_dir = self.base_dir / color
        save_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        save_path = save_dir / f"{ts}.png"
        imwrite_ja(str(save_path), frame)

    # start multithread
    def start(self):
        self.finish_flag = False
        self.thread_monitoring_button_state = Thread(target=self.monitoring_button_state)
        self.thread_monitoring_button_state.start()
    
    # stop multithread
    def stop(self):
        self.finish_flag = True
        self.gui.stop()
        self.gui_thread.join()

class GUI:
    def __init__(self, camera):
        self.camera = camera
    
    # start gui
    def start(self):
        self.window = tkinter.Tk()
        self.window.title("RUTILEA")
        self.base_dir = f"{os.getcwd()}/data"
        self.window.iconbitmap(f'{self.base_dir}/RUTILEA.ico')
        self.window.attributes('-fullscreen', True)
        # self.window.state('zoomed')
        self.height, self.width = self.camera.get_size()
        self.height = int(self.height*0.95)
        self.width = int(self.width*0.95)
        self.ipadx, self.ipady = 15, 10
        self.gui_finish_flag = False

        # make a blank located on the top window
        # self.rutilea_ico = tkinter.PhotoImage(file=f"{self.base_dir}/RUTILEA.png")
        # self.canvas_rutilea = tkinter.Canvas(self.window, width=self.width, height=150)
        # self.canvas_rutilea.create_image(10, 40, image=self.rutilea_ico, anchor=tkinter.W)
        # self.canvas_rutilea.grid(column=0, row=0)

        self.blank = tkinter.Canvas(self.window, height=100)
        self.blank.grid(column=0, row=0)

        # make a canvas of movie
        self.canvas_camera = tkinter.Canvas(self.window, width=self.width, height=self.height)
        self.canvas_camera.grid(column=0, row=1, padx=self.ipadx, pady=self.ipady, sticky=tkinter.S)

        # make a canvas of taken image
        # initialize black image
        self.original_image = PIL.Image.fromarray(np.zeros((self.height, self.width, 3), dtype=np.uint8))
        self.picture_image = ImageTk.PhotoImage(self.original_image)
        self.canvas_picture = tkinter.Canvas(self.window, width=self.width,  height=self.height)
        self.canvas_picture.create_image(0, 0, image=self.picture_image, anchor=tkinter.NW)
        self.canvas_picture.grid(column=1, row=1, padx=self.ipadx, pady=self.ipady, sticky=tkinter.S)

        # # Close button
        # # if you want to make, uncomment
        # self.close_btn = tkinter.Button(self.window, text="Close", width=5, height=5)
        # self.close_btn.grid(column=2, row=0, padx=self.padx, pady=self.pady)
        # self.close_btn.configure(command=self.stop)

        # label of movie
        self.movie_label = tkinter.Label(self.window, text=u"カメラ映像", font=('MSゴシック', "25", "bold"))
        self.movie_label.grid(column=0, row=2, ipadx=self.ipadx, ipady=self.ipady, sticky=tkinter.N)

        # label of image
        self.image_text = tkinter.StringVar()
        self.image_text.set(u"撮影した画像が表示されます")
        self.image_label = tkinter.Label(
            self.window, textvariable=self.image_text, font=('MSゴシック', "25", "bold"))
        self.image_label.grid(column=1, row=2, ipadx=self.ipadx, ipady=self.ipady)

        # label of RUTILEA
        self.rutilea_label = tkinter.Label(self.window, text="R  U  T  I  L  E  A", font=('', '40', "bold"))
        self.rutilea_label.grid(column=0, columnspan=2, row=3, ipadx=self.ipadx, ipady=self.ipady+60, sticky=tkinter.S)

        # call update() by 1mm sec to update the movie
        # if you decreade delay, fps increase
        self.delay = 1
        self.update()
        self._check_to_quit()

        self.window.mainloop()

        self.camera.cap.release()

        # deleate instance variables
        del self.window
        del self.height
        del self.width
        del self.ipadx
        del self.ipady
        del self.gui_finish_flag
        del self.canvas_camera
        del self.original_image
        del self.picture_image
        del self.canvas_picture
        del self.movie_label
        del self.image_text
        del self.image_label
        del self.delay
        del self.camera_monitoring_img
        del self.blank
        del self.rutilea_label
        # del self.canvas_rutilea
        # del self.rutilea_ico
        # del self.close_btn     
    
    # check whether gui_finish_flag is True or False
    def _check_to_quit(self):
        if not self.gui_finish_flag:
            self.window.after(10, self._check_to_quit)
        else:
            self.window.destroy()

    # change the movie by every self.delay seconds
    def update(self):
        frame = self.camera.shot()
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.camera_monitoring_img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas_camera.create_image(0, 0, image=self.camera_monitoring_img, anchor = tkinter.NW)
            self.window.after(self.delay, self.update)
        except:
            self.stop()
            print("カメラとの接続が遮断されました")
            print('終了ボタンを押してアプリを終了してください')
            print("その後カメラを接続して再度アプリを起動してください")
            time.sleep(3)
            
    # change the image
    def change_image(self, new_image: np.ndarray, new_image_color: str):
        # print(new_image.shape)
        self.picture_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        self.picture_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.picture_image))
        self.canvas_picture.create_image(0, 0, image=self.picture_image, anchor=tkinter.NW)
        self.image_text.set("")
        time.sleep(0.1)
        self.image_text.set(f"{new_image_color}フォルダに保存しました")

    # Close button
    def stop(self):
        self.gui_finish_flag = True


def imwrite_ja(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    pid = 29987
    camera_id = 0
    camera_shot = CameraShot(pid, camera_id)
    camera_shot.start()