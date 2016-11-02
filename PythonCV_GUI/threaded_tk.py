#Import python firmata library for communication with arduino
import pyfirmata
from Tkinter import *
import time
import picamera
import threading
import datetime


on=True
ison=True
off=False
video_on=False
sweep_on = False
sweep_count = 0
sweep1 = True
sweep2 = False

#Initialize arduio board and serial port
board=pyfirmata.Arduino('/dev/ttyACM0')
#Initialize servo pins
tilt_servo_pin=board.get_pin('d:11:s')
pan_servo_pin=board.get_pin('d:10:s')
#set servos to initial angles
tilt_servo_pin.write(56)
pan_servo_pin.write(13)

#create app with threading capability to run below while loop simultaneously
class App(threading.Thread):
	
	#initialize app
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()

	#Run setup			
	def run(self):
		#create tkinter gui and make necesary buttons and scales
		self.root=Tk()
		frame=Frame()
		frame.pack()
		#create tilt servo scale bar and set it to initial servo value
		scale=Scale(frame, from_=180, to=0, orient=VERTICAL, label='Tilt', command=self.update_tilt)
		scale.grid(row=0, column=0)
		scale.set(56)
		#create pan servo scale bar and set it to initial servo value
		self.root.scale2=Scale(frame, from_=0, to=120, orient=HORIZONTAL, label='Pan', command=self.update_pan)
		self.root.scale2.grid(row=1, column=1)
		self.root.scale2.set(13)
		#create camera on off button
		button=Button(frame, text = 'Camera (on/off)', command = self.camera_switch)
		button.grid(row=2, column=0)
		#create image capture button
		button2=Button(frame, text = 'Capture Image', command = self.image_capture)
		button2.grid(row=2, column=1)
		#create quit button
		button3=Button(frame, text = 'quit', command = self.quitnow)
		button3.grid(row=2, column=2)
		#create video capture button
		self.root.button4=Button(frame, text = 'Capture Video', command = self.video_capture)
		self.root.button4.grid(row=3, column=1)
		#create servo sweep button
		self.root.button5=Button(frame, text = 'Sweep', command = self.sweep)
		self.root.button5.grid(row=3, column=0)
		self.root.wm_title('Camera Pan/Tilt Controller')
		self.root.geometry("400x600+0+0")
		self.root.mainloop()
		
	#Update tilt servo when button is pressed		
	def update_tilt(self, tilt_angle):
		angle=int(tilt_angle)
		global tilt_servo_pin
		tilt_servo_pin.write(angle)
		time.sleep(0.01)
	
	#Update pan servo when button is pressed
	def update_pan(self, pan_angle):
		angle=int(pan_angle)
		global pan_servo_pin
		pan_servo_pin.write(angle)
		time.sleep(0.01)
		
	#Sweep servo back and forth when button is pressed	
	def sweep(self):
		global sweep_on
		global sweep_count
		if sweep_on == False:
			sweep_on = True
			self.root.button5.config(relief=SUNKEN)
		else:
			sweep_on = False
			self.root.button5.config(relief=RAISED)
			self.root.scale2.set(sweep_count)
			sweep_count=0
	#Capture image with a timestamped file name when image capture button is pressed	
	def image_capture(self):
		timestamp=time.time()
		timestamp_string=datetime.datetime.fromtimestamp(timestamp).strftime('%m-%d-%Y_%H:%M:%S')
		camera.capture('PanTilt'+timestamp_string+'.jpg')
	
	#Capture video when video capture button is pressed and set button to show recording status
	def video_capture(self):
		global video_on
		if video_on == False:
			video_on = True
			self.root.button4.config(relief=SUNKEN)
		else:
			video_on = False
			self.root.button4.config(relief=RAISED)
			
	#Turns camera feed on and off	
	def camera_switch(self):
		global ison
		if ison == True:
			ison = False
		else:
			ison = True
	
	#Quits app cleanly	
	def quitnow(self):
		global off
		off=True
		global ison
		ison = False
		tilt_servo_pin.write(56)
		pan_servo_pin.write(13)
		time.sleep(0.3)
		board.exit()
		self.root.quit()
		
app=App()

#Runs concurrently with the above gui app
while True:
	#generate video preview window to view camera feed
	if ison:
		with picamera.PiCamera() as camera:
			#Set resolution, position, and display preview
			camera.resolution = (1024,768)
			camera.preview_fullscreen=False
			camera.preview_window=(100, 350, 350,300)
			camera.start_preview()
			
			#Sweep camera back and forth while sweep button is pressed
			while ison:
				time.sleep(0.1)
				if sweep_on and sweep1:
					sweep_count=sweep_count+1
					pan_servo_pin.write(sweep_count)
					time.sleep(0.02)
					if sweep_count==120:
						sweep1 = False
						sweep2 = True
				if sweep_on and sweep2:
					sweep_count=sweep_count-1
					pan_servo_pin.write(sweep_count)
					time.sleep(0.02)
					if sweep_count==0:
						sweep1 = True
						sweep2 = False
				#if the video capture button is pressed, begin recording video with time stamped title		
				if video_on:
					timestamp=time.time()
					timestamp_string=datetime.datetime.fromtimestamp(timestamp).strftime('%m-%d-%Y_%H:%M:%S')
					camera.start_recording('PanTiltVideo'+timestamp_string+'.h264')
					#while the video capture button is sunken, continue recording, if pressed again, loop discontinues
					while video_on:
						camera.wait_recording(1)
					#Stop recording	
					camera.stop_recording()
				on=ison
	#discontinue loop if quit button is pressed			
	if off:
		break

		
