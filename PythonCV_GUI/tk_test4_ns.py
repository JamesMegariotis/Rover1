import cv2
import time
import datetime

import Tkinter as tk

from PyMata.pymata import PyMata
from PIL import Image, ImageTk
from collections import deque

# Declare motor driver pins
PWM_L = 3
PWM_R = 11
DIR_L = 12
DIR_R = 13

# Define Directions
CW = 0
CCW = 1

# Define Motors
MOTOR_L = 0
MOTOR_R = 1

direction = None

def quit_(root,cam):
    del(cam)
    root.destroy()

def update_image(image_label, cam):
    (readsuccessful, f) = cam.read()
    gray_im = cv2.cvtColor(f, cv2.COLOR_BGR2RGBA)
    a = Image.fromarray(gray_im)
    b = ImageTk.PhotoImage(image=a)
    image_label.configure(image=b)
    image_label._image_cache = b  # avoid garbage collection
    root.update()


def update_fps(fps_label):
    frame_times = fps_label._frame_times
    frame_times.rotate()
    frame_times[0] = time.time()
    sum_of_deltas = frame_times[0] - frame_times[-1]
    count_of_deltas = len(frame_times) - 1
    try:
        fps = int(float(count_of_deltas) / sum_of_deltas)
    except ZeroDivisionError:
        fps = 0
    fps_label.configure(text='FPS: {}'.format(fps))


def update_all(root, image_label, cam, fps_label):
    update_image(image_label, cam)
    update_fps(fps_label)
    root.after(40, func=lambda: update_all(root, image_label, cam, fps_label))

def image_capture(cam):
    timestamp=time.time()
    timestamp_string=datetime.datetime.fromtimestamp(timestamp).strftime('%m-%d-%Y_%H-%M-%S')
    fn='Rover1_'+timestamp_string+'.jpg'
    (ret, raw_img) = cam.read()
    img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGBA)
    a = Image.fromarray(img)
    a.save(fn, 'JPEG')

def on_press(event):
    delta = {
        "Right": (CW,CW),
        "Left": (CCW, CCW),
        "Up": (CCW,CW),
        "Down": (CW,CCW)
    }
    direction = delta.get(event.keysym, None)

def on_release(event):
    direction = None

def animate(root):
    if direction is not None:
            update_drive()
    root.after(25, func=lambda: animate(root))

def update_drive():
    pwm=int(speed_scale.get())
    print(pwm+','+direction)
        


if __name__ == '__main__':
    # Create a PyMata instance
    #create gui
    root = tk.Tk() 
    image_label = tk.Label(master=root)# label for the video frame
    image_label.pack()
    cam = cv2.VideoCapture(0) 
    fps_label = tk.Label(master=root)# label for fps
    fps_label._frame_times = deque([0]*5)  # arbitrary 5 frame average FPS
    fps_label.pack()
    speed_scale=tk.Scale(master=root, from_=255, to=150, label='Motor Speed')
    speed_scale.pack()
    speed_scale.set(150)
    canvas = tk.Canvas(master=root,width=400, height=400)
    canvas.pack()
    canvas.bind("<Any-KeyPress>", on_press)
    canvas.bind("<Any-KeyRelease>", on_release)
    canvas.bind("<1>", lambda event: canvas.focus_set())
    # button_frame = tk.Frame(master=root)
    # button_frame.pack()
    # forward_button=tk.Button(master=button_frame, text = 'Drive Forward', command =lambda: drive_forward(speed_scale.get(), board))
    # forward_button.grid(row=0, column=1)
    # reverse_button=tk.Button(master=button_frame, text = 'Drive Reverse', command =lambda: drive_reverse(speed_scale.get(), board))
    # reverse_button.grid(row=2, column=1)
    # left_button=tk.Button(master=button_frame, text = 'Turn Left', command =lambda: turn_left(speed_scale.get(), board))
    # left_button.grid(row=1, column=0)
    # right_button=tk.Button(master=button_frame, text = 'Turn Right', command =lambda: turn_right(speed_scale.get(), board))
    # right_button.grid(row=1, column=2)
    img_cap_button=tk.Button(master=root, text = 'Capture Image', command =lambda: image_capture(cam))
    img_cap_button.pack()
    # quit button
    quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,cam,board))
    quit_button.pack()
    # setup the update callback
    root.after(0, func=lambda: update_all(root, image_label, cam, fps_label))
    root.after(0, func=lambda: animate(root))
    root.mainloop()