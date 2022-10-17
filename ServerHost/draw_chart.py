import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import NewdiscoverRPI
import threading
# import imageSharing_Server_2 as imageServer
# import service_announcement as announce
from PIL import Image, ImageTk
import csv
import cv2
import os
import sys


window = tk.Tk()
window.title('Statistic')
window.geometry('1200x600')
canvas1 = tk.Canvas(window, width = 400, height = 500)
canvas1.pack()
canvas1.place(x=0, y=230)

def read_data():
    data = pd.read_csv("Data_record.csv")

    a = []
    recycleQuantity = 0
    trashQuantity = 0
    glassQuantity = 0
    plasticQuantity = 0
    recycleWeight = 0
    trashWeight = 0
    glassWeight = 0
    plasticWeight = 0

    # For Quantity
    for i in data['background']:
        if i == 'recycle':
            recycleQuantity += 1
        elif i == 'trash':
            trashQuantity += 1
        elif i == 'glass':
            glassQuantity += 1
        elif i == 'plastic':
            plasticQuantity += 1

    # For Weight
    p = data.loc[(data['background'] == 'recycle')]

    c = p['250g']

    for x in c:
        weightString = x.strip('g')
        weight = int(weightString)
        recycleWeight += abs(weight)

    p = data.loc[(data['background'] == 'trash')]

    c = p['250g']

    for x in c:
        weightString = x.strip('g')
        weight = int(weightString)
        trashWeight += abs(weight)

    p = data.loc[(data['background'] == 'glass')]

    c = p['250g']

    for x in c:
        weightString = x.strip('g')
        weight = int(weightString)
        glassWeight += abs(weight)

    p = data.loc[(data['background'] == 'plastic')]

    c = p['250g']

    for x in c:
        weightString = x.strip('g')
        weight = int(weightString)
        plasticWeight += abs(weight)

    return recycleQuantity, trashQuantity, glassQuantity, plasticQuantity, recycleWeight, trashWeight, glassWeight, plasticWeight

def plots(window, flag):
    rq, tq, gq, pq, rw, tw, gw, pw = read_data()

    global canvas_l, canvas_r, figure_l, figure_r

    frame = tk.Frame(window)
    frame.pack()
    frame_l = tk.Frame(frame)
    frame_r = tk.Frame(frame)
    frame_l.pack(side='left')
    frame_r.pack(side='right')

    # For Quantity
    figure_l = plt.figure(figsize=(4, 6))
    ax1 = figure_l.add_subplot(111)
    value1 = [rq, tq, gq, pq]
    totalQuantity = rq + tq + gq + pq
    recyclePercent1 = round(rq / totalQuantity * 100, 2)
    trashPercent1 = round(tq / totalQuantity * 100, 2)
    glassPercent1 = round(gq / totalQuantity * 100, 2)
    plasticPercent1 = round(pq / totalQuantity * 100, 2)
    ax1.pie(value1, labels=["recycle\n" + str(recyclePercent1) + '%', "trash\n" + str(trashPercent1) + '%',
                            "glass\n" + str(glassPercent1) + '%', "plastic\n" + str(plasticPercent1) + '%'],
            startangle=0, counterclock=False)
    figure_l.canvas
    canvas_l = FigureCanvasTkAgg(figure_l, frame_l)
    canvas_l.draw()
    canvas_l.flush_events()
    canvas_l.get_tk_widget().pack()
    canvas_l.get_tk_widget().update()

    # For Weight
    figure_r = plt.figure(figsize=(4, 6))
    ax2 = figure_r.add_subplot(111)
    value2 = [rw, tw, gw, pw]
    totalWeight = rw + tw + gw + pw
    recyclePercent2 = round(rw / totalWeight * 100, 2)
    trashPercent2 = round(tw / totalWeight * 100, 2)
    glassPercent2 = round(gw / totalWeight * 100, 2)
    plasticPercent2 = round(pw / totalWeight * 100, 2)
    ax2.pie(value2, labels=["recycle\n" + str(recyclePercent2) + '%', "trash\n" + str(trashPercent2) + '%',
                            "glass\n" + str(glassPercent2) + '%', "plastic\n" + str(plasticPercent2) + '%'],
            startangle=0, counterclock=False)
    canvas_r = FigureCanvasTkAgg(figure_r, frame_r)
    canvas_r.draw()
    canvas_r.flush_events()
    canvas_r.get_tk_widget().pack()
    canvas_r.get_tk_widget().update()
    frame_l.update()
    frame_r.update()
    frame.update()
    figure_l.clear()
    figure_r.clear()
    ax1.clear()
    ax2.clear()
    # canvas_l.get_tk_widget().delete('all')
    # canvas_r.get_tk_widget().delete('all')

    return totalQuantity, totalWeight
global isRunning
isRunning = 1
isPlotted = 0
def close():
    global isRunning
    print("closing")
    isRunning = 0
    window.destroy()
    sys.exit(1)

def main_window():
    global isPlotted
    tq, tw = plots(window, 0)
    L1 = tk.Label(window, text="Quantity", bg='white', width=10, font=("Arial", 40))
    L1.place(x=250, y=80)
    L2 = tk.Label(window, text="Weight", bg='white', width=10, font=("Arial", 40))
    L2.place(x=650, y=80)
    L3 = tk.Label(window, text="Total Quantity: " + str(tq), bg='white', width=18, font=("Arial", 18))
    L3.place(x=275, y=470)
    L4 = tk.Label(window, text="Total Weight: " + str(tw) + 'g', bg='white', width=18, font=("Arial", 18))
    L4.place(x=675, y=470)
    isPlotted += 1
    closeButton = tk.Button(window, text="Close", width=10, height=2, command=close)
    closeButton.place(x=100, y=140)
    if isRunning:
        window.mainloop()

    return window

main_window()
# def show():
#     main_window()
