''' TODO LIST
	Talk about how inputs will be read
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
num_files = 3
data_file1 = "test_data.txt" # sample test file
timing_file = "timing_data.txt" # file that shows the amount of time elapsed for the a given replay
name_file = "data_names.txt"

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

class PlotManager(object):	# contains logic for subplots

	def __init__(self, parent):	# create the subplots and place within 'graphFig' figure object
		self.parent = parent	# reference to graphPage

		# Plot definitions
		self.plot_dynamic1 = graphFig.add_subplot(2, 2, 1) 		# create a 1x2 plot at subplot 1
		self.plot_dynamic2 = graphFig.add_subplot(2, 2, 2)		# create a 1x2 plot at subplot 2
		self.plot_static1  = graphFig.add_subplot(2, 2, 3)		# dynamic plots update as the files are changed
		self.plot_static2  = graphFig.add_subplot(2, 2, 4)

		''' TODO '''
		# Arrays for graphable data
		self.data_x = []
		self.data_y = []

		# Array for static plots
		self.static_plots = []
		self.static_plots.append(self.plot_static1)
		self.static_plots.append(self.plot_static2)

	def animate(self, i):	# animate graphs
		filesExist = self.check_for_files()

		if(filesExist): # all files exist
			graphFig.tight_layout()	# use tight layout for cleaner display of plot elements

			self.handle_new_data()

			self.update_dynamic_plots()
			# self.update_runTimer(timing_file)

			''' TODO '''
			# get names of data-types
			self.data_names = self.get_name_data("data_names.txt")
			collect1 = graphFig.canvas.mpl_connect('pick_event', self.on_pick)	# allow points to be clicked on the graph
		else:
			self.parent.runTimer.configure(text="Missing Input files...")

	def read_background_files(self):	# continue to read files even when animation is paused
		while(str(self.parent.pause_button['state']) == 'disabled'):
			self.handle_new_data()
			time.sleep(1)	# sleep 1 second

	def handle_new_data(self):	# check for new water levels and update the database
		xData, yData = self.get_plot_data(data_file1)

		self.data_x = list(xData)
		self.data_y = list(yData)

	''' TODO '''
	def update_dynamic_plots(self): 	# update dynamic (animated) plots
		xData, yData = self.get_plot_data(data_file1)
		if(xData and yData):
			self.update_plot(self.plot_dynamic1, xData, yData,
				xlabel='x-data',
				ylabel='y-data',
				title ='Dyamic Plot 1',
				settings='bo')	# bo = blue, circles (scatter-points)

		# xData, yData = retrieve dynamic plot 2 data
		xData, yData = self.get_plot_data(data_file1)
		if(xData and yData):
			self.update_plot(self.plot_dynamic2, xData, yData,
								xlabel='x-data',
							 	ylabel='y-data',
							 	title ='Dynamic plot 2',
			 					settings='r-D')	# r-D = red, diamonds with a line through points '''

	''' TODO '''
	def get_name_data(self, fileName):
		pullData = open(fileName, "r").read()
		dataList = pullData.split('\n')
		nameList = []

		for eachLine in dataList:
			if len(eachLine) > 1:
				nameList.append(str(eachLine))

		return nameList

	def update_static_plot(self, plotNumber, xData, yData): # update static plot
		selected_plot = self.static_plots[int(plotNumber) - 1]

		''' TODO - Adjust x and y-labels to fit the data '''
		self.update_plot(selected_plot, xData, yData,
						 xlabel='X-Data ',
						 ylabel='Y-Data',
						 title='Title Here',
						 settings='go')

		diag_line = selected_plot.plot(	selected_plot.get_xlim(), 	# add a 45 degree line to the plot
									    selected_plot.get_ylim(),
									    ls="--",
									    c="0.1")

	''' TODO - ADD more counters for files '''
	def check_for_files(self):	# check that all input files exist
		fileCounter = 0
		fileCounter += self.check_fileExists(data_file1)
		fileCounter += self.check_fileExists(timing_file)
		fileCounter += self.check_fileExists(name_file)

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

	''' TODO '''
	def update_runTimer(self, fileName):
		if(os.stat(fileName).st_size != 0): # check that the file is not blank
			x_data, y_Data = self.get_plot_data(fileName)
			current_x = str(xData[0])
			current_y = str(yData[0])
			self.parent.runTimer.configure(text='Current X: %s, Current Y: %s ' % (current_x, current_y))

	def on_pick(self, event):	# handle clicks to the graph
		index = event.ind[0]	# get the index of the mouse click
		# use the index into a name array to get the name of a dataset
		# current_name = some_name_array[index]
		# current_x = some_x_array[index]
		# current_y = some_y_array[index]
		# self.parent.pickMessage.configure(text='Data-point name: %s, x: %s, y: %s' % (current_name, current_x, current_y))

root = App()
root.geometry("1280x720")
root.mainloop()
