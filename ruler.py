import math
import time
import pyautogui
import win32api
import win32gui
import win32con
from pynput import mouse
from pynput.mouse import Listener,Controller
from tkinter import Tk, Canvas
from PIL import Image, ImageTk
line_ids = []

def replace_image(event):
    update_image(event)
    draw_lines()

def update_image(event):
    global rotate_the_ruler, image, photo, image_id
    if event.keysym.lower() == 'right':
        if rotate_the_ruler <= 0:
            rotate_the_ruler = 359
        else:
            rotate_the_ruler -= 1
    elif event.keysym.lower() == 'left':
        if rotate_the_ruler >= 359:
            rotate_the_ruler = 0
        else:
            rotate_the_ruler += 1
    image = Image.open(f'rotate_the_ruler/{rotate_the_ruler}.png').convert('RGBA')
    photo = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_id, image=photo)
    draw_lines()

def draw_lines():
    global line_ids, x_center, y_center, x1_rot, y1_rot, x2_rot, y2_rot, x3_rot, y3_rot, x4_rot, y4_rot
    global x1_line, y1_line, x2_line, y2_line, x3_line, y3_line, x4_line, y4_line
    angle_rad = math.radians(rotate_the_ruler)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    width = image.width
    height = image.height
    rect_width = 820
    rect_height = 58
    x=image_x
    y=image_y
    # Определяем координаты центра прямоугольника
    x_center = x+width/2
    y_center = y+height/2
    
    x1 = -rect_width / 2
    y1 = -10
    x2 = -rect_width / 2
    y2 = -rect_height / 2
    x3 = rect_width / 2
    y3 = -rect_height / 2
    x4 = rect_width / 2
    y4 = -10
    
    # Применяем угол наклона к координатам вершин
    x1_rot = x1 * cos_angle - y1 * sin_angle
    y1_rot = x1 * sin_angle + y1 * cos_angle
    x2_rot = x2 * cos_angle - y2 * sin_angle
    y2_rot = x2 * sin_angle + y2 * cos_angle
    x3_rot = x3 * cos_angle - y3 * sin_angle
    y3_rot = x3 * sin_angle + y3 * cos_angle
    x4_rot = x4 * cos_angle - y4 * sin_angle
    y4_rot = x4 * sin_angle + y4 * cos_angle
    
    # Рассчитываем координаты вершин вокруг повернутого прямоугольника
    x1_line = x_center + x1_rot
    y1_line = y_center + y1_rot
    x2_line = x_center + x2_rot
    y2_line = y_center + y2_rot
    x3_line = x_center + x3_rot
    y3_line = y_center + y3_rot
    x4_line = x_center + x4_rot
    y4_line = y_center + y4_rot
    
    # Удаляем предыдущий прямоугольник
    if line_ids:
        canvas.delete(line_ids)
    
    # Рисуем прямоугольник вокруг повернутого прямоугольника
    line_ids = canvas.create_polygon(x1_line, y1_line,
                                     x2_line, y2_line,
                                     x3_line, y3_line,
                                     x4_line, y4_line,
                                     outline='red', fill='',width=2)

def start_drag(event):
    global start_x, start_y, image_x, image_y, delta_x, delta_y
    start_x = event.x
    start_y = event.y
    delta_x = event.x - image_x
    delta_y = event.y - image_y

def drag_image(event):
    global start_x, start_y, image_x, image_y, delta_x, delta_y,x,y
    x = event.x - delta_x
    y = event.y - delta_y
    canvas.coords(image_id, x, y)
    image_x = x
    image_y = y
    draw_lines()

def is_point_inside_rectangle(x, y, x1, y1, x2, y2, x3, y3, x4, y4):
    # Проверяем, находится ли точка (x, y) внутри повернутого прямоугольника
    # Используем метод спроецированных координат
    def is_point_inside_triangle(px, py, ax, ay, bx, by, cx, cy):
        # Проверяем, находится ли точка (px, py) внутри треугольника, определенного вершинами (ax, ay), (bx, by), (cx, cy)
        d1 = (px - bx) * (ay - by) - (ax - bx) * (py - by)
        d2 = (px - cx) * (by - cy) - (bx - cx) * (py - cy)
        d3 = (px - ax) * (cy - ay) - (cx - ax) * (py - ay)
        return (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0)
    
    # Проверяем, находится ли точка внутри повернутого прямоугольника
    return is_point_inside_triangle(x, y, x1, y1, x2, y2, x3, y3) or is_point_inside_triangle(x, y, x1, y1, x3, y3, x4, y4)

def closest_line_to_point(cursor_x, cursor_y, line1_x, line1_y, line2_x, line2_y, line3_x, line3_y, line4_x, line4_y):
    # Вычисляем расстояние от курсора (cursor_x, cursor_y) до каждой из четырех линий
    distance1 = distance_to_line(cursor_x, cursor_y, line1_x, line1_y, line2_x, line2_y)
    distance2 = distance_to_line(cursor_x, cursor_y, line2_x, line2_y, line3_x, line3_y)
    distance3 = distance_to_line(cursor_x, cursor_y, line3_x, line3_y, line4_x, line4_y)
    distance4 = distance_to_line(cursor_x, cursor_y, line4_x, line4_y, line1_x, line1_y)
    
    # Находим минимальное расстояние
    min_distance = min(distance1, distance2, distance3, distance4)
    
    # Определяем ближайшую линию на основе минимального расстояния
    if min_distance == distance1:
        closest_line = (line1_x, line1_y, line2_x, line2_y)
    elif min_distance == distance2:
        closest_line = (line2_x, line2_y, line3_x, line3_y)
    elif min_distance == distance3:
        closest_line = (line3_x, line3_y, line4_x, line4_y)
    else:
        closest_line = (line4_x, line4_y, line1_x, line1_y)
    
    return closest_line

def distance_to_line(x, y, line_x1, line_y1, line_x2, line_y2):
    # Вычисляем расстояние от точки (x, y) до прямой, проходящей через точки (line_x1, line_y1) и (line_x2, line_y2)
    numerator = abs((line_y2 - line_y1) * x - (line_x2 - line_x1) * y + (line_x2 * line_y1) - (line_y2 * line_x1))
    denominator = math.sqrt((line_y2 - line_y1) ** 2 + (line_x2 - line_x1) ** 2)

    # Проверка нулевого делителя
    if math.isclose(denominator, 0):
        return 0

    distance = numerator / denominator

    return int(distance)

# Функция для отслеживания координат курсора
def on_click(x,y):
    global x1_line, y1_line, x2_line, y2_line, x3_line, y3_line, x4_line, y4_line,prevx,prevy
    while is_point_inside_rectangle(x, y, x1_line, y1_line, x2_line, y2_line, x3_line, y3_line, x4_line, y4_line) and win32api.GetKeyState(0x01) <0:
        x1, y1, x2, y2 = closest_line_to_point(x, y, x1_line, y1_line, x2_line, y2_line, x3_line, y3_line, x4_line, y4_line)
        d = distance_to_line(x, y, x1, y1, x2, y2)

        if y < prevy:
            angle = math.atan2(y2 - y1, x2 - x1)
            if (90<rotate_the_ruler<180 or 270<rotate_the_ruler<359):
                y=y-1*math.sin(angle)
                x=x-1*math.cos(angle)
            elif (0<rotate_the_ruler<90 or 180<rotate_the_ruler<270):
                y=y+1*math.sin(angle)
                x=x+1*math.cos(angle)
            time.sleep(0.25)
            pyautogui.moveTo(x, y+d)

        if y > prevy:
            angle = math.atan2(y2 - y1, x2 - x1)
            if (90<rotate_the_ruler<180 or 270<rotate_the_ruler<359):
                y=y-1*math.sin(angle)
                x=x-1*math.cos(angle)
            elif (0<rotate_the_ruler<90 or 180<rotate_the_ruler<270):
                y=y+1*math.sin(angle)
                x=x+1*math.cos(angle)
            time.sleep(0.25)
            pyautogui.moveTo(x, y-d)

        if x < prevx:
            angle = math.atan2(y2 - y1, x2 - x1)
            if (90<rotate_the_ruler<180 or 270<rotate_the_ruler<359):
                y=y-1*math.sin(angle)
                x=x-1*math.cos(angle)
            elif (0<rotate_the_ruler<90 or 180<rotate_the_ruler<270):
                y=y+1*math.sin(angle)
                x=x+1*math.cos(angle)
            time.sleep(0.25)
            pyautogui.moveTo(x, y+d)

        if x > prevx:
            angle = math.atan2(y2 - y1, x2 - x1)
            if (90<rotate_the_ruler<180 or 270<rotate_the_ruler<359):
                y=y-1*math.sin(angle)
                x=x-1*math.cos(angle)
            elif (0<rotate_the_ruler<90 or 180<rotate_the_ruler<270):
                y=y+1*math.sin(angle)
                x=x+1*math.cos(angle)
            time.sleep(0.25)
            pyautogui.moveTo(x, y-d)

    prevx = x
    prevy = y

mo=Controller()
prevx=0
prevy=0
line_ids = []
start_x = 0
start_y = 0
image_x=500
image_y=500
rotate_the_ruler = 0
x1_line=0
y1_line=0
x2_line=0
y2_line=0
x3_line=0
y3_line=0
x4_line=0
y4_line=0
root = Tk()
root.attributes('-fullscreen', True)
root.configure(background='black')
root.wm_attributes('-topmost', True)
root.wm_attributes("-transparentcolor", "black")
root.overrideredirect(True)
hwnd = win32gui.FindWindow(None, root.title())
win32gui.ShowWindow(hwnd, 0)
hwnd = win32gui.GetForegroundWindow()
if hwnd:
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_TOOLWINDOW)
pyautogui.FAILSAFE = False
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
canvas = Canvas(root, width=w, height=h, bg='black')
canvas.config(highlightthickness=0)
canvas.pack()
image = Image.open(f'rotate_the_ruler/{rotate_the_ruler}.png')
image = image.convert('RGBA')
photo = ImageTk.PhotoImage(image, master=root)
x=round(image.width/2)
y=round(image.height/2)
width = image.width
height = image.height
image_id = canvas.create_image(image_x, image_y, anchor='nw', image=photo)
draw_lines()

canvas.bind('<Button-1>', start_drag)
canvas.bind('<B1-Motion>', drag_image)
root.bind('<KeyPress>', replace_image)
liste=Listener(on_move=on_click)
liste.start()

listener = mouse.Listener(on_move=on_click)
listener.start()
root.mainloop()
