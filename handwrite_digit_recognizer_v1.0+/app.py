import tkinter as tk
import win32gui
from PIL import ImageGrab
import numpy as np
from digit_image_recognition import DigitImageRecognition as DIM

'''
    l = label
    b = button
'''

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # initialization
        self.x = 0
        self.y = 0
        self.canvas = tk.Canvas(self, width=300, height=300,
                                bg="white", cursor="cross")
        self.b_recognize = tk.Button(self, text="Recognize",
                                     command=self.recognize_handwriting)
        self.b_clear = tk.Button(self, text="Clear",
                                 command=self.clear_canvas)
        self.l_result = tk.Label(self, text="", font=('Arial', 24))

        # grid structure
        self.canvas.grid(row=0, column=0, columnspan=2, pady=2)
        self.b_recognize.grid(row=1, column=1, pady=2)
        self.b_clear.grid(row=1, column=0, pady=2)
        self.l_result.grid(row=2, column=0, columnspan=2, pady=2)

        # others
        # Note: B1-Motion means "The mouse is moved, with mouse button 1
        #  being held down (use B2 for the middle button,
        #  B3 for the right button)."
        # Reference:
        #  https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
        self.canvas.bind("<B1-Motion>", self.draw_lines)
        self.dim = DIM()
        self.model = self.dim.create_model()

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 12
        self.canvas.create_oval(self.x - r, self.y - r,
                                self.x + r, self.y + r, fill='black')

    def clear_canvas(self):
        self.canvas.delete("all")

    def capture_canvas(self):
        # get the handle of the canvas itself
        HWND = self.canvas.winfo_id()

        # get the coordinates of the canvas
        rect = win32gui.GetWindowRect(HWND)

        # grabs the image in the coordinates
        img = ImageGrab.grab(rect)

        return img

    def image_processing(self, img):
        # crop the outer border by a bit
        cropped_img = img.crop((1, 1, 299, 299))

        # resize to 8 x 8 to match dataset
        resized_img = cropped_img.resize((8, 8))

        # convert rgb to grayscale
        grayscaled_img = resized_img.convert('L')

        # change value of image array to fit in with dataset
        img_arr = np.array(grayscaled_img)
        reformed_img = -img_arr + 255
        return reformed_img

    # predict function reads in 2D arrays, but it cannot read arrays in array
    # except for the dataset itself (not sure why)
    # this opens all the arrays and merge them into 1
    def merging_arrays(self, img):
        one_arr_img = [[]]
        for i in img:
            for j in i:
                one_arr_img[0].append(j)
        return one_arr_img

    def recognize_handwriting(self):
        img = self.capture_canvas()
        processed_img = self.image_processing(img)
        reshaped_img_arr = self.merging_arrays(processed_img)
        result = self.model.predict(reshaped_img_arr)
        self.l_result.configure(text=str(result))
