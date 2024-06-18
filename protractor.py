import pyautogui
from tkinter import Tk, Canvas
from PIL import Image, ImageTk
line_ids = []

def replace_image(event):
    update_image(event)

def update_image(event):
    global rotate_the_protractor, image, photo, image_id
    if event.keysym.lower() == 'right':
        if rotate_the_protractor <= 0:
            rotate_the_protractor = 359
        else:
            rotate_the_protractor -= 1
    elif event.keysym.lower() == 'left':
        if rotate_the_protractor >= 359:
            rotate_the_protractor = 0
        else:
            rotate_the_protractor += 1
    elif event.keysym.lower() == 'd':
        root.destroy()
    image = Image.open(f'rotate_the_protractor/{rotate_the_protractor}.png').convert('RGBA')
    photo = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_id, image=photo)
   
def drag_image(event):
    global start_x, start_y, image_x, image_y, delta_x, delta_y,x,y
    x = event.x - delta_x
    y = event.y - delta_y
    canvas.coords(image_id, x, y)
    image_x = x
    image_y = y

def start_drag(event):
    global start_x, start_y, image_x, image_y, delta_x, delta_y
    start_x = event.x
    start_y = event.y
    delta_x = event.x - image_x
    delta_y = event.y - image_y

rotate_the_protractor=0
image_x=500
image_y=500
root = Tk()
root.attributes('-fullscreen', True)
root.configure(background='black')
root.wm_attributes('-topmost', True)
root.wm_attributes("-transparentcolor", "black")
root.overrideredirect(True)
pyautogui.FAILSAFE = False
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
canvas = Canvas(root, width=w, height=h, bg='black')
canvas.config(highlightthickness=0)
canvas.pack()
image = Image.open(f'rotate_the_protractor/{rotate_the_protractor}.png')
image = image.convert('RGBA')
photo = ImageTk.PhotoImage(image, master=root)
x=round(image.width/2)
y=round(image.height/2)
width = image.width
height = image.height
image_id = canvas.create_image(image_x, image_y, anchor='nw', image=photo)
canvas.bind('<Button-1>', start_drag)
canvas.bind('<B1-Motion>', drag_image)
root.bind('<KeyPress>', replace_image)
root.mainloop()
