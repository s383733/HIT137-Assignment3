#Create a Tkinter application using the concepts of object-oriented programming, such as, multiple inheritance, multiple decorators, encapsulation, polymorphism, and method overriding, etc.

import tkinter as tk        #Importing tkinter which will be used to create the GUI application
from tkinter import filedialog  #Import filedialog which will be used for creating file selection windows
from PIL import Image, ImageTk  #Import PIL for image handling within GUI
from ultralytics import YOLO #Importing our simple AI model that will be incorporated in the application

class AI_app:
    def __init__(self, root):
        self.root = root        #Initialise root window
        self.root.title("Animal Detection Service")     #Give a title to the window

        self.about = tk.Button(root, text = "About")#, command = self.about_message) 
        self.about.grid(row=10, column=1, padx=5, pady=5)

        self.dowload_app = tk.Button(root, text = "Download the App")#, command = self.download_app_link)
        self.dowload_app.grid(row=10, column=2, padx=5, pady=5)

        self.terms_of_service = tk.Button(root, text= "Terms of Service")#, command = self.terms_of_service_message)
        self.terms_of_service.grid(row=10, column=3, padx=5, pady=5)

        self.privacy_policy = tk.Button(root, text= "Terms of Service")#, command = self.privacy_policy_message)
        self.privacy_policy.grid(row=10, column=4, padx=5, pady=5)

        self.help_centre = tk.Button(root, text= "Terms of Service")#, command = self.help_centre_message)
        self.help_centre.grid(row=10, column=5, padx=5, pady=5)

        self.upload_label = tk.Label(root, text = "Upload Your Image")      #Create a label for image uploading
        self.upload_label.grid(row=1, column=1, padx=5, pady=5)       #Pack the label into the window

        self.upload_button = tk.Button(root, text = "Upload", command = self.upload_image)  #Create a button for image uploading
        self.upload_button.grid(row=1, column=2, padx=5, pady=5)      #Pack the button within the window

        self.predict_label = tk.Label(root, text = "Predict the Animals")      #Create a label for image uploading
        self.predict_label.grid(row=2, column=1, padx=5, pady=5)       #Pack the label into the window

        self.predict_button = tk.Button(root, text = "Predict", command = self.detect_animal)  #Create a button to initiate animal prediciton
        self.predict_button.grid(row=2, column=2, padx=5, pady=5)      #Pack the button within the window

        self.result_label = tk.Label(root, text = "")   #Create a label for the results
        self.result_label.grid(row=3, column=1, padx=5, pady=5)    #Pack label within the window

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