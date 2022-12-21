import os
cur_dir = os.getcwd() 
import tkinter as tk
from tkinter import ttk
import pandas as pd
from TC300 import TC300
from Z_stage import ZStage
from Rot_stage import RotStage
from csv import writer
LARGE_FONT = ('Verdana', 12)
import threading
import numpy as np
import time
from datetime import datetime
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
                                               NavigationToolbar2Tk)

filename = cur_dir + '\TC300_Config\TC300' + datetime.today().strftime(
    '%H_%M_%d_%m_%Y') + '.csv'

config_parameters = pd.DataFrame(columns=['Time', 'Actual temperature', 'Current CH1', 'Voltage CH1', 'Current CH2', 'Voltage CH2', 'Z position', 'Rotation position'])

config_parameters.to_csv(filename, index=False)

zero_time = time.perf_counter()

sensor_dict = {'1 ': 'PT100', '2 ': 'PT1000', '3 ': 'NTC1', '4 ': 'NTC2', '5 ': 'Thermo C.', 
               '6 ': 'AD590', '7 ': 'EXT1', '8 ': 'EXT2'}

sensor1 = sensor_dict[TC300().type1()]

sensor2 = sensor_dict[TC300().type2()]

P = TC300().PID_P()


I = TC300().PID_I()

D = TC300().PID_D()

cur_index = 0

func_to_run = ''

Z_init = round(float(ZStage().position()), 2)
Theta_init = round(float(RotStage().position()), 2)

def set_default():
    TC300().set_T1(value = float(globals()['GUI'].entry_target.get()))
    TC300().set_CURR2(value = 58.073 + 2.185*float(globals()['GUI'].entry_target.get()))
    TC300().set_PID_P(value = float(globals()['GUI'].entry_P.get()))
    TC300().set_PID_I(value = float(globals()['GUI'].entry_I.get()))
    TC300().set_PID_D(value = float(globals()['GUI'].entry_D.get()))
    TC300().set_ch1(1)
    TC300().set_ch2(1)

def set_ch1():
    TC300().set_ch1(globals()['GUI'].x.get())
    
def set_ch2():
    TC300().set_ch2(globals()['GUI'].y.get())
    
def set_op_mode1():
    TC300().set_op_mode1((int(globals()['GUI'].modechosen1.current()) * 2))

def set_op_mode2():
    TC300().set_op_mode2((int(globals()['GUI'].modechosen2.current()) * 2))

def go_z():
    ZStage().set_speed((float(globals()['GUI'].entry_delta_z.get())))
    ZStage().set_position((float(globals()['GUI'].entry_z.get())))
    
def go_theta():
    RotStage().set_speed((float(globals()['GUI'].entry_delta_theta.get())))
    RotStage().set_position((float(globals()['GUI'].entry_theta.get())))
    
def pause_z():
    ZStage().stop()

def pause_theta():
    RotStage().stop()

def my_animate1(i):
    # function to animate graph on each step
    global ax1
    
    color = 'darkblue'

    columns = pd.read_csv(filename).columns.values
    data = pd.read_csv(filename)
    data = data.tail(len(data) - globals()['cur_index'])        
    t = data[columns[0]].values
    if len(t) == 0:
        t = []
    y = data[columns[1]].values
    if len(y) == 0:
        y = []
    xlabel = ax1.get_xlabel()
    ylabel = ax1.get_ylabel()
    title = ax1.get_title()
    ax1.clear()
    ax1.set_xlabel(xlabel, fontsize = 8)
    ax1.set_ylabel(ylabel, fontsize = 8)
    ax1.tick_params(axis='both', which='major', labelsize=8)
    ax1.set_title(title, fontsize = 8, pad = -5)
    ax1.plot(t, y, '-', color = color, lw = 1)
    #globals()['GUI'].update()
    globals()['GUI'].update_idletasks()
    #return [globals()[f'ax{n}']]
    
def my_animate2(i):
    # function to animate graph on each step
    global ax2
    color = 'Crimson'

    columns = pd.read_csv(filename).columns.values
    data = pd.read_csv(filename)
    data = data.tail(1)        
    theta = data[columns[7]].values
    if len(theta) == 0:
        theta = []
    z = data[columns[6]].values
    if len(z) == 0:
        z = []
    xlabel = ax2.get_xlabel()
    ylabel = ax2.get_ylabel()
    title = ax2.get_title()
    ax2.clear()
    ax2.set_xlabel(xlabel, fontsize = 8)
    ax2.set_ylabel(ylabel, fontsize = 8)
    ax2.tick_params(axis='both', which='major', labelsize=8)
    ax2.set_title(title, fontsize = 8, pad = -5)
    ax2.set_xlim((-17, 17))
    ax2.set_ylim((0, 13))
    ax2.plot(theta, z, 'o', color = color, lw = 1)
    #globals()['GUI'].update()
    globals()['GUI'].update_idletasks()
    #return [globals()[f'ax{n}']]
     
interval = 100

fig1 = Figure(figsize = (2.8, 1.65), dpi=300)
ax1 = fig1.add_subplot(111)
fig1.subplots_adjust(left = 0.25, bottom = 0.25)
ax1.set_xlabel('t, s')
ax1.set_ylabel(r'T, °C')
ax1.set_title('T(t)', fontsize = 8)


fig2 = Figure(figsize = (2.8, 1.65), dpi=300)
ax2 = fig2.add_subplot(111)
fig2.subplots_adjust(left = 0.25, bottom = 0.25)
ax2.set_xlabel(r'θ, deg')
ax2.set_ylabel(r'Z, mm')
ax2.set_title(r'Z(θ)', fontsize = 8)
ax2.set_xlim((-17, 17))
ax2.set_ylim((0, 13))


class write_config_parameters(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        
        global func_to_run
        
        while True:
            dataframe = [round(time.perf_counter() - zero_time, 2)]
            dataframe.append(TC300().T1())
            dataframe.append(TC300().CURR1())
            dataframe.append(TC300().VOLT1())
            dataframe.append(TC300().CURR2())
            dataframe.append(TC300().VOLT2())
            dataframe.append(ZStage().position())
            dataframe.append(RotStage().position())
            
            exec(func_to_run)
            
            func_to_run = ''
            
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
        global GUI
        frame = self.frames[cont]
        frame.tkraise() #create window
        GUI = frame

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

        self.modechosen1 = ttk.Combobox(self, width = 20)
        self.modechosen1['values'] = (' Heater', 
                                  ' Constant Current')
        self.modechosen1.bind("<<ComboboxSelected>>", self.set_op_mode1)
        self.modechosen1.current(0)
        self.modechosen1['state'] = 'disabled'
        self.modechosen1.pack()
        self.modechosen1.place(x=310,y=185)
          


        label_mode2 = tk.Label(self,
                           text="Mode",font=("Arial",10,'bold'))
        label_mode2.pack()
        label_mode2.place(x=710, y=185)

        self.modechosen2 = ttk.Combobox(self, width = 20)
        self.modechosen2['values'] = (' Heater', 
                                  ' Constant Current')
        self.modechosen2.bind("<<ComboboxSelected>>", self.set_op_mode2)
        self.modechosen2.current(1)
        self.modechosen2['state'] = 'disabled'
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
        
        label_Z = tk.Label(self, text = 'Z', font = ('verdana', 16))
        label_Z.place(x = 100, y = 350)
        
        label_theta = tk.Label(self, text = 'Rotation', font = ('verdana', 16))
        label_theta.place(x = 500, y = 350)
        
        self.entry_z = tk.Entry(self)
        self.entry_z.insert(0, str(Z_init))
        self.entry_z.place(x = 100, y = 400)
        
        button_arrow_up = tk.Button(self, text = r'🔼', command = self.arrow_up, font = ('verdana', 5), width = 2)
        button_arrow_up.place(x = 210, y = 395)
        
        button_arrow_down = tk.Button(self, text = r'🔽', command = self.arrow_down, font = ('verdana', 5), width = 2)
        button_arrow_down.place(x = 210, y = 410)
        
        label_delta_z = tk.Label(self, text = r'Δ, mm', font = ('verdana', 14))
        label_delta_z.place(x = 20, y = 445)
        
        self.entry_delta_z = tk.Entry(self)
        self.entry_delta_z.insert(0, '1')
        self.entry_delta_z.place(x = 100, y = 450)
        
        button_go_z = tk.Button(self, text = 'Go', font = ('verdana, 14'), command = self.go_z)
        button_go_z.place(x = 100, y = 500)
        
        self.button_pause_z = tk.Button(self, text = r'⏸️', font = ('verdana', 14), command = lambda: self.pause_z())
        self.button_pause_z.place(x = 150, y = 500)
        
        self.pause_z_status = 0
        
        self.entry_theta = tk.Entry(self)
        self.entry_theta.insert(0, str(Theta_init))
        self.entry_theta.place(x = 500, y = 400)
        
        button_counter_clockwise = tk.Button(self, text = r'🔃', command = self.counter_clockwise, font = ('verdana', 5), width = 2)
        button_counter_clockwise.place(x = 610, y = 395)
        
        button_clockwise = tk.Button(self, text = r'🔄', command = self.clockwise, font = ('verdana', 5), width = 2)
        button_clockwise.place(x = 610, y = 410)
        
        label_delta_theta = tk.Label(self, text = r'Δ, deg', font = ('verdana', 14))
        label_delta_theta.place(x = 400, y = 445)
        
        self.entry_delta_theta = tk.Entry(self)
        self.entry_delta_theta.insert(0, '1')
        self.entry_delta_theta.place(x = 500, y = 450)
        
        button_go_theta = tk.Button(self, text = 'Go', font = ('verdana, 14'), command = self.go_theta)
        button_go_theta.place(x = 500, y = 500)
        
        self.button_pause_theta = tk.Button(self, text = r'⏸️', font = ('verdana', 14), command = lambda: self.pause_theta())
        self.button_pause_theta.place(x = 550, y = 500)
        
        self.pause_theta_status = 0
        
        self.columns = pd.read_csv(filename, sep = ',').columns
        
        self.table_dataframe = ttk.Treeview(self, columns = self.columns, show = 'headings', height = 1)
        self.table_dataframe.place(x = 20, y = 650, width = 8 * 120 + 2)

        self.initial_value = []
        
        for ind, heading in enumerate(self.columns):
            self.table_dataframe.heading(ind, text = heading)
            self.table_dataframe.column(ind,anchor=tk.CENTER, stretch=tk.NO, width=120)
            self.initial_value.append(heading)
                
        self.table_dataframe.insert('', tk.END, 'Current dataframe', text = 'Current dataframe', values = self.initial_value)
        
        self.update_item('Current dataframe')
        
        self.plot1 = FigureCanvasTkAgg(globals()['fig1'], self)
        self.plot1.draw()
        self.plot1.get_tk_widget().place(x = 1000, y=0)
        
        button_clear_graph = tk.Button(self, text = 'Clear', command = self.clear_graph, font = ('Verdana', 16))
        button_clear_graph.place(x = 1000, y = 500)
        
        self.plot2 = FigureCanvasTkAgg(globals()['fig2'], self)
        self.plot2.draw()
        self.plot2.get_tk_widget().place(x = 1000, y=550)
        
        #self.plot3 = FigureCanvasTkAgg(globals()['fig3'], self)
        #self.plot3.draw()
        #self.plot3.get_tk_widget().place(x = 1000, y=500)
        
    def update_item(self, item):
        try:
            dataframe = pd.read_csv(filename).tail(1).values.flatten().round(2)
            self.table_dataframe.item(item, values=tuple(dataframe))
            self.table_dataframe.after(500, self.update_item, item)
        except FileNotFoundError:
            self.table_dataframe.after(500, self.update_item, item)
    
    def click(self):
        global func_to_run
        func_to_run = 'set_default()'
        self.x.set(1)
        self.y.set(1)
        self.update()
        
    def display1(self):
        global func_to_run
        func_to_run = 'set_ch1()'
            
    def display2(self):
        global func_to_run
        func_to_run = 'set_ch2()'
        
    def set_op_mode1(self, event):
        global func_to_run
        func_to_run = 'set_op_mode1()'

    def set_op_mode2(self, event):
        global func_to_run
        func_to_run = 'set_op_mode2()'
        
    def arrow_up(self):
        z = float(self.entry_z.get())
        delta = float(self.entry_delta_z.get())
        if (z >= 1 + delta and z <= 11.8 - delta) or z - 1 <= delta:
            self.entry_z.delete(0, tk.END)
            self.entry_z.insert(0, z + delta)
            self.go_z()
        
    def arrow_down(self):
        z = float(self.entry_z.get())
        delta = float(self.entry_delta_z.get())
        if (z >= 1 + delta and z <= 11.8 - delta) or z - 11.8 >= - delta:
            self.entry_z.delete(0, tk.END)
            self.entry_z.insert(0, z - delta)
            self.go_z()
            
    def clockwise(self):
        theta = float(self.entry_theta.get())
        delta = float(self.entry_delta_theta.get())
        if (theta >= -15 + delta and theta <= 15 - delta) or theta - (-15) <= delta:
            self.entry_theta.delete(0, tk.END)
            self.entry_theta.insert(0, theta - delta)
            self.go_theta()
        
    def counter_clockwise(self):
        theta = float(self.entry_theta.get())
        delta = float(self.entry_delta_theta.get())
        if (theta >= -15 + delta and theta <= 15 - delta) or theta - (-15) <= delta:
            self.entry_theta.delete(0, tk.END)
            self.entry_theta.insert(0, theta + delta)
            self.go_theta()
        
    def go_z(self):
        global func_to_run
        func_to_run = 'go_z()'
        
    def go_theta(self):
        global func_to_run
        func_to_run = 'go_theta()'
        
    def pause_z(self):
        global func_to_run
        if self.pause_z_status == 0:
            self.button_pause_z.config(text = r'▶️')
            self.pause_z_status = 1
            func_to_run = 'pause_z()'
        elif self.pause_z_status == 1:
            self.button_pause_z.config(text = r'⏸️')
            self.pause_z_status = 0
            func_to_run = 'go_z()'
        else:
            pass
        
    def pause_theta(self):
        global func_to_run
        if self.pause_theta_status == 0:
            self.button_pause_theta.delete(0, tk.END)
            self.button_pause_theta.config(text = r'▶️')
            self.pause_theta_status = 1
            func_to_run = 'pause_theta()'
        elif self.pause_theta_status == 1:
            self.button_pause_theta.config(text = r'⏸️')
            self.pause_theta_status = 0
            func_to_run = 'go_theta()'
        else:
            pass
        
    def clear_graph(self):
        global cur_index
        global filename
        
        cur_index = len(pd.read_csv(filename))
        
        print(f'Current index is {cur_index}')
        
def main():
    write_config_parameters()
    app = Frontend(TC300_GUI)
    ani1 = animation.FuncAnimation(
        fig = fig1, func = lambda x: my_animate1(x), interval=interval, blit = False)
    ani2 = animation.FuncAnimation(
        fig = fig2, func = lambda x: my_animate2(x), interval=interval, blit = False)
    app.mainloop()
    while True:
        pass


if __name__ == '__main__':
    main()