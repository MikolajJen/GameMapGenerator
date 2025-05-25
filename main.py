import random
from tkinter import *
from tkinter import messagebox
from core.mapgeneration import generateMapXHTML, generateMapToPNG
from core.readPNG import decodeIDAT, pixels_to_tkinter_photoimage
from core.perlin import setSeed
import time
import os

root = Tk()


root.title('Fractal Brownian Motion')
root.resizable(False, False)

root.geometry('800x600')


formFrame = Frame(root)
formFrame.place(relx=0.5, rely=0.0, anchor='n')

#Width and height txt's
widthLbl = Label(formFrame, text="Width: ")
widthLbl.grid(row=0, column=0, padx=5, pady=5)
widthTxt = Entry(formFrame, width="10")
widthTxt.grid(row=0, column=1, padx=5, pady=5)

heightLbl = Label(formFrame, text="Height: ")
heightLbl.grid(row=0, column=2, padx=5, pady=5)
heightTxt = Entry(formFrame, width="10")
heightTxt.grid(row=0, column=3, padx=5, pady=5)

formFrame.grid_columnconfigure(0, weight=1)
formFrame.grid_rowconfigure(1, weight=1)

seedFrame = Frame(root, width=100, height=100)
seedFrame.place(relx=0.5, rely=0.15, anchor='n')

seedLabel = Label(seedFrame, text="Seed: ")
seedLabel.grid(row=0, column=1, padx=5, pady=5)

seedTxt = Entry(seedFrame, width="10")
seedTxt.grid(row=0, column=2, padx=5, pady=5)

seedButton = Button(seedFrame, text="Randomize a seed", command = lambda: randomizeSeed())
seedButton.grid(row = 0, column=3, padx=5, pady=5)


imgFrame = Frame(root, width=400, height=400, background="white")
imgFrame.place(relx=0.5, rely=.6, anchor='center')

image = []





def randomizeSeed():
    seedTxt.delete(0, END)
    random.seed(time.time())
    seed = random.randint(0, 999999999)
    seedTxt.insert(0, seed)


def genMapPNG(label, width, height):

    try:
        width = int(width)
        height = int(height)
    except (ValueError):
        messagebox.showerror(
            title="Error!",
            message="Width and height must be integers!"
        )
        return
    if width <= 0 or height <= 0:
        messagebox.showerror(
            title="Error!",
            message="Width and height must be positive values"
        )
        return
    if width != height:
        messagebox.showerror(
            title="Error!",
            message="Width and height must be equal"
        )
        return

    try:
        seed = int(seedTxt.get())
    except(ValueError):
        messagebox.showerror(
            title="Error!",
            message="Seed must be an integer"
        )
        return

    setSeed(seed)
    generateMapToPNG(width, height)



    image = decodeIDAT()

    photo = pixels_to_tkinter_photoimage(image)





    label.configure(image=photo)
    label.image = photo
    label.pack()





def genMapXHTML(width, height):
    try:
        width = int(width)
        height = int(height)
    except (ValueError):
        messagebox.showerror(
            title="Error!",
            message="Width and height must be integers!"
        )
        return
    if width <= 0 or height <= 0:
        messagebox.showerror(
            title="Error!",
            message="Width and height must be positive values"
        )
        return
    if width != height:
        messagebox.showerror(
            title="Error!",
            message="Width and height must be equal"
        )
        return

    try:
        seed = int(seedTxt.get())
    except(ValueError):
        messagebox.showerror(
            title="Error!",
            message="Seed must be an integer"
        )
        return

    answer = messagebox.askokcancel(
        title="Warning!",
        message="This is an experimental function.\n"
                "This will produce a very big XHTML file which size depends on width and height input.\n"
                "Do you want to proceed?"
    )

    if(answer):
        setSeed(seed)
        generateMapXHTML(width, height)
    else:
        print("Anulowano")


imgLabel = Label(imgFrame, bg='white')

if os.path.exists('map.png'):
    image=decodeIDAT()
    photo = pixels_to_tkinter_photoimage(image)
    imgLabel.configure(image=photo)
    imgLabel.image = photo
    imgLabel.pack()


btnFrame = Frame(root)
btnFrame.place(relx=0.5, rely=0.050, anchor='n')

btnGenerateXHTML = Button(btnFrame, text = "Generate a XHTML map", fg="black", command = lambda: genMapXHTML(widthTxt.get(), heightTxt.get()))
btnGenerateXHTML.grid(row=2, column=0, columnspan=3, pady=10)

btnGenerateMap = Button(btnFrame, text = "Generate a PNG", fg="black", command = lambda: genMapPNG(imgLabel, widthTxt.get(), heightTxt.get()))
btnGenerateMap.grid(row=2, column=3, columnspan=3, pady=10)

btnFrame.grid_columnconfigure(0, weight=1)
btnFrame.grid_rowconfigure(1, weight=1)










root.mainloop()