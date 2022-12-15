# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import threading

def click():
    print("Begin heating")
    
def submit():
    print("")

def get_random():
    return round(np.random.random(1)[0], 2)

window = tk.Tk()
window.title("TC300")
window.resizable(width=False, height=False)
frm_entry = tk.Frame(master=window)
lbl_temp = tk.Label(master=frm_entry, text="TC300 MENU")

frame1 = tk.Frame(master=window, width=1000, height=600)
frame1.pack()

label1 = tk.Label(window,
                  text="MENU", 
                  font=("Times New Romen",20, 'bold'),
                  foreground='black'
                  )
label1.pack()
label1.place(x=480, y=0)
#Framework



button = tk.Button(window,
                   text="start",font=("Times New Romen",10,'bold'),
                   command=click,
                   width=6,height=2,
                   bg="light gray",fg="black",
                   relief='raised',bd=5
                   )
button.pack()
button.place(x=800, y=80)
#Start button



label2 = tk.Label(window,
                   text="Target Temperature",font=("Arial",15,'bold'))
entry1 = tk.Entry(window,
                  font=("Arial",12))
label2.pack()
entry1.pack()
label2.place(x=200, y=50)
entry1.place(x=450, y=50)
label18 = tk.Label(window,text="\N{DEGREE CELSIUS}",font=("Arial",10,'bold'))
label18.pack()
label18.place(x=680,y=54)

label3 = tk.Label(window,
                   text="Actual Temperature",font=("Arial",15,'bold'))
label3.pack()
label3.place(x=200, y=90)

label_actual_temperature = tk.Label(window, text = '0.00',
                  font=("Arial",12))

label_actual_temperature.place(x=450, y=90)

def update_label_actual_temperature(interval = 1000):
    label_actual_temperature['text'] = str(get_random())
    label_actual_temperature.after(interval, update_label_actual_temperature)
    
label19 = tk.Label(window,text="\N{DEGREE CELSIUS}",font=("Arial",10,'bold'))
label19.pack()
label19.place(x=680,y=90)
#Two kinds of temperature

label4 = tk.Label(window,
                   text="CH1",font=("Arial",20,'bold'))
label4.pack()
label4.place(x=100, y=180)

label5 = tk.Label(window,
                   text="CH2",font=("Arial",20,'bold'))
label5.pack()
label5.place(x=550, y=180)
#Channel 1&2



label6 = tk.Label(window,
                   text="P",font=("Arial",15,'bold'))
entry3 = tk.Entry(window,
                  font=("Arial",12),
                  width=6)
label6.pack()
entry3.pack()
label6.place(x=320, y=130)
entry3.place(x=345, y=135)

label7 = tk.Label(window,
                   text="I",font=("Arial",15,'bold'))
entry4 = tk.Entry(window,
                  font=("Arial",12),
                  width=6)
label7.pack()
entry4.pack()
label7.place(x=450, y=130)
entry4.place(x=475, y=135)

label8 = tk.Label(window,
                   text="D",font=("Arial",15,'bold'))
entry5 = tk.Entry(window,
                  font=("Arial",12),
                  width=6)
label8.pack()
entry5.pack()
label8.place(x=580, y=130)
entry5.place(x=605, y=135)


label9 = tk.Label(window,
                   text="PID",font=("Arial",15,'bold'))
label9.pack()
label9.place(x=220, y=130)
#PID coefficient



def display1():
    if(x.get()==1):
        print("CH1 on")
    else:
        print("CH1 off")
        
def display2():
    if(y.get()==1):
        print("CH2 on")
    else:
        print("CH2 off")
    
x = tk.IntVar()
y = tk.IntVar()

check_button1 = tk.Checkbutton(window,
                              text="On",
                              variable=x,
                              onvalue=1,
                              offvalue=0,
                              command=display1,
                              font=('Arial',15),
                              fg='red',
                              bg='black',
                              )
check_button1.pack()
check_button1.place(x=180,y=180)

check_button2 = tk.Checkbutton(window,
                              text="On",
                              variable=y,
                              onvalue=1,
                              offvalue=0,
                              command=display2,
                              font=('Arial',15),
                              fg='red',
                              bg='black',
                              )
check_button2.pack()
check_button2.place(x=630,y=180)
#Switch of channel



label10 = tk.Label(window,
                   text="Mode",font=("Arial",10,'bold'))
label10.pack()
label10.place(x=260, y=185)

modechosen1 = ttk.Combobox(window, width = 15)
modechosen1['values'] = (' Heater', 
                          ' Constant Current')
modechosen1.set('')
modechosen1.pack()
modechosen1.place(x=310,y=185)
  


label11 = tk.Label(window,
                   text="Mode",font=("Arial",10,'bold'))
label11.pack()
label11.place(x=710, y=185)

modechosen2 = ttk.Combobox(window, width = 15)
modechosen2['values'] = (' Heater', 
                          ' Constant Current')
modechosen2.set('')
modechosen2.pack()
modechosen2.place(x=760,y=185)
#Modechosen combobox


label12 = tk.Label(window,
                   text="Applied current",font=("Arial",15,'bold'))
label12.pack()
label12.place(x=100, y=250)
#applied current for CH1

label14 = tk.Label(window,
                   text="Applied voltage",font=("Arial",15,'bold'))
label14.pack()
label14.place(x=100, y=300)
#applied voltage for CH1

label16 = tk.Label(window,
                   text="Sensor type",font=("Arial",15,'bold'))
label16.pack()
label16.place(x=100, y=350)




label13 = tk.Label(window,
                   text="Applied current",font=("Arial",15,'bold'))
label13.pack()
label13.place(x=550, y=250)
#applied current for CH2

label15 = tk.Label(window,
                   text="Applied voltage",font=("Arial",15,'bold'))
label15.pack()
label15.place(x=550, y=300)
#applied voltage for CH2

label17 = tk.Label(window,
                   text="Sensor type",font=("Arial",15,'bold'))
label17.pack()
label17.place(x=550, y=350)

thread_update_actual_temperature = threading.Thread(target = update_label_actual_temperature, daemon = True)

thread_update_actual_temperature.start()

window.mainloop()

thread_update_actual_temperature.join()