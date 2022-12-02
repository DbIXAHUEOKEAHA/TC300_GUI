import os
cur_dir = os.getcwd() 
import tkinter as tk
from tkinter import ttk
import pandas as pd
LARGE_FONT = ('Verdana', 12)
from lock_in import lock_in
import threading

class Frontend(tk.Tk):
    
    '''This is a class that creates window in general'''

    def __init__(self, window, size = '1920x1080', title = 'TC300', *args, **kwargs):
        '''init is the function that runs every time, when Frontend class called
        so here we should initialise all variables that we are going to use'''
        tk.Tk.__init__(self, *args, **kwargs) #initialising tkinter window

        tk.Tk.iconbitmap(self) #window icon is empty, may add some if needed
        tk.Tk.geometry(self, newGeometry = size) #size of window, '1920x1080' by default
        tk.Tk.wm_title(self, title) #window title 'TC300' by default

        container = tk.Frame(self) #window object
        container.pack(side='top', fill='both', expand='True') 
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        frame = window(container, self)
        self.frames[window] = frame
        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(window) #refer to show_frame function below

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() #create window

class TC300(tk.Frame):

    def __init__(self, parent, controller):
        '''init is the function that runs every time, when Frontend class called
        so here we should initialise all variables that we are going to use'''
        
        self.adress = 'ASRL3::INSTR' #adress of TC300 device

        tk.Frame.__init__(self, parent)

        

        #python is one-threaded by default, so to make it multi-threaded we need to implement some new features with 'threading' library
        #############################################
        '''creating threads for each process'''

        #############################################

        '''start every thread'''

        #############################################
        '''join thread into general stream of threads'''

        #############################################

    
        
def main():
    app = Frontend(TC300)
    app.mainloop()
    while True:
        pass


if __name__ == '__main__':
    main()