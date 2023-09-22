import tkinter
from tkinter import *
from tkinter import ttk
import os

def start():
    os.system("sudo mn --controller=remote,ip=127.0.0.1 --topo=linear," + host_number.get() + " --mac")
def exit():
    topo.destroy()
topo=Tk()
topo.config(bg="white")
topo.title("choose host number for your topology")
topo.geometry("300x100")
host_value = tkinter.StringVar()
list_host=list(range(2,10))
host_number = ttk.Combobox(topo, textvariable=host_value, width=7)
host_number['values'] = list_host
host_number['state'] = 'readonly'
host_number.pack()
click=Button(topo,text="start",width=100,command=start)
click.pack()
click1=Button(topo,text="exit",width=100,command=exit)
click1.pack()
topo.resizable(False,False)
topo.eval('tk::PlaceWindow . center')
topo.mainloop()