import tkinter as tk
from tkinter import messagebox
from langdetect import detect, DetectorFactory
from googletrans import Translator
from textblob import TextBlob
import time

# Ensures consistent language detection results
DetectorFactory.seed = 0
translator = Translator()

# Decorator to time the function execution
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken for {func.__name__}: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Language Detection and Sentiment Analysis Class
class LanguageDetector:
    def __init__(self):
        pass

    # Private method for detecting language (Encapsulation)
    @timing_decorator
    def _detect_language(self, text):
        try:
            # LangDetect library to detect language from input text
            language = detect(text)
            return language
        except Exception as e:
            return "Error detecting language: " + str(e)

    # Private method for sentiment analysis using TextBlob
    def _analyze_sentiment(self, text):
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity  # Sentiment polarity between -1 and 1
            if sentiment > 0:
                return "Positive"
            elif sentiment < 0:
                return "Negative"
            else:
                return "Neutral"
        except Exception as e:
            return "Error analyzing sentiment: " + str(e)

    # Private method to translate text to English using googletrans
    def _translate_to_english(self, text):
        try:
            detected_language = translator.detect(text).lang
            if detected_language == "en":
                return "Text is already in English."
            else:
                translated_text = translator.translate(text, dest="en")
                return translated_text.text
        except Exception as e:
            return "Error translating: " + str(e)

# Tkinter GUI class, inheriting from both Tk and LanguageDetector
class LanguageDetectionApp(tk.Tk, LanguageDetector):
    def __init__(self):
        tk.Tk.__init__(self)  # Initialize Tkinter
        LanguageDetector.__init__(self)  # Initialize LanguageDetector
        self.title("Language Detection, Translation & Sentiment Analysis")
        self.geometry("1024x640")
        self.configure(bg="#F0F8FF")  # Soft light blue background color

        # GUI Title
        self.title_label = tk.Label(self, text="Language Detection, Translation & Sentiment Analysis",
                                    font=("Arial", 20), bg="#4682B4", fg="white", pady=5)
        self.title_label.pack(fill=tk.X)

        # Project Info
        self.subtitle_label = tk.Label(self, text="A group project by Group 100",
                                       font=("Arial", 12), bg="#4682B4", fg="white")
        self.subtitle_label.pack(fill=tk.X)

        # Entry label
        self.input_label = tk.Label(self, text="Enter text (up to 200 words):", font=("Arial", 16), bg="#F0F8FF")
        self.input_label.pack(pady=5)

        # Text widget for inputting large amounts of text (up to 200 words)
        self.text_entry = tk.Text(self, height=5, width=80, font=("Arial", 14))  # size of input box
        self.text_entry.pack(pady=10)

        # Buttons for operations
        self.detect_button = tk.Button(self, text="Detect Language & Analyze", font=("Arial", 14), 
                                       command=self.detect_language)
        self.detect_button.pack(pady=10)

        # Output labels for results (Language & Sentiment on the same line)
        self.result_frame = tk.Frame(self, bg="#F0F8FF")
        self.result_frame.pack(pady=10)
        
        self.result_label = tk.Label(self.result_frame, text="Detected Language: ", font=("Arial", 16), bg="#F0F8FF")
        self.result_label.grid(row=0, column=0, padx=10)

        self.sentiment_label = tk.Label(self.result_frame, text="Sentiment Analysis: ", font=("Arial", 16), bg="#F0F8FF")
        self.sentiment_label.grid(row=0, column=1, padx=10)

        # Translation output box with text wrapping
        self.translation_label = tk.Label(self, text="English Translation:", font=("Arial", 16), bg="#F0F8FF")
        self.translation_label.pack(pady=10)

        self.translation_output = tk.Text(self, height=5, width=80, wrap="word", font=("Arial", 14), state=tk.DISABLED)
        self.translation_output.pack(pady=10)

        # Add some additional buttons at the bottom of the interface
        self.add_navigation_buttons()

    def add_navigation_buttons(self):
        # Create a frame to hold the navigation buttons
        nav_frame = tk.Frame(self, bg="#F0F8FF")
        nav_frame.pack(pady=20)
        
        # Create the navigation buttons
        buttons = [("About", self.about), 
                   ("Terms of Services", self.terms_of_services),
                   ("Download the App", self.download_app), 
                   ("Privacy Policy", self.privacy_policy),
                   ("Help Centre", self.help_centre), 
                   ("Feedback", self.feedback)]
        
        for name, command in buttons:
            tk.Button(nav_frame, text=name, font=("Tahoma", 10), command=command).pack(side=tk.LEFT, padx=10)

    # Method to detect language, analyze sentiment, and provide translation
    def detect_language(self):
        text = self.text_entry.get("1.0", tk.END).strip()  # Get all text from the Text widget
        if text:
            # Limit input to about 200 words
            if len(text.split()) > 200:
                messagebox.showwarning("Input Error", "Please limit your input to 200 words.")
            else:
                # Call the _detect_language method from LanguageDetector
                language = self._detect_language(text)
                sentiment = self._analyze_sentiment(text)
                translation = self._translate_to_english(text)

                # Display the results in respective labels
                self.result_label.config(text=f"Detected Language: {language}", fg="blue")
                self.sentiment_label.config(text=f"Sentiment Analysis: {sentiment}", fg="green" if sentiment == "Positive" else "red")

                # Display translation in the output box
                self.translation_output.config(state=tk.NORMAL)
                self.translation_output.delete("1.0", tk.END)  # Clear previous content
                self.translation_output.insert(tk.END, translation)
                self.translation_output.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    # Define simple command actions for the buttons
    def about(self):
        messagebox.showinfo("About", "This is a project created by Group 100 for Language Detection, Sentiment Analysis, and Translation.")

    def terms_of_services(self):
        messagebox.showinfo("Terms of Services", "Treat others how you would want to be treated.")

    def download_app(self):
        messagebox.showinfo("Download App", "Download link will be available soon, please come back later.")

    def privacy_policy(self):
        messagebox.showinfo("Privacy Policy", "Privacy policy information here.")

    def help_centre(self):
        messagebox.showinfo("Help Centre", "No help available at this time, good luck :)")

    def feedback(self):
        messagebox.showinfo("Feedback", "We'd love your Feedback on how we're doing.")

    # Method to quit the program
    def quit_program(self):
        self.destroy()

# Run the application
if __name__ == "__main__":
    app = LanguageDetectionApp()
    app.mainloop()
