from pyautogui import moveTo, size, click, position
import random as rand
from time import sleep
import tkinter as ttk
import ctypes
from pynput import keyboard
from multipledispatch import dispatch
import pickle


global baseX, baseY
baseX = 0
baseY = 0
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def left_click():
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def openItems():
    global baseX, baseY
    click(1, 1)
    PressKey(25)
    sleep(.2)
    ReleaseKey(25)
    sleep(.5)
    click(baseX + 440, baseY - 200)
    sleep(.2)
    left_click()
    sleep(.2)


#for mythic, 3x10
def mythicRandom():
    global baseX, baseY
    openItems()
    click(baseX - 40, baseY - 100)
    left_click()
    sleep(.2)
    click(baseX - 40, baseY - 60)
    left_click()
    sleep(.2)
    for i in range(15):
        row = rand.randint(0,2)
        col = rand.randint(0,9)
        while (row == 2 and col > 2):
            col = rand.randint(0,10)
        click(baseX + col*56, baseY + row*73)
        left_click()
        print(row, col)
        print(position())
        sleep(.3)

#For legendaries, 7x10
def legendRandom():
    global baseX, baseY
    openItems()
    click(baseX - 40, baseY - 100)
    left_click()
    sleep(.2)
    click(baseX - 40,baseY - 40)
    left_click()
    sleep(.2)
    for i in range(15):
        row = rand.randint(0,6)
        if (row == 6):
            col = 0
        else:
            col = rand.randint(0,9)
        click(baseX + col*56, baseY + row*74)
        left_click()
        print(row, col)
        print(position())
        sleep(.3)

@dispatch(tuple)
def calibrate(position):
    print('calibrating')
    with open("basePosi.pickle", "wb") as f:
        pickle.dump((position[0],position[1]), f, protocol=pickle.HIGHEST_PROTOCOL)
    calibrate()

@dispatch()
def calibrate():
    global baseX, baseY
    try:
        with open('basePosi.pickle', "rb") as f:
            basePos = pickle.load(f)
    except (OSError, IOError) as e:
        with open("basePosi.pickle", "wb") as f:
            pickle.dump((620,280), f, protocol=pickle.HIGHEST_PROTOCOL)
    baseX = basePos[0]
    baseY = basePos[1]
    print('calibration complete')
    print(str(baseX) + ", " + str(baseY))

def on_press(key):
    if key == keyboard.Key.enter:
        calibrate(position())
        return False

def beginCalibration():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

'''
while True:
    iType = input("Mythic or Legendary?\n")
    if iType[0].lower() == 'm':
        mythicRandom()
        break
    elif iType[0].lower() == 'l':
        legendRandom()
        break
    else:
        print("Try Again")
'''

calibrate()
root = ttk.Tk()
root.title("Item Randomizer")

root.geometry("280x50+1630+730")
ttk.Button(root, text="Recalibrate", height = 1, width = 40, command=beginCalibration).pack(side = ttk.BOTTOM)
ttk.Button(root, text="Mythic", height = 1, width = 20, command=mythicRandom).pack(side = ttk.LEFT)
ttk.Button(root, text="Legendary", height = 1, width = 20, command=legendRandom).pack(side = ttk.RIGHT)

root.lift()
root.attributes("-topmost", True)
root.mainloop()


'''
while True:
    print(position())
'''


# Collect events until released