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

filename = cur_dir + '\config\TC300' + datetime.today().strftime(
    '%H_%M_%d_%m_%Y') + '.csv'

config_parameters = pd.DataFrame(columns=['Time', 'Target temperature', 'Current CH1', 'Voltage CH1', 'Current CH2', 'Voltage CH2'])

config_parameters.to_csv(filename, index=False)

zero_time = time.perf_counter()

sensor_dict = {'1 ': 'PT100', '2 ': 'PT1000', '3 ': 'NTC1', '4 ': 'NTC2', '5 ': 'Thermo C.', 
               '6 ': 'AD590', '7 ': 'EXT1', '8 ': 'EXT2'}

sensor1 = sensor_dict[TC300().type1()]

time.sleep(0.025)

sensor2 = sensor_dict[TC300().type2()]

time.sleep(0.025)

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
                           text="start",font=("Times New Romen",10,'bold'),
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
        entry1 = tk.Entry(self,
                          font=("Arial",12))
        label_target_temperature.pack()
        entry1.pack()
        label_target_temperature.place(x=200, y=70)
        entry1.place(x=450, y=70)
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
        entry3 = tk.Entry(self,
                          font=("Arial",12),
                          width=6)
        label_P.pack()
        entry3.pack()
        label_P.place(x=320, y=130)
        entry3.place(x=345, y=135)

        label_I = tk.Label(self,
                           text="I",font=("Arial",15,'bold'))
        entry4 = tk.Entry(self,
                          font=("Arial",12),
                          width=6)
        label_I.pack()
        entry4.pack()
        label_I.place(x=450, y=130)
        entry4.place(x=475, y=135)

        label_D = tk.Label(self,
                           text="D",font=("Arial",15,'bold'))
        entry5 = tk.Entry(self,
                          font=("Arial",12),
                          width=6)
        label_D.pack()
        entry5.pack()
        label_D.place(x=580, y=130)
        entry5.place(x=605, y=135)


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

        modechosen1 = ttk.Combobox(self, width = 15)
        modechosen1['values'] = (' Heater', 
                                  ' Constant Current')
        modechosen1.set('')
        modechosen1.pack()
        modechosen1.place(x=310,y=185)
          


        label_mode2 = tk.Label(self,
                           text="Mode",font=("Arial",10,'bold'))
        label_mode2.pack()
        label_mode2.place(x=710, y=185)

        modechosen2 = ttk.Combobox(self, width = 15)
        modechosen2['values'] = (' Heater', 
                                  ' Constant Current')
        modechosen2.set('')
        modechosen2.pack()
        modechosen2.place(x=760,y=185)
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
        
    def update_item(self, item):
        try:
            dataframe = pd.read_csv(filename).tail(1).values.flatten().round(2)
            self.table_dataframe.item(item, values=tuple(dataframe))
            self.table_dataframe.after(500, self.update_item, item)
        except FileNotFoundError:
            self.table_dataframe.after(500, self.update_item, item)
    
    def click(self):
        print("Begin heating")
    
    def get_random(self):
        return round(np.random.random(1)[0], 2)
    
    def display1(self):
        if(self.x.get()==1):
            print("CH1 on")
        else:
            print("CH1 off")
            
    def display2(self):
        if(self.y.get()==1):
            print("CH2 on")
        else:
            print("CH2 off")
        
def main():
    write_config_parameters()
    app = Frontend(TC300_GUI)
    app.mainloop()
    while True:
        pass


if __name__ == '__main__':
    main()