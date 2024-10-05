#Create a Tkinter application using the concepts of object-oriented programming, such as, multiple inheritance, multiple decorators, encapsulation, polymorphism, and method overriding, etc.

import tkinter as tk        #Importing tkinter which will be used to create the GUI application
from tkinter import filedialog
from tkinter import messagebox  #Import filedialog which will be used for creating file selection windows
from PIL import Image, ImageTk  #Import PIL for image handling within GUI
from ultralytics import YOLO #Importing our simple AI model that will be incorporated in the application

class Login_to_App:
    def __init__(self, root):    
        self.root = root    #Initialise a root window for the login screen
        self.root.title("Sign in or Proceed as Guest")

        self.title_label = tk.Label(root, text = "Welcome! Please choose an option:")   #Create a title for login screen
        self.title_label.grid(row=0, column=0, pady=20)

        self.login_button = tk.Button(root, text = "Sign in and search", command = self.login_page)
        self.login_button.grid(row=1, column=0, padx=10, pady=10)

        self.guest_button = tk.Button(root, text = "Search as Guest", command = self.guest_mode)
        self.guest_button.grid(row=1, column=1, padx=10, pady=10)

        self.or_label = tk.Label(root, text = "-------- or ---------")
        self.or_label.grid(row=2, column=0, padx=20)

        self.sign_up_button = tk.Button(root, text = "Create Account", command = self.create_account_page)
        self.sign_up_button.grid(row=3, column=0, padx=20)
    
    def login_page(self):
        self.login_screen = tk.Toplevel(self.root)
        self.login_screen.title("Sign in")

        self.username_label = tk.Label(self.login_screen, text = "Username")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.password_label = tk.Label(self.login_screen, text = "Password")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)

        self.username_entry = tk.Entry(self.login_screen)
        self.username_entry.grid(row=0, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_screen, show = "*")
        self.password_entry.grid(row=1, column=0, padx=5, pady=5)

        self.sign_in_button = tk.Button(self.login_screen, text = "Sign In", command = self.check_login_details)
        self.sign_in_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def check_login_details(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "HIT137" and password == "Group100":
            messagebox.showinfo("Sign in successful")
            self.login_screen.destroy()
            self.open_AI_app(full_version = True)
        else:
            messagebox.showerror("Incorrect username or password")
            self.login_screen.destroy()

    def open_AI_app(self, full_version):
        self.root.withdraw()
        ai_window = tk.Toplevel(self.root)
        app = AI_app(ai_window, full_version)

    def guest_mode(self):
        self.open_AI_app(full_version = False)
    
    def create_account_page(self):
        self.create_account_screen = tk.Toplevel(self.root)
        self.create_account_screen.title("Please create an account to proceed")

        self.create_username_label = tk.Label(self.create_account_screen, text = "Please create a username")
        self.create_username_label.grid(row=0, column=0, padx=5, pady=5)
        self.create_password_label = tk.Label(self.create_account_screen, text = "Please create a password")
        self.create_password_label.grid(row=1, column=0, padx=5, pady=5)

        self.create_username_entry = tk.Entry(self.create_account_screen)
        self.create_username_entry.grid(row=0, column=0, padx=5, pady=5)
        self.create_password_entry = tk.Entry(self.create_account_screen)
        self.create_password_entry.grid(row=1, column=0, padx=5, pady=5)

        self.create_account_button = tk.Button(self.login_screen, text = "Finish creating account and return to log in", command = self.finish_creating_account)
        self.create_account_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    def finish_creating_account(self, full_version):
        self.account_created_message = messagebox.showinfo("Account created successfully")
        self.root.withdraw()
        ai_window = tk.Toplevel(self.root)
        app = AI_app(ai_window, full_version)

class AI_app:
    def __init__(self, root, full_version):
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

        if full_version:
            self.predict_label = tk.Label(root, text = "Predict the Animals")      #Create a label for image uploading
            self.predict_label.grid(row=2, column=1, padx=5, pady=5)       #Pack the label into the window
            
            self.predict_button = tk.Button(root, text = "Predict", command = self.detect_animal)  #Create a button to initiate animal prediciton
            self.predict_button.grid(row=2, column=2, padx=5, pady=5)      #Pack the button within the window
        else:
            self.guest_label = tk.Label(root, text = "Limited Access: No Prediction Available, please sign up for predictions")
            self.guest_label.grid(row=3, column=1, padx=5, pady=5)
        
        self.result_label = tk.Label(root, text = "")   #Create a label for the results
        self.result_label.grid(row=3, column=1, padx=5, pady=5)    #Pack label within the window

        if full_version:
            self.model = YOLO('yolov8x.pt')

    def upload_image(self):     #Create a method to upload images into the GUI
        file_path = filedialog.askopenfilename()    #Create an Open dialog and return opened file image
        self.image = Image.open(file_path)      #Open the image using PIL
        self.image_tk = ImageTk.PhotoImage(self.image)      #Converts the image to Tkinter format
        self.image_label = tk.Label(image = self.image_tk)      #Displays the image in the GUI
        self.image_label.pack()     #Pack the label into the window

    def detect_animal(self):    #Create a method to detect the animal(s) in the image
        prediction = self.model.predict(self.image)     #Assign model prediction to "prediction"
        for result in prediction:   
            print(result.boxes)     #print the boxes onto the image showing the classified animals
            result.show()       #Show the results and confidence for each box

root = tk.Tk()
login_app = Login_to_App(root)
root.mainloop()