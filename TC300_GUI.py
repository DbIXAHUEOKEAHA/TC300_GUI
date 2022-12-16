import os
cur_dir = os.getcwd() 
import tkinter as tk
from tkinter import ttk
import pandas as pd
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
import matplotlib.pyplot as plt
from matplotlib import style
import re
import pyvisa as visa
from pyvisa import constants

rm = visa.ResourceManager()

# Write command to a device and get it's output
def get(device, command):
    '''device = rm.open_resource() where this function gets all devices initiaals such as adress, baud_rate, data_bits and so on; 
    command = string Standart Commands for Programmable Instruments (SCPI)'''
    return device.query(command)
    #return np.random.random(1)

class TC300():

    def __init__(self, adress='ASRL4::INSTR'):
        
        self.adress = adress
        
        self.open()
        
        #self.tc = 0

        self.set_options = {'T1', 'T2', 'VMAX1', 'VMAX2', 'CURR1', 'CURR2'}

        self.get_options = {'T1', 'T2', 'VOLT1', 'VOLT2', 'CURR1', 'CURR2'}
        
        self.operation_mode_dict = {'0 ': 'Heater', '1 ': ' ', '2 ': 'Current'}
       
    def open(self):
        self.tc = rm.open_resource(self.adress, baud_rate=115200,
                                   data_bits=8, parity=constants.VI_ASRL_PAR_NONE,
                                   stop_bits=constants.VI_ASRL_STOP_ONE,
                                   flow_control=constants.VI_ASRL_FLOW_NONE,
                                   write_termination='\r', read_termination='\r')
    
    def IDN(self):
        return(get(self.tc, 'IDN?')[2:])
    
    def set_ch1(self, value):
        #Set Channel 1 status (0=Disable; 1=Enable).
        self.tc.write('EN1=' + str(value))
        
    def set_ch2(self, value):
        #Set Channel 2 status (0=Disable; 1=Enable).
        self.tc.write('EN2=' + str(value))

    def T1(self):
        # Get the CH1 target temperature; returned value is the actual temperature in °C
        value_str = get(self.tc, 'TACT1?')
        self.close()
        if value_str == '':
            self.open()
            value_str = get(self.tc, 'TACT1?')
            self.close()
        value_float = re.findall(r'\d*\.\d+|\d+', value_str)
        value_float = [float(i) for i in value_float]
        return(value_float[0])
    
    def VOLT1(self):
        #Get the CH1 Output Voltage value, with a range of 0.1 to 24.0 V 
        #and a resolution of 0.1V.
        value = get(self.tc, 'VOLT1?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)
    
    def VOLT2(self):
        #Get the CH2 Output Voltage value, with a range of 0.1 to 24.0 V 
        #and a resolution of 0.1V.
        value = get(self.tc, 'VOLT2?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)
    
    def CURR1(self):
        #Get the CH1 Actual Output Current Value, the range is -2000 to +2000 mA,
        #with a resolution of 1mA.
        value = get(self.tc, 'CURR1?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)
    
    def CURR2(self):
        #Get the CH1 Actual Output Current Value, the range is -2000 to +2000 mA,
        #with a resolution of 1mA.
        value = get(self.tc, 'CURR2?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)
    
    def set_VMAX1(self, value):
        #Set the CH1 Output Voltage Max value to value V 
        #(value ranges from 0.1 to 24, corresponding to 0.1 to 24.0 V).
        self.tc.write('VMAX1=' + str(int(value) * 10))
        self.close()
        
    def set_VMAX2(self, value):
        #Set the CH2 Output Voltage Max value to value V 
        #(value ranges from 0.1 to 24, corresponding to 0.1 to 24.0 V).
        self.tc.write('VMAX2=' + str(int(value) * 10))
        self.close()
        
    def set_CURR1(self, value):
        #Set the CH1 output current value, 
        #range is -2000 to +2000 mA, resolution of 1 mA.
        self.tc.write('CURR1=' + str(int(value)))
        self.close()
        
    def set_CURR2(self, value):
        #Set the CH2 output current value, 
        #range is -2000 to +2000 mA, resolution of 1 mA.
        self.tc.write('CURR2=' + str(int(value)))
        self.close()

    def set_T1(self, value=20):
        # Set the CH1 target temperature to value °C, the range is defined by
        # TMIN1 and TMAX1, the setting resolution of value is 1.
        #self.tc.write('EN1=1')
        self.tc.write('TSET1=' + str(int(value * 10)))
        self.close()

    def set_T1_MIN(self, t1_from=0):
        # Set the CH1 Target Temperature Min value,
        # (Range: -200 to TMAX1°C, with a resolution of 1°C).
        self.tc.write('TMIN1=' + str(t1_from))
        self.close()

    def set_T1_MAX(self, t1_to=30):
        # Set the CH1 Target Temperature Max value, n equals value
        # TMIN1 to 400°C, with a resolution of 1°C).
        self.tc.write('T1MAX=' + str(t1_to))
        self.close()

    def T2(self):
        # Get the CH2 target temperature; returned value is the actual temperature in °C
        value_str = get(self.tc, 'TACT2?')
        self.close()
        if value_str == '':
            self.open()
            value_str = get(self.tc, 'TACT2?')
            self.close()
        value_float = re.findall(r'\d*\.\d+|\d+', value_str)
        value_float = [float(i) for i in value_float]
        return(value_float[0])

    def set_T2(self, value=20):
        # Set the CH2 target temperature to value °C, the range is defined by
        # TMIN1 and TMAX1, the setting resolution of value is 1.
        #self.tc.write('EN2=1')
        self.tc.write('TSET2=' + str(int(value * 10)))
        self.close()

    def set_T2_MIN(self, t2_from=0):
        # Set the CH2 Target Temperature Min value,
        # (Range: -200 to TMAX2°C, with a resolution of 1°C).
        self.tc.write('TMIN1=' + str(t2_from))
        self.close()

    def set_T2_MAX(self, t2_to=20):
        # Set the CH2 Target Temperature Max value, n equals value
        # TMIN1 to 400°C, with a resolution of 1°C).
        self.tc.write('T1MAX=' + str(t2_to))
        self.close()
    
    def set_PID_P(self, value = 1.9):
        #Set CH1 P share parameter (Gain of P) to value, 
        #the range of value is 0 to 9.99 with a resolution of 0.01.
        self.tc.write('KP1=' + str(int(value * 100)))
        self.close()
        
    def set_PID_I(self, value = 0.01):
        #Set CH1 I share parameter (Gain of P) to value, 
        #the range of value is 0 to 9.99 with a resolution of 0.01.
        self.tc.write('TI1=' + str(int(value * 100)))
        self.close()
        
    def set_PID_D(self, value = 2.4):
        #Set CH1 D share parameter (Gain of P) to value, 
        #the range of value is 0 to 9.99 with a resolution of 0.01.
        self.tc.write('TD1=' + str(int(value * 100)))
        self.close()
        
    def PID_P(self):
        #Get CH1 P parameter
        value = get(self.tc, 'KP1?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)
    
    def PID_I(self):
        #Get CH1 I parameter
        value = get(self.tc, 'TI1?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)
    
    def PID_D(self):
        #Get CH1 D parameter
        value = get(self.tc, 'TD1?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)
        
    def type1(self):
        #Get CH1 sensor type
        value = get(self.tc, 'TYPE1?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)
    
    def type2(self):
        #Get CH2 sensor type
        value = get(self.tc, 'TYPE2?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(value)

    def op_mode1(self):
        #Get CH1 operation mode
        value = get(self.tc, 'MOD1?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(self.operation_mode_dict[value])
    
    def op_mode2(self):
        #Get CH1 operation mode
        value = get(self.tc, 'MOD2?')
        self.close()
        if value.startswith('\n'):
            value = value[2::]
        return(self.operation_mode_dict[value])
    
    def set_op_mode1(self, value):
        #Set CH1 operation mode
        self.tc.write('MOD1=' + str(value))
        self.close()
    
    def set_op_mode2(self, value):
        #Set CH2 operation mode
        self.tc.write('MOD2=' + str(value))
        self.close()
    
    def close(self):
        self.tc.close()
        


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

t0 = 0

def my_animate(i = 0, n = 1):
    # function to animate graph on each step
    global t0
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
    if len(t) == 0:
        t = [0]
    y = data[columns[n]].values
    if len(y) == 0:
        y = [0]
    print(f't = {t}\ny = {y}')
    #globals()[f'ax{n}'].set_xlim((t0, np.max(t)))
    globals()[f'ax{n}'].plot(t, y, '-', color = color, lw = 1)
    globals()['GUI'].update()
    globals()['GUI'].update_idletasks()
    return [globals()[f'ax{n}']]
    
    
ax_dict = {1: 'T, °C', 2: 'I, mA', 3: 'V, V'}
    
interval = 100

def create_fig(i, figsize, pad = 0, tick_size = 4, label_size = 6, x_pad =0, y_pad = 1, title_size = 8, title_pad = -5):
        globals()[f'fig{i}'] = Figure(figsize, dpi=300)
        globals()[f'ax{i}'] = globals()[f'fig{i}'].add_subplot(111)
        globals()[f'ax{i}'].autoscale(enable = False, axis = 'x')
        globals()[f'ax{i}'].set_xlabel('t, s')
        globals()[f'ax{i}'].set_ylabel(ax_dict[i])
        globals()[f'ax{i}'].set_title(f'{ax_dict[i][0]}(t)', fontsize = 8)
        globals()[f'animation{i}'] = animation.FuncAnimation(
            fig = globals()[f'fig{i}'], func = lambda x: my_animate(x, n = i), interval=interval, blit = False)
        
for i in range(1, 4):
    create_fig(i, figsize = (2.8, 1.65))

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
        
        globals()['GUI'] = self
        
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
        self.plot1.get_tk_widget().place(x = 1000, y=0)
        
        self.plot2 = FigureCanvasTkAgg(globals()['fig2'], self)
        self.plot2.draw()
        self.plot2.get_tk_widget().place(x = 100, y=500)
        
        self.plot3 = FigureCanvasTkAgg(globals()['fig3'], self)
        self.plot3.draw()
        self.plot3.get_tk_widget().place(x = 1000, y=500)
        
    def update_item(self, item):
        try:
            dataframe = pd.read_csv(filename).tail(1).values.flatten().round(2)
            self.table_dataframe.item(item, values=tuple(dataframe))
            self.table_dataframe.after(500, self.update_item, item)
        except FileNotFoundError:
            self.table_dataframe.after(500, self.update_item, item)
    
    def click(self):
         
        time.sleep(0.025)
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
         
        time.sleep(0.025)
        TC300().set_ch1(self.x.get())
            
            
    def display2(self):
         
        time.sleep(0.025)
        TC300().set_ch2(self.y.get())
        
    def set_op_mode1(self, event):
        if self.modechosen1.current() == 0:
            time.sleep(0.025)
            TC300().set_op_mode1(0)
        if self.modechosen1.current() == 1:
            time.sleep(0.025)
            TC300().set_op_mode1(2)
            
    def set_op_mode2(self, event):
        if self.modechosen2.current() == 0:
            time.sleep(0.025)
            TC300().set_op_mode2(0)
        if self.modechosen2.current() == 1:
            time.sleep(0.025)
            TC300().set_op_mode2(2)
        
def main():
    write_config_parameters()
    app = Frontend(TC300_GUI)
    app.mainloop()
    while True:
        pass


if __name__ == '__main__':
    main()