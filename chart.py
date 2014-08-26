### Utility script for picking out katakana characters from chart ###

# import
from tkinter import *
from PIL import Image, ImageTk

# constants
katakana = ['a', 'i', 'u', 'e', 'o',
            'ka', 'ki', 'ku', 'ke', 'ko',
            'sa', 'shi', 'su', 'se', 'so',
            'ta', 'chi', 'tsu', 'te', 'to',
            'na', 'ni', 'nu', 'ne', 'no',
            'ha', 'hi', 'fu', 'he', 'ho',
            'ma', 'mi', 'mu', 'me', 'mo',
            'ya', 'yu', 'yo',
            'ra', 'ri', 'ru', 're', 'ro',
            'wa', 'wo', 'n']

# variables
size = 0
index = 0
orig = (-1, -1)

base = "data\\computer (gray)\\"
directory = "dart\\"
chartdir  = "_katakana_chart.jpg"

# functions
def orig1(event):
    global orig
    orig = (event.x, event.y)
    root.title("Katakana Chart [bot right]")
    root.bind("<Button-1>", orig2)

def orig2(event):
    global size, preview, canvas2, frame2, preview
    dist = (event.x - orig[0], event.y - orig[1])
    size = ((min(dist)) // 10) * 10
    root.bind("<Button-1>", click)
    root.bind("<Left>", left)
    root.bind("<Right>", right)
    root.bind("<BackSpace>", back)

    if ('preview' in globals()):
        preview.destroy()
    preview = Toplevel()
    preview.title("Preview [" + str(size) + " x " + str(size) + "]")
    
    frame2 = Frame(preview, width = size, height = size)
    frame2.pack()

    canvas2 = Canvas(frame2, bg = "white", width = size, height = size)
    canvas2.pack()

    first()

def click(event):
    x = event.x
    y = event.y
    kana = image.crop((x - size // 2, y - size // 2, x + size // 2, y + size// 2))
    phot = ImageTk.PhotoImage(kana)
    kana.save(base + directory + katakana[index] + ".png")
    nextkana()
    canvas2.create_image(0, 0, image = phot, anchor = 'nw')
    preview.mainloop()

def first():
    global index
    index = 0
    root.title("Katakana Chart - " + katakana[index])

def prevkana():
    global index
    index = max(index - 1, 0)
    root.title("Katakana Chart - " + katakana[index])

def nextkana():
    global index
    index = min(index + 1, len(katakana) - 1)
    root.title("Katakana Chart - " + katakana[index])

def left(event):
    prevkana()

def right(event):
    nextkana()

def back(event):
    init()

def init():
    global root
    root.title("Katakana Chart [top left]")
    root.bind("<Button-1>", orig1)

root = Tk()
init()

image = Image.open(base + directory + chartdir)
photo = ImageTk.PhotoImage(image)

frame = Frame(root, width = photo.width() , height = photo.height())
frame.pack()

canvas = Canvas(frame, bg = "white", width = photo.width(), height = photo.height())
canvas.create_image(0, 0, image = photo, anchor = 'nw' )
canvas.pack()

#panel = Label(root, image = img)
#panel.pack()

root.mainloop()
