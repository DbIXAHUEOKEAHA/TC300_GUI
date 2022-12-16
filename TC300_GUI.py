import os
cur_dir = os.getcwd() 
import tkinter as tk
from tkinter import ttk
import pandas as pd
from csv import writer
LARGE_FONT = ('Verdana', 12)
from TC300 import TC300
import threading
import numpy as np
import time
from datetime import datetime
import matplotlib.animation as animation
#import blit_animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
                                               NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib import style

filename = cur_dir + '\TC300_Config\TC300' + datetime.today().strftime(
    '%H_%M_%d_%m_%Y') + '.csv'

config_parameters = pd.DataFrame(columns=['Time', 'Actual temperature', 'Current CH1', 'Voltage CH1', 'Current CH2', 'Voltage CH2'])

config_parameters.to_csv(filename, index=False)

zero_time = time.perf_counter()

sensor_dict = {'1 ': 'PT100', '2 ': 'PT1000', '3 ': 'NTC1', '4 ': 'NTC2', '5 ': 'Thermo C.', 
               '6 ': 'AD590', '7 ': 'EXT1', '8 ': 'EXT2'}

sensor1 = sensor_dict[TC300().type1()]

time.sleep(0.025)

sensor2 = sensor_dict[TC300().type2()]

time.sleep(0.025)

P = TC300().PID_P()

time.sleep(0.025)

I = TC300().PID_I()

time.sleep(0.025)

D = TC300().PID_D()

time.sleep(0.025)

def my_animate(i = 0, n = 1):
    # function to animate graph on each step
    
    if n%3 == 1:
        color = 'darkblue'
    elif n%3 == 2:
        color = 'darkgreen'
    elif n%3 == 0:
        color = 'crimson'
    else:
        color = 'black'

    columns = pd.read_csv(filename).columns.values
    data = pd.read_csv(filename)
    t = data[columns[0]].values
    y = data[columns[n]].values
    
ax_dict = {1: 'T, °C', 2: 'I, mA', 3: 'V, V'}
    
def create_fig(i, figsize, pad = 0, tick_size = 4, label_size = 6, x_pad =0, y_pad = 1, title_size = 8, title_pad = -5):
        globals()[f'fig{i}'] = Figure(figsize, dpi=300)
        globals()[f'ax{i}'] = globals()[f'fig{i}'].add_subplot(111)
        globals()[f'ax{i}'].set_xlabel('t, s')
        globals()[f'ax{i}'].set_ylabel(ax_dict[i])
        globals()[f'ani{i}'] = StartAnimation
        globals()[f'ani{i}'].start()
        
for i in range(1, 4):
    create_fig(i, figsize = (200, 100))

interval = 100

class StartAnimation:
    
    def start(i):
        globals()[f'animation{i}'] = animation.FuncAnimation(
            fig = globals()[f'fig{i}'], func = lambda x: my_animate(x, n = i), interval=interval, blit = False)


class write_config_parameters(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            dataframe = [round(time.perf_counter() - zero_time, 2)]
            dataframe.append(TC300().T1())
            time.sleep(0.025)
            dataframe.append(TC300().CURR1())
            time.sleep(0.025)
            dataframe.append(TC300().VOLT1())
            time.sleep(0.025)
            dataframe.append(TC300().CURR2())
            time.sleep(0.025)
            dataframe.append(TC300().VOLT2())
            
            with open(filename, 'a') as f_object:
                try:
                    # Pass this file object to csv.writer()
                    # and get a writer object
                    writer_object = writer(f_object)

                    # Pass the list as an argument into
                    # the writerow()
                    writer_object.writerow(dataframe)
                    time.sleep(0.1)

                    # Close the file object
                    f_object.close()
                except KeyboardInterrupt:
                    f_object.close()

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

class TC300_GUI(tk.Frame):

    def __init__(self, parent, controller):
        '''init is the function that runs every time, when Frontend class called
        so here we should initialise all variables that we are going to use'''
        
        self.adress = 'ASRL3::INSTR' #adress of TC300 device

        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self,
                          text="MENU", 
                          font=("Times New Romen",20, 'bold'),
                          foreground='black'
                          )
        label1.pack()
        label1.place(x=480, y=20)
        #Framework



        button_start = tk.Button(self,
                           text="Set",font=("Times New Romen",10,'bold'),
                           command=self.click,
                           width=6,height=2,
                           bg="light gray",fg="black",
                           relief='raised',bd=5
                           )
        button_start.pack()
        button_start.place(x=800, y=80)
        #Start button



        label_target_temperature = tk.Label(self,
                           text="Target Temperature",font=("Arial",15,'bold'))
        self.entry_target = tk.Entry(self,
                          font=("Arial",12))
        self.entry_target.insert(0, '50')
        label_target_temperature.pack()
        self.entry_target.pack()
        label_target_temperature.place(x=200, y=70)
        self.entry_target.place(x=450, y=70)
        label_degree1 = tk.Label(self,text="\N{DEGREE CELSIUS}",font=("Arial",10,'bold'))
        label_degree1.pack()
        label_degree1.place(x=680,y=74)

        label_CH1 = tk.Label(self,
                           text="CH1",font=("Arial",20,'bold'))
        label_CH1.pack()
        label_CH1.place(x=100, y=180)

        label_CH2 = tk.Label(self,
                           text="CH2",font=("Arial",20,'bold'))
        label_CH2.pack()
        label_CH2.place(x=550, y=180)
        #Channel 1&2

        label_P = tk.Label(self,
                           text="P",font=("Arial",15,'bold'))
        self.entry_P = tk.Entry(self,
                          font=("Arial",12),
                          width=6)
        self.entry_P.insert(0, P)
        label_P.pack()
        self.entry_P.pack()
        label_P.place(x=320, y=130)
        self.entry_P.place(x=345, y=135)

        label_I = tk.Label(self,
                           text="I",font=("Arial",15,'bold'))
        self.entry_I = tk.Entry(self,
                          font=("Arial",12),
                          width=6)
        self.entry_I.insert(0, I)
        label_I.pack()
        self.entry_I.pack()
        label_I.place(x=450, y=130)
        self.entry_I.place(x=475, y=135)

        label_D = tk.Label(self,
                           text="D",font=("Arial",15,'bold'))
        self.entry_D = tk.Entry(self,
                          font=("Arial",12),
                          width=6)
        self.entry_D.insert(0, D)
        label_D.pack()
        self.entry_D.pack()
        label_D.place(x=580, y=130)
        self.entry_D.place(x=605, y=135)


        label_PID = tk.Label(self,
                           text="PID",font=("Arial",15,'bold'))
        label_PID.pack()
        label_PID.place(x=220, y=130)
        #PID coefficient

            
        self.x = tk.IntVar()
        self.y = tk.IntVar()

        check_button1 = tk.Checkbutton(self,
                                      text="On",
                                      variable=self.x,
                                      onvalue=1,
                                      offvalue=0,
                                      command=self.display1,
                                      font=('Arial',15),
                                      fg='red',
                                      bg='black',
                                      )
        check_button1.pack()
        check_button1.place(x=180,y=180)

        check_button2 = tk.Checkbutton(self,
                                      text="On",
                                      variable=self.y,
                                      onvalue=1,
                                      offvalue=0,
                                      command=self.display2,
                                      font=('Arial',15),
                                      fg='red',
                                      bg='black',
                                      )
        check_button2.pack()
        check_button2.place(x=630,y=180)
        #Switch of channel



        label_mode1 = tk.Label(self,
                           text="Mode",font=("Arial",10,'bold'))
        label_mode1.pack()
        label_mode1.place(x=260, y=185)

        self.modechosen1 = ttk.Combobox(self, width = 15)
        self.modechosen1['values'] = (' Heater', 
                                  ' Constant Current')
        self.modechosen1.bind("<<ComboboxSelected>>", self.set_op_mode1)
        self.modechosen1.current(0)
        self.modechosen1.pack()
        self.modechosen1.place(x=310,y=185)
          


        label_mode2 = tk.Label(self,
                           text="Mode",font=("Arial",10,'bold'))
        label_mode2.pack()
        label_mode2.place(x=710, y=185)

        self.modechosen2 = ttk.Combobox(self, width = 15)
        self.modechosen2['values'] = (' Heater', 
                                  ' Constant Current')
        self.modechosen2.bind("<<ComboboxSelected>>", self.set_op_mode2)
        self.modechosen2.current(1)
        self.modechosen2.pack()
        self.modechosen2.place(x=760,y=185)
        #Modechosen combobox

        label_sensortype1 = tk.Label(self,
                           text="Sensor type",font=("Arial",15,'bold'))
        label_sensortype1.pack()
        label_sensortype1.place(x=100, y=250)
        
        label_sensortype1_actual = tk.Label(self, text = sensor1, 
                                            font=("Arial",15,'bold'))
        label_sensortype1_actual.place(x = 250, y = 250)

        label_sensortype2 = tk.Label(self,
                           text="Sensor type",font=("Arial",15,'bold'))
        label_sensortype2.pack()
        label_sensortype2.place(x=550, y=250)
        
        label_sensortype2_actual = tk.Label(self, text = sensor2, 
                                            font=("Arial",15,'bold'))
        label_sensortype2_actual.place(x = 700, y = 250)
        
        self.columns = pd.read_csv(filename, sep = ',')
        
        self.table_dataframe = ttk.Treeview(self, columns = self.columns, show = 'headings', height = 1)
        self.table_dataframe.place(x = 100, y = 350, width = 6 * 120 + 2)

        self.initial_value = []
        
        for ind, heading in enumerate(self.columns):
            self.table_dataframe.heading(ind, text = heading)
            self.table_dataframe.column(ind,anchor=tk.CENTER, stretch=tk.NO, width=120)
            self.initial_value.append(heading)
                
        self.table_dataframe.insert('', tk.END, 'Current dataframe', text = 'Current dataframe', values = self.initial_value)
        
        self.update_item('Current dataframe')
        
        self.plot1 = FigureCanvasTkAgg(globals()['fig1'], self)
        self.plot1.draw()
        globals()[f'self.plot{self.order}'].get_tk_widget().place(relx=0, rely=0)
        
    def update_item(self, item):
        my_animate()
        try:
            dataframe = pd.read_csv(filename).tail(1).values.flatten().round(2)
            self.table_dataframe.item(item, values=tuple(dataframe))
            self.table_dataframe.after(500, self.update_item, item)
        except FileNotFoundError:
            self.table_dataframe.after(500, self.update_item, item)
    
    def click(self):
        TC300().set_T1(value = float(self.entry_target.get()))
        time.sleep(0.025)
        TC300().set_CURR2(value = 58.073 + 2.185*float(self.entry_target.get()))
        time.sleep(0.025)
        TC300().set_PID_P(value = float(self.entry_P.get()))
        time.sleep(0.025)
        TC300().set_PID_I(value = float(self.entry_I.get()))
        time.sleep(0.025)
        TC300().set_PID_D(value = float(self.entry_D.get()))
        time.sleep(0.025)
    
    def display1(self):
        TC300().set_ch1(self.x.get())
            
            
    def display2(self):
        TC300().set_ch2(self.y.get())
        
    def set_op_mode1(self, event):
        if self.modechosen1.current() == 0:
            TC300().set_op_mode1(0)
        if self.modechosen1.current() == 1:
            TC300().set_op_mode1(2)
            
    def set_op_mode2(self, event):
        if self.modechosen2.current() == 0:
            TC300().set_op_mode2(0)
        if self.modechosen2.current() == 1:
            TC300().set_op_mode2(2)
        
def main():
    write_config_parameters()
    app = Frontend(TC300_GUI)
    app.mainloop()
    while True:
        pass


if __name__ == '__main__':
    main()