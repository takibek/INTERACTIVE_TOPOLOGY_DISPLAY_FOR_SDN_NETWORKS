from tkinter import *
import tkinter as tk
from mininet.topo import Topo
from mininet.net import Mininet
from tkinter import ttk
import request
import matplotlib.pyplot as plt
from PIL import Image
from PIL import Image, ImageTk
import subprocess
import  threading
import secrets
master = Tk()
master.config(bg="white")
master.title("linear Topology")
master.geometry("1400x1400")
frame = Frame(master)
frame.pack(side="top", expand=True, fill="both")
frame = Frame(master)
frame.pack(side="top", expand=True, fill="both")
w = tk.Canvas(master, width=1400, height=1400, bg="white")
w.pack()
def clear_frame():
   for widgets in frame.winfo_children():
      widgets.destroy()

def create():
    def line(x1, y1, x2, y2, color):
        print(x1, y1, x2, y2)
        w.create_line(x1, y1, x2, y2, fill=color)

    full_labesl = {}

    labels = []
    for i in range(99):
        l = Button(master, bg="white", border=0, highlightthickness=0, cursor="hand1")
        labels.append(l)

    labelh = []

    switches = request.get_switches()
    print(len(switches))
    a = 0
    b = 0
    c = 0
    a1 = 0
    b1 = 0
    switch_data = {}
    size = len(switches)
    switch_image = ImageTk.PhotoImage(Image.open("icons/icons8-switch-50.png"))
    switch_image1 = ImageTk.PhotoImage(Image.open("icons/switcher2.png"))
    host_image = ImageTk.PhotoImage(Image.open("icons/icons8-laptop-64.png"))
    hos_image1 = ImageTk.PhotoImage(Image.open("icons/laptop1.png"))
    hos_image2 = ImageTk.PhotoImage(Image.open("icons/desktop.png"))
    hos_image3 = ImageTk.PhotoImage(Image.open("icons/tablet.png"))
    list_image = [host_image, hos_image1, hos_image2, hos_image3]
    list_image_switcher = [switch_image1]

    if switches != None:
        i = 0
        sp = 0
        hp = 0
        switch_list_count = 0
        for switch in switches:

            sp = sp + 1
            if (sp <= (size / 2)):
                a = 400
                b = b + 100
                a1 = a
                b1 = b
            else:
                a = 800
                c = c + 100
                a1 = a
                b1 = c
            switch_name = f"switch_{switch['dpid']}"
            test = {id: i, "sw_name": switch_name}
            full_labesl[i] = test

            def on_click(type, text, name, data, pos_panel):
                print(text)
                title = ""
                inf_data = ""
                panel_switch = Tk()
                if (type == "s"):
                    title = "switch information"
                    dpid = f"dpid:_{data['dpid']}"
                    ports = f"Ports:_{data['ports']}"
                    inf_data = dpid + "\n" + ports

                    def show():
                        flow = Tk()
                        flow.title("flow table")
                        flow_text = dpid[-1]
                        output = subprocess.check_output("sudo ovs-ofctl dump-flows s" + str(flow_text) + "",
                                                         shell=True)
                        label = Label(flow, text=str(output), bg="black", fg="#ccff33", relief='groove', wraplength=250)
                        label.pack()
                        flow.resizable(False, False)

                    flow_table = Button(panel_switch, text="show flow table", bg="green", border=0, command=show)
                    flow_table.pack()
                else:
                    title = "host information"
                    mac = "MAC:_" + data['mac']
                    ipv4 = f"Ipv4:_{data['ipv4']}"
                    ipv6 = f"Ipv6:_{data['ipv6']}"
                    port = f"Port:_{data['port']}"
                    inf_data = mac + "\n" + ipv4 + "\n" + ipv6 + "\n" + port

                panel_switch.title("" + title)
                panel_switch.config(bg="black")
                panel_switch.geometry("250x250+" + str(pos_panel[0]) + "+" + str(pos_panel[1]))

                lab1 = Label(panel_switch, text=inf_data, bg="black", fg="#ccff33", relief='groove', wraplength=250)
                lab1.pack()
                panel_switch.eval('tk::PlaceWindow . center')
                panel_switch.mainloop()

            def run():
                print("switch name==>" + switch_name)



            switch_data[switch_list_count] = {'pos': i, 'name': switch_name, 'x': a1, 'y': b1}
            switch_list_count = switch_list_count + 1
            pos_panel = [a1, b1]
            labels[i].config(text=switch_name, image=secrets.choice(list_image_switcher),
                             command=lambda type="s", k=i, name=switch, data=switch, pos=pos_panel: on_click(type, k,
                                                                                                             name, data,
                                                                                                             pos))
            labels[i].place(x=a1, y=b1)
            x1 = a1
            y1 = b1
            hosts = request.get_hosts_by_switch(switch['dpid'])
            if hosts != None:
                for host in hosts:

                    i = i + 1
                    if (sp <= size / 2):
                        a = a1 - 200
                        b = b1 - 20
                        a1 = a
                        b1 = b
                    else:
                        a = a1 + 200
                        b = b1 - 20
                        a1 = a
                        b1 = b
                    host_name = "PC_" + host['mac']

                    pos_h = [a1, b1]
                    labels[i].config(text=host_name, image=secrets.choice(list_image),
                                     command=lambda type="h", k=i, name=host, data=host, pos=pos_h: on_click(type, k,
                                                                                                             name, data,
                                                                                                             pos))
                    labels[i].place(x=a1, y=b1)
                    x2 = a1
                    y2 = b1
                    l1 = w.create_text(x1, y1 + 30, fill="red", tag="l1")
                    l2 = w.create_text(x2, y2 + 30, fill="blue", tag="l2")

                    x1 = w.coords(l1)[0]
                    y1 = w.coords(l1)[1]
                    x2 = w.coords(l2)[0]
                    y2 = w.coords(l2)[1]
                    line(x1, y1, x2, y2, "red")

                    i = i + 1

    links = request.get_links()
    if links != None:
        for link in links:
            pos1 = 0
            pos2 = 0
            x1 = 0
            x2 = 0
            y1 = 0
            y2 = 0
            for i in range(switch_list_count):
                if (switch_data[i]['name'] == f"switch_{link['src']['dpid']}"):
                    pos1 = switch_data[i]['pos']
                    x1 = switch_data[i]['x']
                    y1 = switch_data[i]['y']
                    print("======================find src====================")
                    print(f"switch_{link['src']['dpid']}")

                if (switch_data[i]['name'] == f"switch_{link['dst']['dpid']}"):
                    pos2 = switch_data[i]['pos']
                    x2 = switch_data[i]['x']
                    y2 = switch_data[i]['y']
                    print("======================find dist====================")
                    print(f"switch_{link['dst']['dpid']}")

            l1 = w.create_text(x1 + 30, y1 + 30, fill="red", tag="l1")
            l2 = w.create_text(x2 + 30, y2 + 30, fill="blue", tag="l2")

            x1 = w.coords(l1)[0]
            y1 = w.coords(l1)[1]
            x2 = w.coords(l2)[0]
            y2 = w.coords(l2)[1]
            line(x1, y1, x2, y2, "green")

create()

def printit():

  threading.Timer(15.0, printit).start()
  clear_frame()
  w.delete('all')
  create()

printit()
master.attributes('-fullscreen', True)
master.resizable(False, False)

master.mainloop()