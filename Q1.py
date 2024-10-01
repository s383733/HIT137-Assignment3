#Create a Tkinter application using the concepts of object-oriented programming, such as, multiple inheritance, multiple decorators, encapsulation, polymorphism, and method overriding, etc.

import tkinter as tk        #Importing tkinter which will be used to create the GUI application
from tkinter import filedialog  #Import filedialog which will be used for creating file selection windows
from PIL import Image, ImageTk  #Import PIL for image handling within GUI
from ultralytics import YOLO #Importing our simple AI model that will be incorporated in the application

class AI_app:
    def __init__(self, root):
        self.root = root        #Initialise root window
        self.root.title("Image Classifier")     #Give a title to the window

        self.label = tk.Label(root, text = "Upload Image")      #Create a label for image uploading
        self.label.pack()       #Pack the label into the window

        self.upload_button = tk.Button(root, text = "Upload", command = self.upload_image)  #Create a button for image uploading
        self.upload_button.pack()       #Pack the button within the window

        self.predict_button = tk.Button(root, text = "Predict", command = self.detect_animal)  #Create a button to initiate animal prediciton
        self.predict_button.pack()      #Pack the button within the window

        self.result_label = tk.Label(root, text = "")   #Create a label for the results
        self.result_label.pack()    #Pack label within the window

        self.model = YOLO('yolov8x.pt')

    def upload_image(self):     #Create a method to upload images into the GUI
        file_path = filedialog.askopenfilename()    #Create an Open dialog and return opened file object
        self.image = Image.open(file_path)      
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(image = self.image_tk)
        self.image_label.pack()     #Pack the label into the window

    def detect_animal(self):    #Create a method to detect the animal(s) in the image
        prediction = self.model.predict(self.image)
        for result in prediction:
            print(result.boxes)
            result.show()

root = tk.Tk()
app = AI_app(root)
root.mainloop()