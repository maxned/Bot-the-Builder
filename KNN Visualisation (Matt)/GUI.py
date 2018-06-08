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
num_files = 4
data_file1 = "K_5.csv" 
data_file2 = "K_10.csv" 
data_file3 = "K_15.csv"
data_file4 = "K_20.csv"

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

		# create the plot manager
		self.plot_container = PlotManager(self)

		# start the animation
		self.anim = animation.FuncAnimation(graphFig, self.plot_container.animate, interval=refreshRate)

		# button to pause the animation
		self.pause_button = tk.Button(button_frame, state='active', text="Pause Animation",
								command=self.pause_animation)
		# button to resume the animation
		self.resume_button = tk.Button(button_frame, state='disabled', text="Resume Animation",
								command=self.resume_animation)

		self.quit_button = tk.Button(button_frame, text="Quit",
		  					command=lambda: controller.close_program())
		self.quit_button.pack(side='left')

		self.start_run()

	def start_run(self):	# initialize the replay parser
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

class PlotManager(object):	# contains logic for subplots

	def __init__(self, parent):	# create the subplots and place within 'graphFig' figure object
		self.parent = parent	# reference to graphPage

		# Plot definitions
		self.plot1 = graphFig.add_subplot(2, 2, 1) 		# create a 1x2 plot at subplot 1
		self.plot2 = graphFig.add_subplot(2, 2, 2)		# create a 1x2 plot at subplot 2
		self.plot3 = graphFig.add_subplot(2, 2, 3)		# dynamic plots update as the files are changed
		self.plot4 = graphFig.add_subplot(2, 2, 4)

	def animate(self, i):	# animate graphs
		filesExist = self.check_for_files()

		if(filesExist): # all files exist
			graphFig.tight_layout()	# use tight layout for cleaner display of plot elements

			self.handle_new_data()

			self.update_plots()

		else:
			self.parent.runTimer.configure(text="Missing Input files...")

	def read_background_files(self):	# continue to read files even when animation is paused
		while(str(self.parent.pause_button['state']) == 'disabled'):
			self.handle_new_data()
			time.sleep(1)	# sleep 1 second

	def handle_new_data(self):	# check for updates to plot_data
		xData, yData = self.get_plot_data(data_file1)

		self.data_x = list(xData)
		self.data_y = list(yData)

	def update_plots(self): 	# update dynamic (animated) plots
		xData, yData = self.get_plot_data(data_file1)
		if(xData and yData):
			self.update_plot(self.plot1, xData, yData,
				xlabel='time (seconds)',
				ylabel='probability of win (%)',
				title ='Probability of Winning vs. Time for K = 5',
				settings='b-D')	# bo = blue, circles (scatter-points)

		# xData, yData = retrieve dynamic plot 2 data
		xData, yData = self.get_plot_data(data_file2)
		if(xData and yData):
			self.update_plot(self.plot2, xData, yData,
								xlabel='time (seconds)',
							 	ylabel='probability of win (%)',
							 	title ='Probability of Winning vs. Time for K = 10',
			 					settings='r-D')	# r-D = red, diamonds with a line through points '''
		
		xData, yData = self.get_plot_data(data_file3)
		if(xData and yData):
			self.update_plot(self.plot3, xData, yData,
								xlabel='time (seconds)',
							 	ylabel='probability of win (%)',
							 	title ='Probability of Winning vs. Time for K = 15',
			 					settings='g-D')	# r-D = red, diamonds with a line through points '''

		xData, yData = self.get_plot_data(data_file4)
		if(xData and yData):
			self.update_plot(self.plot4, xData, yData,
								xlabel='time (seconds)',
							 	ylabel='probability of win (%)',
							 	title ='Probability of Winning vs. Time for K = 20',
			 					settings='y-D')	# r-D = red, diamonds with a line through points '''

	def check_for_files(self):	# check that all input files exist
		fileCounter = 0
		fileCounter += self.check_fileExists(data_file1)
		fileCounter += self.check_fileExists(data_file2)
		fileCounter += self.check_fileExists(data_file3)
		fileCounter += self.check_fileExists(data_file4)
		
		if(fileCounter == num_files):
			return 1
		else:
			return 0

	def check_fileExists(self, fileName):	# check that the files exist before starting the animation
		if(os.path.isfile(fileName)):
			return 1
		else:
			return 0

	def get_plot_data(self, fileName):	# read from a file and get data
		pullData = open(fileName, "r").read() # open file for reading
		dataList = pullData.split('\n')	# read file, delimited by new-lines
		xList = []
		yList = []

		for eachLine in dataList:	# parse through the the read lines
			if len(eachLine) > 1: # skip empty lines (if they exist)
				x, y = eachLine.split(',')
				if(x.isnumeric()):
					xList.append(float(x))
					yList.append(float(y))

		return xList, yList

	def update_plot(self, currentPlot, xData, yData, xlabel, ylabel, title, settings):
		currentPlot.clear() # clean the graph before adding new data
		currentPlot.set_xlabel(xlabel)
		currentPlot.set_ylabel(ylabel)
		currentPlot.set_title(title)
		currentPlot.plot(xData, yData, settings, picker=5)	#'bo' = blue scatter plot

	def clear_plots(self):	# clear all plots at the start of a new run
		self.plot_dynamic1.clear()
		self.plot_dynamic2.clear()
		self.plot_static1.clear()
		self.plot_static2.clear()

root = App()
root.geometry("1280x720")
root.mainloop()
