''' TODO LIST 
	Split classes into separate modules
	Remove Search specific labels
	Remove SQL Database functionality
	Talk about how inputs will be read
	Change file-reading titles
	Fix comments so they apply to AI
'''

import tkinter as tk
import numpy as np
import os.path
import time

import matplotlib
matplotlib.use("TkAgg") # backend of matplotlib -
						# configure to use matplotlib inside of Tkinter windows
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg #use the default matplotlib drawing surface + toolbar
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt

# Define background plot style
style.use("ggplot")	

# Define the graph
graphFig = plt.Figure() 

# Refresh rate for plots in milliseconds
refreshRate = 1000

# TODO - List filenames here

class App(tk.Tk):	# Main Window container of our Application

	def __init__(self, *args, **kwargs): 

		tk.Tk.__init__(self, *args, **kwargs)	# initialize Tkinter window	
		container = tk.Frame(self)	# create a frame for the window

		container.pack(side="top", fill="both", expand=True)	# configure geometry layout of elements
		container.grid_rowconfigure(0, weight=1)		
		container.grid_columnconfigure(0, weight=1)

		self.resizable(False, False) # disable resizing from the user

		x = (self.winfo_screenwidth() - 	# change where the window
			self.winfo_reqwidth()) / 8		# appears on the screen
		y = (self.winfo_screenwidth() - 
			self.winfo_reqwidth()) / 8

		''' May be deprecated in python 3
		self.geometry("+{xpos}+{ypos}".format(xpos=x, ypos=y))
		'''

		self.title("Bot-the-Builder Graphing Interface")

		graphframe = GraphPage(container, self)	# create a frame for graphing
		graphframe.grid(row=0, column=0, sticky="nsew") # grid begins at row 0 and column 0 and stretches in all directions
		graphframe.tkraise()	# raise the current frame to the front of the display

	def close_program(self):
		self.destroy()

		
class GraphPage(tk.Frame): # Graphing class for plotting 

	def __init__(self, parent, controller):	# parent = tk.Frame (main window), controller = instance of App (Tk.tk)
		tk.Frame.__init__(self, parent)	

		button_frame = tk.Frame(self) 
		button_frame.pack(padx=15) 

		display_frame = tk.Frame(self)
		display_frame.pack(padx=15)
			
		myCanvas = FigureCanvasTkAgg(graphFig, self) # add the matplotlib graph to the Tkinter window
		myCanvas.show()
		myCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		myToolBar = NavigationToolbar2TkAgg(myCanvas, self)	# add the matplotlib toolbar to the bottom left 	
		myToolBar.update()
		myCanvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		self.newRun_button = tk.Button(button_frame, text="New Run",
									command=self.start_run)
		self.newRun_button.pack(side='left')

		self.runTimer = tk.Message(display_frame, text="TODO - Add the timing here in seconds",
								   width=500, font=("Verdana", 12))
		self.runTimer.pack(side='right')

		# label to display data point info
		self.pickMessage = tk.Message(display_frame, text="no data selected", width=500, font=("Verdana", 12)) 
		self.pickMessage.pack(side='right')

		# pause the animation
		self.pause_button = tk.Button(button_frame, state='active', text="Pause Animation",		
								command=self.pause_animation) 	
		# resume the animation						
		self.resume_button = tk.Button(button_frame, state='disabled', text="Resume Animation",		
								command=self.resume_animation) 	

		self.quit_button = tk.Button(button_frame, text="Quit",
		  					command=lambda: controller.close_program()) 	
		self.quit_button.pack(side='left')	

	def start_run(self):	# initialize the replay parser
		self.newRun_button.pack_forget()
		self.quit_button.pack_forget()
		self.pause_button.pack(side='left')
		self.resume_button.pack(side='left')
		self.quit_button.pack(side='left')
		self.resume_animation()

	def pause_animation(self):	# pause the animation
		self.anim.event_source.stop()
		self.pause_button.configure(state='disabled')
		self.resume_button.configure(state='active')
		self.runTimer.configure(text='Animation paused...press resume to continue')

	def resume_animation(self):	# resume the animation
		self.anim.event_source.start()
		self.resume_button.configure(state='disabled')
		self.pause_button.configure(state='active')		
		 
root = App()
root.geometry("1280x720")
root.mainloop()