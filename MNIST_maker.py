import tkinter as tk
from tkinter import filedialog, messagebox
import PIL.Image
import PIL.ImageDraw
import re
import random
import os
import csv

class MNIST_Maker():
    
    def __init__(self):

        self.save_format = ".jpg"
        self.image_size = None
        self.image_name = None
        self.n_images = None
        self.generated_digits = []
        self.brush_size = None
        self.path_provided = False
        self.save_path = None # Save directory
        
        self.InitializeWindow()

    def ImageSizeButton(self, s):
        self.image_size = s
        self.custom_size.delete(0, tk.END)
        self.custom_size.insert(0,self.custom_size_tt)
        self.UpdateStatus()

    def ImageSize(self, s):
        
        self.custom_size.configure(bg="white")

        if s == self.custom_size_tt and self.image_size is not None:
            return
        elif s == "":
            self.image_size = None
            self.UpdateStatus()
            return

        try:
            self.image_size = int(s)
            self.UpdateStatus()
        except:
            self.custom_size.configure(bg="red")


    def temp_text(self, w, s):
        if len(w.get()) == 0:
            w.insert(0,s)


    def fill_text(self, w, s):
        if w.get() == s:
            w.delete(0, tk.END)

    def FileNameCheck(self):

        self.filename_entry.configure(bg="white")        

        file_name_entry = self.filename_entry.get()

        if file_name_entry == "" or file_name_entry == self.filename_entry_tt:
            self.image_name = None
            return

        name_regex = re.compile('^CON|(^[a-zA-Z0-9]+[^<>:"/|?*~%#+$!@,.();{}\[\]\\\]+[a-zA-Z0-9]$)') # want to be not None
        reserved_names_regex = re.compile("(^CON$|^PRN$|^AUX$|^NUL$|^COM\d{1}$|^LPT\d{1}$)") # want to be None

        name_result = name_regex.search(file_name_entry)
        reserved_name_result = reserved_names_regex.search(file_name_entry)

        if (name_result is not None) and (reserved_name_result is None):
            self.image_name = file_name_entry
        else:
            self.filename_entry.configure(bg="red")        

    def save_file(self):
        result = filedialog.askdirectory()

        if len(result) > 0:
            self.save_path = result
            self.path_provided = True
            self.UpdateStatus()
       
    def UpdateFormat(self):

        format_dict = {"JPG":".jpg", "PNG":".png", "EPS":".eps"}
        self.save_format = format_dict[self.format_var.get()]

    def SetBrushSize(self):
        self.brush_size = int(self.brush_size_slider.get())

    def StartIndex(self):
        
        self.start_idx.configure(bg="white")

        if self.start_idx.get() == "":
            return

        try:
            if int(self.start_idx.get()) < 0:
                self.start_idx.configure(bg="red")
            self.EndIndex() 
            self.StartEndCheck()
        except:
            self.start_idx.configure(bg="red")
            self.StartEndCheck()

    def EndIndex(self):

        self.end_idx.configure(bg="white")
        
        if self.end_idx.get() == "" or self.end_idx.get() == self.end_idx_tt:
            return

        try:
            if int(self.start_idx.get()) >= int(self.end_idx.get()) or int(self.end_idx.get()) < 0 :
                self.end_idx.configure(bg="red") # end wrong cause too small
            self.StartEndCheck()
        except:
            try:
                if int(self.end_idx.get()) <= 0:
                    self.end_idx.configure(bg="red")    
            except:
                self.end_idx.configure(bg="red") # end wrong cause non int
            self.StartEndCheck()

    def StartEndCheck(self):
 
        try:
            if int(self.start_idx.get()) < int(self.end_idx.get()) and int(self.start_idx.get()) >= 0:
                self.n_images = int(self.end_idx.get()) - int(self.start_idx.get()) + 1
                self.UpdateStatus()
            else:
                self.n_images = None
                self.UpdateStatus()
        except:
            self.n_images = None
            self.UpdateStatus()


    def CbCheck(self):

        state_sum = 0
        for cb_i in self.cb_dict.values():
            state_sum += cb_i.get()

        if state_sum == 2:

            for cb_i,int_var_i in self.cb_dict.items():
                if int_var_i.get():
                    cb_i.configure(state= tk.DISABLED)
        else:
        
            for cb_i,int_var_i in self.cb_dict.items():
                if int_var_i.get():
                    cb_i.configure(state= tk.NORMAL)


    def UpdateStatus(self):
        status_string = f"size = {self.image_size} | nr. images = {self.n_images} | path set = {self.path_provided}"
        status_label = tk.Label(self.settings, text= status_string, relief= tk.SUNKEN, width= 50)
        status_label.grid(row=8, column=0, columnspan=2)

    def ErrorBar(self, err):

        err = "Errors; "+err
        self.error_bar = tk.Label(self.settings, text= err, width= 50)
        self.error_bar.grid(row=9, column=0, columnspan=2)

    def SaveSettings(self):

        err = ""

        if self.image_size is None:
            err += "no size, "
        if self.image_name is None:
            err += "no name, "
        if self.n_images is None:
            err += "no images, "
        if not self.path_provided:
            err += "no path"

        if len(err) > 0:
            self.ErrorBar(err)
            return


        # Generated digits
        for digit,int_var in enumerate(self.cb_dict.values()):
            if int_var.get():
                self.generated_digits.append(digit)
                         
        self.s_idx = int(self.start_idx.get())
        self.e_idx = int(self.end_idx.get())
        self.destroy()
        self.PaintLoop()

    def destroy(self):
        self.settings.destroy()


    def InitializeWindow(self, button_width = 25, button_pad_x = 5, button_pad_y = 10):
                
        self.settings = tk.Tk() # Settings window start
        self.settings.title("Settings for MNIST maker")
        self.settings.resizable(False, False)

        
        ##### ROW 0 #####

        # Image size buttons
        self.image_size32_btn = tk.Button(self.settings, command= lambda:self.ImageSizeButton(32), text= "32x32", width= button_width, padx= button_pad_x, pady= button_pad_y)
        self.image_size32_btn.grid(row=0,column=0)

        self.image_size64_btn = tk.Button(self.settings, command= lambda:self.ImageSizeButton(64), text= "64x64", width= button_width, padx= button_pad_x, pady= button_pad_y)
        self.image_size64_btn.grid(row=0,column=1)

        ##### ROW 1 #####

        self.image_size128_btn = tk.Button(self.settings, command= lambda:self.ImageSizeButton(128), text= "128x128", width= button_width, padx= button_pad_x, pady= button_pad_y)
        self.image_size128_btn.grid(row=1,column=0)

        self.image_size256_btn = tk.Button(self.settings, command= lambda:self.ImageSizeButton(256), text= "256x256", width= button_width, padx= button_pad_x, pady= button_pad_y)
        self.image_size256_btn.grid(row=1,column=1)


        ##### ROW 2 #####


        # Custom image size
        self.custom_size_tt = "Custom image size"
        self.custom_size = tk.Entry(self.settings, width= button_width)
        self.custom_size.insert(0, self.custom_size_tt)
        self.custom_size.grid(row=2,column=0, ipady= 4, pady= 5)
        self.custom_size.bind("<FocusIn>", lambda e: self.fill_text(self.custom_size, self.custom_size_tt))
        self.custom_size.bind("<FocusOut>", lambda e: self.ImageSize(self.custom_size.get()), add="+")
        self.custom_size.bind("<FocusOut>", lambda e: self.temp_text(self.custom_size, self.custom_size_tt), add="+")
        

        # Image name
        self.filename_entry_tt = "Image name"
        self.filename_entry = tk.Entry(self.settings, width= button_width)
        self.filename_entry.insert(0, self.filename_entry_tt)
        self.filename_entry.grid(row=2,column=1, ipady= 4, pady= 5)
        self.filename_entry.bind("<FocusIn>", lambda e: self.fill_text(self.filename_entry, self.filename_entry_tt))
        self.filename_entry.bind("<FocusOut>", lambda e: self.FileNameCheck(), add="+")
        self.filename_entry.bind("<FocusOut>", lambda e: self.temp_text(self.filename_entry, self.filename_entry_tt), add="+")
        

        ##### ROW 3 #####

        # Checkbox buttons frame
        self.digit_frame = tk.Frame(self.settings, width= 2*button_width)
        self.digit_frame.grid(row=3, column=0, columnspan=2)

        # Checkbox digits
        self.cb_dict = {}

        for checkbutton_idx in range(10):

            cb_str = str(checkbutton_idx)
            cb_var = tk.IntVar()

            cb = tk.Checkbutton(self.digit_frame, text= cb_str, variable= cb_var, command= self.CbCheck)
            cb.select()
            cb.grid(row=0, column=checkbutton_idx)

            self.cb_dict[cb] = cb_var

        # Background color checkbox
        self.cb_background = tk.IntVar()
        cb = tk.Checkbutton(self.digit_frame, text= "bg", variable= self.cb_background, padx= 5)
        cb.select()
        cb.grid(row=0, column=10)



        ##### ROW 4 #####

        # Brush scale
        self.brush_size_slider = tk.Scale(self.settings, from_= 1, to= 25, orient= tk.HORIZONTAL, label="Brush size", length= 300, command= lambda e: self.SetBrushSize())
        self.brush_size_slider.set(12)
        self.brush_size_slider.grid(row=4,column=0, columnspan=2)


        ##### ROW 5 #####

        # Start and end index
        self.start_idx_tt = "Start index"
        self.start_idx = tk.Entry(self.settings, width= button_width)
        self.start_idx.insert(0, self.start_idx_tt)
        self.start_idx.grid(row=5, column=0, ipady= 4, pady= 5)
        self.start_idx.bind("<FocusIn>", lambda e: self.fill_text(self.start_idx, self.start_idx_tt))
        self.start_idx.bind("<FocusOut>", lambda e: self.StartIndex(), add="+")
        self.start_idx.bind("<FocusOut>", lambda e: self.temp_text(self.start_idx, self.start_idx_tt), add="+")
        

        self.end_idx_tt = "End index"
        self.end_idx = tk.Entry(self.settings, width= button_width)
        self.end_idx.insert(0, self.end_idx_tt)
        self.end_idx.grid(row=5, column=1, ipady= 4, pady= 5)
        self.end_idx.bind("<FocusIn>", lambda e: self.fill_text(self.end_idx, self.end_idx_tt))
        self.end_idx.bind("<FocusOut>", lambda e: self.EndIndex(), add="+")
        self.end_idx.bind("<FocusOut>", lambda e: self.temp_text(self.end_idx, self.end_idx_tt), add="+")
        

        ##### ROW 6 #####

        # Save data file location selector
        self.path_button = tk.Button(self.settings, text="Save path", width= button_width, command= self.save_file, padx= button_pad_x, pady= button_pad_y)
        self.path_button.grid(row=6,column=0)

        # File format drop down menu
        self.format_var = tk.StringVar()
        self.format_var.set("JPG")
        formats = ["JPG", "PNG", "EPS"]
        self.file_format = tk.OptionMenu(self.settings, self.format_var, *formats, command= lambda e: self.UpdateFormat())
        self.file_format.grid(row=6,column=1, ipadx= 2*button_width+button_pad_x, ipady= 8)


        ##### ROW 7 #####

        # save settings and move on to painting
        self.save_button = tk.Button(self.settings, text="Save settings", command= lambda: self.SaveSettings(), width= 2*button_width, padx= button_pad_x, pady= button_pad_y)
        self.save_button.grid(row=7, column=0, columnspan=2)


        ##### ROW 8 #####

        # status
        self.status_string = f"size = {self.image_size} | nr. images = {self.n_images} | path set = {self.path_provided}"
        self.status_label = tk.Label(self.settings, text= self.status_string, relief= tk.SUNKEN, width= 50)
        self.status_label.grid(row=8, column=0, columnspan=2, pady= 10)


        self.settings.mainloop() # Settings window exit

    def PaintLoop(self):
            paint_obj = PaintGUI(settings= self)



class PaintGUI():

    def __init__(self, settings) :
        
        # Transfer variables
        self.settings = settings
        self.image_full_path = self.settings.save_path + "/Images/" + self.settings.image_name + "_" # only need image index
        self.paint_digit = random.choice(self.settings.generated_digits)
        self.labels = []
        self.canvas_size = 600
        self.fg_color = "black"
        self.bg_color = "white"
        self.grey = "#808080"
        self.new_c = 255
        self.image_index = settings.s_idx
        self.start_index = settings.s_idx
        self.end_index = settings.e_idx

        # Background colors
        if self.settings.cb_background.get(): # black background
            self.fg_color, self.bg_color = self.bg_color, self.fg_color
            self.new_c = 0

        # Create folder for images
        if not os.path.exists(self.settings.save_path + "/Images"):
            os.makedirs(self.settings.save_path + "/Images")

        # Create drawing canvas canvas
        self.root = tk.Tk()
        self.root.configure(background= self.grey)
        self.root.state("zoomed")
        self.root.title("MNIST maker [S]ave image, [R]eset image, [U]ndo image")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Canvas keybinds
        self.root.bind("<KeyPress-R>", lambda e: self.Clear(), add="+")
        self.root.bind("<KeyPress-r>", lambda e: self.Clear(), add="+")
        self.root.bind("<KeyPress-S>", lambda e: self.Increment(), add="+")
        self.root.bind("<KeyPress-s>", lambda e: self.Increment(), add="+")
        self.root.bind("<KeyPress-U>", lambda e: self.Undo(), add="+")
        self.root.bind("<KeyPress-u>", lambda e: self.Undo(), add="+")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Painting Canvas
        self.canvas = tk.Canvas(self.root, width= self.canvas_size, height= self.canvas_size, bg= self.bg_color, cursor= "circle")
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.place(x= screen_width // 2, y= screen_height // 2, anchor= tk.CENTER)

        # Digit Label
        self.digit_label = tk.Label(self.root, text= str(self.paint_digit), font= ("Arial", 75), bg= self.grey)
        self.digit_label.place(x= screen_width // 2, y= screen_height // 2 - 400, anchor= tk.CENTER)

        # Progress label
        self.progress_label = tk.Label(self.root, text= f"{self.image_index-self.start_index} / {self.settings.n_images}", font= ("Arial", 25), bg= self.grey)
        self.progress_label.place(x= screen_width // 2, y= screen_height // 2 + 400, anchor= tk.CENTER)

        # Pillow image used for saving
        self.image = PIL.Image.new("L", (self.canvas_size, self.canvas_size), color= self.new_c) 
        self.draw = PIL.ImageDraw.Draw(self.image)

        self.root.mainloop()


    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        brush_size = self.settings.brush_size
        self.canvas.create_rectangle(x1,y1,x2,y2, outline= self.fg_color, fill= self.fg_color, width= brush_size)
        self.draw.rectangle([x1, y1, x2+brush_size, y2+brush_size], outline= self.fg_color, fill= self.fg_color, width= brush_size)

    def Clear(self): # Triggered when pressing R or after saving
        self.canvas.delete("all")
        self.image = PIL.Image.new("L", (self.canvas_size, self.canvas_size), color= self.new_c)
        self.draw = PIL.ImageDraw.Draw(self.image)

    def Undo(self):

        if len(self.labels) > 0:
            self.labels.pop()
            self.image_index -= 1
            os.remove(self.image_full_path+str(self.image_index)+self.settings.save_format)
            self.Clear()
            self.paint_digit = random.choice(self.settings.generated_digits)
            self.digit_label.configure(text= str(self.paint_digit))
            self.progress_label.configure(text= f"{self.image_index-self.start_index} / {self.settings.n_images}")

    def Increment(self): # Triggered when pressing S
        
        rescaled_image = self.image.resize((self.settings.image_size, self.settings.image_size))
        rescaled_image.save(self.image_full_path+str(self.image_index)+self.settings.save_format)
        self.labels.append(self.paint_digit)
        self.image_index += 1
        if self.image_index > self.end_index:
            self.EndProgram()

        self.Clear()
        self.paint_digit = random.choice(self.settings.generated_digits)
        self.digit_label.configure(text= str(self.paint_digit))
        self.progress_label.configure(text= f"{self.image_index-self.start_index} / {self.settings.n_images}")

    def on_closing(self):
        message_string = f"Save current image and quit? \n You have done {self.image_index-self.start_index} / {self.settings.n_images} images"
        answer = messagebox.askyesnocancel("Quit", message_string)
        if answer is not None:
            if answer:
                self.Increment()
            
            self.EndProgram()


    def EndProgram(self):

        os.chdir(self.settings.save_path)

        # export labels to csv before destroying
        if  len(self.labels) > 0:
            filename_csv = "labels_"+str(self.start_index)+"_"+str(self.end_index)+".csv"
            if not os.path.exists(filename_csv):
                with open(filename_csv,'w', newline='') as f:
                    write = csv.writer(f)
                    write.writerows([self.labels])
        else:
            os.rmdir("Images")

        self.root.destroy()
        exit(0)


if __name__ == '__main__':
    mnist_maker = MNIST_Maker()

