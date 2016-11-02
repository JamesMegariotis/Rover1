import Tkinter as tk
import time

from PyMata.pymata import PyMata

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

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # self.board = PyMata("COM5", verbose=True)
        # self.board.set_pin_mode(PWM_L, board.PWM, board.DIGITAL)
	    # self.board.set_pin_mode(PWM_R, board.PWM, board.DIGITAL)
	    # self.board.set_pin_mode(DIR_L, board.OUTPUT, board.DIGITAL)
	    # self.board.set_pin_mode(DIR_R, board.OUTPUT, board.DIGITAL)
        self.direction = None
        self.canvas = tk.Canvas(width=400, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Any-KeyPress>", self.on_press)
        self.canvas.bind("<Any-KeyRelease>", self.on_release)
        self.canvas.bind("<1>", lambda event: self.canvas.focus_set())
        self.speed_scale=tk.Scale(from_=255, to=150, label='Motor Speed')
	    # self.speed_scale.pack()
	    # self.speed_scale.set(150)
        self.animate()

    def on_press(self, event):
        delta = {
            "Right": (CW,CW),
            "Left": (CCW, CCW),
            "Up": (CCW,CW),
            "Down": (CW,CCW)
        }
        self.direction = delta.get(event.keysym, None)

    def on_release(self, event):
        self.direction = None

    def animate(self):
        if self.direction is not None:
        	time.sleep(0.001)
            # update_drive()
        self.after(25, self.animate)

    def update_drive(self):
    	pwm=int(self.speed_scale.get())
	    # motor_driver(MOTOR_L, CW, pwm)
	    # motor_driver(MOTOR_R, CW, pwm)

    def motor_driver(motor, direction, pwm_speed):
	    if(motor==MOTOR_L):
	    	time.sleep(0.001)
	        # self.board.digital_write(DIR_L, direction)
	        # self.board.analog_write(PWM_L, pwm_speed)
	    elif(motor==MOTOR_R):
	    	time.sleep(0.001) 
	        # self.board.digital_write(DIR_R, direction)
	        # self.board.analog_write(PWM_R, pwm_speed)

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()