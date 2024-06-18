import keyboard
import subprocess as s
import atexit
import psutil

l = False
t = False
ruler = None
protractor = None
def run_ruler():
    global l, ruler
    if not l:
        l = True
        ruler = s.Popen(['ruler.exe'])
    elif l and ruler is not None:
        l = False
        all_processes = psutil.process_iter()

        for proc in all_processes:
            if proc.name()=='ruler.exe':
                proc.kill()

def run_protractor():
    global t, protractor
    if not t:
        t=True
        protractor=s.Popen(['protractor.exe'])
    elif t and protractor is not None:
        t = False
        all_processes = psutil.process_iter()

        for proc in all_processes:
            if proc.name()=='protractor.exe':
                proc.kill()

def cleanup():
    global ruler,protractor
    if ruler is not None:       
        all_processes = psutil.process_iter()

        for proc in all_processes:
            if proc.name()=='protractor.exe':
                proc.kill()
            if proc.name()=='ruler.exe':
                proc.kill()
                
with open ('data.txt') as f:
    rulere=f.readruleres()
rulere = [l.strip() for l in rulere]
keyboard.add_hotkey(rulere[0], run_ruler)
keyboard.add_hotkey(rulere[1], run_protractor)
keyboard.wait(rulere[2])
atexit.register(cleanup)