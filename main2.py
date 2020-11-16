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

class Button(Serial):
    def __init__(self, pid):
        super().__init__(port=self._find_port_names(pid=pid)[0], baudrate=9600, timeout=0.5)

    # check what color of button is pushed
    def check_button(self):
        msg = self.readline()
        line = str(msg)
        result = re.findall("switched", line)

        if len(result)!=0: # first readline
            signal = str(self.readline()) # second readline
            which_switch = re.findall(r'[0-9]',signal)
            if which_switch[0]== "1":
                return "green"
            elif which_switch[0]== "3":
                return "red"
            elif which_switch[0]== "4":
                return "black"
            else:
                return ""
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
            # if self.gui._gui_check_quit():
            #     print(7)
            #     print('Finish')
            #     self.stop()
            #     time.sleep(1)
            #     break

            pushed_color = self.button.check_button()
            if pushed_color is None:
                pass
            elif pushed_color == "":
                print('\nFinish')
                self.stop()
                time.sleep(1)
                break
            elif pushed_color is not None:
                print(f"{pushed_color} is pushed")
                frame = self.camera.shot()
                self.save_image(pushed_color, frame)
                self.gui.change_image(frame, pushed_color)
                time.sleep(1)
            
    # save image in each directory
    def save_image(self, color: str, frame: np.ndarray):
        save_dir = self.base_dir / color
        save_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        save_path = save_dir / f"{ts}.png"
        cv2.imwrite(str(save_path), frame)

    # start multithread
    def start(self):
        self.finish_flag = False
        self.thread_monitoring_button_state = Thread(target=self.monitoring_button_state)
        self.thread_monitoring_button_state.start()
    
    # stop multithread
    def stop(self):
        self.finish_flag = True
        # self.thread_monitoring_button_state.join()
        self.gui.stop()
        self.gui_thread.join()

class GUI:
    def __init__(self, camera):
        self.camera = camera
    
    # start gui
    def start(self):
        self.window = tkinter.Tk()
        self.window.title("RUTILEA")
        self.window.iconbitmap('RUTILEA.ico')
        # self.window.geometry('+0+0')
        self.window.attributes('-fullscreen', True)
        self.height, self.width = self.camera.get_size()
        self.padx, self.pady = 20, 100
        self.gui_finish_flag = False

        # make a canvas of movie
        self.canvas_camera = tkinter.Canvas(self.window, width=self.width, height=self.height)
        self.canvas_camera.grid(column=0, row=0, padx=self.padx, pady=self.pady)

        # make a canvas of taken image
        # initialize black image
        self.original_image = PIL.Image.fromarray(np.zeros((self.height, self.width, 3), dtype=np.uint8))
        self.picture_image = ImageTk.PhotoImage(self.original_image)
        self.canvas_picture = tkinter.Canvas(self.window, width=self.width,  height=self.height)
        self.canvas_picture.create_image(0, 0, image=self.picture_image, anchor=tkinter.NW)
        self.canvas_picture.grid(column=1, row=0, padx=self.padx, pady=self.pady)

        # # Close button
        # # if you want to make, uncomment
        # self.close_btn = tkinter.Button(self.window, text="Close", width=5, height=5)
        # self.close_btn.grid(column=2, row=0, padx=self.padx, pady=self.pady)
        # self.close_btn.configure(command=self.stop)

        # label of movie
        self.movie_label = tkinter.Label(self.window, text=u"カメラ映像", font=('MSゴシック', "30", "bold"))
        self.movie_label.grid(column=0, row=1, padx=self.padx, pady=self.pady)

        # label of image
        self.image_text = tkinter.StringVar()
        self.image_text.set(u"撮影した画像が表示されます")
        self.image_label = tkinter.Label(
            self.window, textvariable=self.image_text, font=('MSゴシック', "30", "bold"))
        self.image_label.grid(column=1, row=1, padx=self.padx, pady=self.pady)

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
        del self.padx
        del self.pady
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
        # del self.close_btn
    
    # check whether gui_finish_flag is True or False
    def _check_to_quit(self):
        if not self.gui_finish_flag:
            self.window.after(10, self._check_to_quit)
        else:
            self.window.destroy()

    # def _gui_check_quit(self):
    #     print(8)
    #     if not self.gui_finish_flag:
    #         print('SS')
    #         return False
    #     else:
    #         print('JJ')
    #         return True

    # change the movie by every self.delay seconds
    def update(self):
        frame = self.camera.shot()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.camera_monitoring_img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas_camera.create_image(0, 0, image=self.camera_monitoring_img, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)

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

if __name__ == "__main__":
    pid = 29987
    camera_id = 2
    camera_shot = CameraShot(pid, camera_id)
    camera_shot.start()
