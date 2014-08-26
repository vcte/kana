# GUI for drawing
from tkinter import *
from PIL import Image, ImageDraw, ImageTk

from normalize import normalize
from ann import ANN

# variables

width = 500
height = 500

# functions

def gui():
    global draw, image, photo, canvas
    root = Tk()
    root.title("Katakana Handwriting Recognition")
    root.bind("<B1-Motion>", paint)
    root.bind("<B3-Motion>", erase)
    root.bind("<Return>", classify_draw)
    root.bind("<BackSpace>", clear_draw)

    frame = Frame(root, width = width, height = height)
    frame.pack()

    #img = PhotoImage(width = width, height = height)
    #img.put("#EEEEEE", (50, 50))
    #img = ImageTk.PhotoImage(Image.open("data\\computer (color)\\anime\\a.png"))
    #img = ImageTk.PhotoImage('RGB', (width, height))
    image = Image.new("RGB", (16, 16), 0xFFFFFF).resize((width, height))
    photo = ImageTk.PhotoImage(image)
    draw = ImageDraw.Draw(image) #pxs = image.load()
    prev = (-1, -1)
    
    canvas = Canvas(frame, bg = "white", width = width, height = height)
    canvas.create_image(0, 0, image = photo, anchor = 'nw')
    canvas.pack()

    #img.put("#EEEEEE", (50, 50))

    root.mainloop()

def refresh_draw():
    global image, photo, canvas
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image = photo, anchor = 'nw')

def paint(event):
    global draw
    (x, y) = (event.x, event.y)
    if (x >= 0 and x < width and y >= 0 and y < height):
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill = (0, 0, 0))
        refresh_draw()

def erase(event):
    global draw
    (x, y) = (event.x, event.y)
    if (x >= 0 and x < width and y >= 0 and y < height):
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill = (0xFF, 0xFF, 0xFF))
        refresh_draw()

def classify_draw(event):
    print("classifying drawing")
    ann.classify(ann.parse(normalize(image)))

def clear_draw(event):
    global draw
    draw.ellipse((-width, -height, width * 2, height * 2), fill = (0xFF, 0xFF, 0xFF))
    refresh_draw()

def outweights(l, j):
	return [ann.weights[l][i][j] for i in range(len(ann.weights[l]))]

def reconstruct(data):
	img = Image.new("LA", (16, 16))
	pxs = img.load()
	for x in range(16):
		for y in range(16):
			pxs[x, y] = (int(data[y * 16 + x] * 128 + 128), 255)
	return img

if __name__ == "__main__":
    ann = ANN()
    ann.load("256_iteration_30")
    
    gui()
