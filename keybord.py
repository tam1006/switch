import cv2
import os
import datetime
dt_now = datetime.datetime.now()


def save_frame_camera_key(device_num, dir_path, basename, ext='png', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    while True:
        ret, frame = cap.read()
        windowsize = (800, 600)
        frame = cv2.resize(frame, windowsize)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
            cv2.imwrite(
                dir_path + "{}.png".format(dt_now.strftime('%Y-%m-%d_%H-%M-%S')), frame)

        elif key == ord('q'):
            break
    
    capture.release()
    cv2.destroyAllWindowsS()
    
save_frame_camera_key(2, 'data/temp', 'camera_capture')
