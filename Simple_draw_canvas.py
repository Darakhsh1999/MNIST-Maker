import tkinter as tk
from tkinter import messagebox
import PIL.Image
import PIL.ImageDraw


WIDTH, HEIGHT = 500, 500
CENTER = WIDTH // 2
WHITE = (255,255,255)


class PaintGUI():

    def __init__(self) :
        
        self.root = tk.Tk()
        self.root.geometry("500x500")
        #self.root.state("zoomed")
        self.root.title("MNIST maker [S]ave image, [R]eset image")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # update so these values are passed from the settings class
        self.color = "black"
        self.brush_width = 12

        self.canvas = tk.Canvas(self.root, width= WIDTH-10, height= HEIGHT-10, bg= "white", cursor= "circle")
        self.canvas.bind("<B1-Motion>", self.paint, add="+")
        self.root.bind("<KeyPress-R>", lambda e: self.clear(), add="+")
        self.root.bind("<KeyPress-r>", lambda e: self.clear(), add="+")
        self.canvas.pack()

        # Pillow image used for
        self.image = PIL.Image.new("L", (WIDTH, HEIGHT), 255) 
        self.draw = PIL.ImageDraw.Draw(self.image)

        self.root.mainloop()

    def KeyPress(self, event):
        print("Pressed bound key")

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_rectangle(x1,y1,x2,y2, outline= self.color, fill= self.color, width= self.brush_width)
        self.draw.rectangle([x1, y1, x2+ self.brush_width, y2+self.brush_width], outline= self.color, fill= self.color, width= self.brush_width)

    def clear(self):
        print("clear is called")
        self.canvas.delete("all")
        self.image = PIL.Image.new("L", (WIDTH, HEIGHT), 255)
        self.draw = PIL.ImageDraw.Draw(self.image)

    def save(self):
        print("last image saved")
        #self.image.save() # (path + image_name + _index, image_save_format)

    def on_closing(self):
        answer = messagebox.askyesnocancel("Quit", "Do you want to save last image?")
        if answer is not None:
            if answer:
                self.save()
            self.root.destroy()

    

p_gui = PaintGUI()