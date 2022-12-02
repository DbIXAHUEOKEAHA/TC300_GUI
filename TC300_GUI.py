import os
cur_dir = os.getcwd() 
import tkinter as tk
from tkinter import ttk
import pandas as pd
LARGE_FONT = ('Verdana', 12)
from TC300 import TC300
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

class TC300_settings(tk.Frame):

    def __init__(self, parent, controller):
        '''init is the function that runs every time, when Frontend class called
        so here we should initialise all variables that we are going to use'''
        
        self.adress = 'ASRL3::INSTR' #adress of TC300 device

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='TC300 settings', font=LARGE_FONT)
        label.place(relx=0.485, rely=0.02)
        
        self.entry_target1 = tk.Entry(self) #entry box with initial value of self.aux1_initial
        self.entry_target1.place(relx=0.5, rely=0.5)
        
        button_set_target1 = tk.Button(self, text='Set target 1 temperature',
                                        command=self.button_target1_clicked)
        button_set_target1.place(relx=0.6, rely=0.6)
        
        '''
        self.value_t1 = tk.StringVar(value='20.0')
        self.label_value_t1 = tk.Label(self, text=(
            '\n' + self.value_t1.get()), font=('Arial', 16))
        self.label_value_t1.place(relx=0.15, rely=0.3)
        '''

        #python is one-threaded by default, so to make it multi-threaded we need to implement some new features with 'threading' library
        #############################################
        '''creating threads for each process'''

        thread_update_t1 = threading.Thread(
            target=self.update_value_t1())

        #############################################

        '''start every thread'''

        thread_update_t1.start()

        #############################################
        '''join thread into general stream of threads'''

        thread_update_t1.join()

        #############################################
        
    def button_target1_clicked(self):
        TC300().set_T1(self.entry_target1.get())

    def update_value_t1(self, interval=100):
        '''updates label of ch1 in a parallel thread, 
        because thread with this function was initialised before'''
        
        value = TC300().t1()
        self.label_value_t1['text'] = '\n' + str(value)
        self.label_value_t1.after(interval, self.update_value_t1)
    
    
        
def main():
    app = Frontend(TC300_settings)
    app.mainloop()
    while True:
        pass


if __name__ == '__main__':
    main()