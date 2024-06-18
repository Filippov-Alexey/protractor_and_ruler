import keyboard
import subprocess as s
import atexit

ruler = None
protractor = None

def run_ruler():
    global ruler
    if ruler is None:
        ruler=s.Popen(['python','ruler.py'])
    elif ruler is not None:
        ruler.terminate()
        ruler=None

def run_protractor():
    global protractor
    if protractor is None:
        protractor = s.Popen(['python', 'protractor.py'])
    elif protractor is not None:
        protractor.terminate()
        protractor = None

def cleanup():
    global ruler, protractor
    if ruler is not None:
        ruler.terminate()
    if protractor is not None:
        protractor.terminate()
    
with open('data.txt') as f:
    hotkeys = f.readlines()
hotkeys = [line.strip() for line in hotkeys]

keyboard.add_hotkey(hotkeys[0], run_ruler)
keyboard.add_hotkey(hotkeys[1], run_protractor)
keyboard.wait(hotkeys[2])

atexit.register(cleanup)
