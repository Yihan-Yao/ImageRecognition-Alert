from python_imagesearch.imagesearch import imagesearcharea, region_grabber
import pyautogui, keyboard, time, threading
from tkinter import *
import winsound;
import os

region = [-1, -1, -1, -1]
root = Tk()
root.title("图灵的localalert")

label1 = Label(root, text="左上未设置")
label2 = Label(root, text="右下未设置")

def tlButtonClick():
    while True:
        if keyboard.is_pressed('space'):
            pos = pyautogui.position()
            label1.config(text = str(pos))
            region[0] = pos[0]
            region[1] = pos[1]
            break

def tlButtonClickThread():
    threading.Thread(target=tlButtonClick).start();

def brButtonClick():
    while True:
        if keyboard.is_pressed('space'):
            pos = pyautogui.position()
            label2.config(text = str(pos))
            region[2] = pos[0]
            region[3] = pos[1]
            break

def brButtonClickThread():
    threading.Thread(target=brButtonClick).start();

def take_screenshot(coord):
    # Take the screenshot in the given corrds
    im = pyautogui.screenshot(region=(coord[0], coord[1], 100, 20))
    return PhotoImage(im)

running = False

def startButtonClick():
    labelStart.config(text = "正在运行")
    global running
    running = True
    while True:
        if running == False:
            break
        textbox.delete("1.0", "end")
        if region[2]-region[0] < 40:
            region[2] = region[0] + 40
        if region[3]-region[1] < 40:
            region[3] = region[1] + 40
        im = region_grabber((region[0], region[1], region[2], region[3]))
        redpos = imagesearcharea("red.png", 0, 0, im.width, im.height, 0.95, im)
        neutpos = imagesearcharea("neut.png", 0, 0, im.width, im.height, 0.95, im)
        textbox.insert("end", "redpos:  "+str(redpos)+'\n')
        textbox.insert("end", "neutpos: "+str(neutpos)+'\n')
        if redpos[0] != -1 or neutpos[0] != -1:
            winsound.PlaySound(r'./Warning.wav', winsound.SND_FILENAME)
            time.sleep(2.5)
        else:
            time.sleep(1)

def startButtonClickThread():
    threading.Thread(target=startButtonClick).start();
    
def stopButtonClick():
    labelStart.config(text = "未开始")
    textbox.delete("1.0", "end")
    global running
    running = False;

    

tlButton = Button(root, text="按空格设置左上", command=tlButtonClickThread)
brButton = Button(root, text="按空格设置右下", command=brButtonClickThread)

label1.grid(column=0, row=0, padx=20, pady=20)
label2.grid(column=1, row=0, padx=20, pady=20)
tlButton.grid(column=0, row=1, padx=20, ipady=20)
brButton.grid(column=1, row=1, padx=20, ipady=20)

labelStart = Label(root, text="未开始")
labelStart.grid(padx=20, pady=20, columnspan=2)
startButton = Button(root, text="开始", command=startButtonClickThread)
startButton.grid(ipadx=40, ipady=20, columnspan=2)
stopButton = Button(root, text="停止", command=stopButtonClick)
stopButton.grid(ipadx=40, ipady=20, columnspan=2)

textbox = Text(root, width=40, height=10)
textbox.grid(padx=20, pady=20, columnspan=2)

root.mainloop()