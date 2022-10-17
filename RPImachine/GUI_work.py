import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Frame
from PIL import Image, ImageTk

white = "#ffffff"
lightBlue2 = "#adc5ed"
font = "Constantia"
fontButtons = (font, 12)
maxWidth  = 1900
maxHeight = 980

def openNewWindow1():
    import imageProcessing_recogbackrpi1_gui_warp_pas

def openNewWindow2():
    import imageProcessing_recogbackrpi1_gui_warp_glass_pas

def openNewWindow3():
    
    # Toplevel object which will
    # be treated as a new window
    newWindow3 = Toplevel(mainWindow)
 
    # sets the title of the
    # Toplevel widget
    newWindow3.title("Paper VS Other")
 
    # sets the geometry of toplevel
    newWindow3.geometry("800x480")
 
    # A Label widget to show in toplevel
    Label(newWindow3).pack()
    mainFrame = Frame(newWindow3)
    mainFrame.place(x=20, y=20)
    closeButton = Button(newWindow3, text = "CLOSE", font = fontButtons, bg = white, width = 20, height= 1)
    closeButton.configure(command= lambda: newWindow3.destroy())
    closeButton.place(x=270,y=430)
    #Capture video frames
    lmain = tk.Label(mainFrame)
    lmain.grid(row=0, column=0)
    def show_frame():
        ret, frame = cap.read()
        cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img   = Image.fromarray(cv2image).resize((760, 400))
        imgtk = ImageTk.PhotoImage(image = img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)
    show_frame()

# a button widget which will open a
# new window on button click
  #Graphics window
mainWindow = tk.Tk()
mainWindow.configure(bg=lightBlue2)
mainWindow.geometry('%dx%d+%d+%d' % (maxWidth,maxHeight,0,0))
mainWindow.resizable(0,0)
# mainWindow.overrideredirect(1)

   
class1 = Button(mainWindow,
             text ="Trash VS Other",
             width = 80,
             height = 10,
                command = openNewWindow1)
class1.pack(pady = 50)
class2 = Button(mainWindow,
             text ="Glass VS Other",
             width = 80,
             height = 10,
             command = openNewWindow2)
class2.pack(pady = 50)
# class3 = Button(mainWindow,
#              text ="Calibration",
#              width = 30,
#              height = 5,
#              command = openNewWindow2)
# class3.pack(pady = 0)
# trash = tk.Button(mainWindow, text="Trash VS Other", width=80, height=10, command=openNewWindow1)
# trash.place(x=530, y=20)
# glass = tk.Button(mainWindow, text="Trash VS Other", width=80, height=10, command=openNewWindow2)
# glass.place(x=530, y=320)
# calibration = tk.Button(mainWindow, text="Trash VS Other", width=30, height=5, command=openNewWindow2)
# calibration.place(x=750, y=620)
closeButton = Button(mainWindow, text = "CLOSE", font = fontButtons, bg = white, width = 20, height= 1)
closeButton.configure(command= lambda: mainWindow.destroy())
closeButton.place(x=830,y=830)
pic= Image.open("logo2.jpg").resize((300, 300))
photo = ImageTk.PhotoImage(pic)

imgLabel = tk.Label(mainWindow,image=photo)
imgLabel.pack(side=tk.RIGHT)
mainloop()
#Display
#Starts GUI
