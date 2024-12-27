import tkinter as tk
from tkinter import messagebox
import subprocess

# GUI Application class
class WelcomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to StegApp")  # Set the title
        self.root.configure(bg="black")  # Dark background
        self.root.resizable(False, False)  # Fixed window size

        # GUI layout
        self.create_widgets()

    def create_widgets(self):
        # Smiley face with text above the buttons
        tk.Label(self.root, text="😊 Welcome to Cypher StegApp! 😊", bg="black", fg="limegreen", font=("Courier", 16)).grid(row=0, column=0, columnspan=3, pady=20)

        # Welcome label with warm messages
        tk.Label(self.root, text="Here's all about LSB in Img!", bg="black", fg="limegreen", font=("Courier", 24, "bold")).grid(row=1,
                                                                                                                       column=0,
                                                                                                                       columnspan=3,
                                                                                                                       pady=20)

        tk.Label(self.root, text="Hello! What would you like to do today?", bg="black", fg="limegreen", font=("Courier", 16)).grid(row=2,
                                                                                                                            column=0,
                                                                                                                            columnspan=3,
                                                                                                                            pady=10)

        # Buttons for StegMake, StegAnalyze, and ImgRevive
        tk.Button(self.root, text="StegMake", command=self.run_stegmake, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Courier", 14), width=20).grid(row=3, column=0, pady=20)

        tk.Button(self.root, text="StegAnalyze", command=self.run_steganalyze, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Courier", 14), width=20).grid(row=3, column=1, pady=20)

        tk.Button(self.root, text="ImgRevive", command=self.run_imgrevive, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Courier", 14), width=20).grid(row=3, column=2, pady=20)

        # Copyright Notice at the bottom of the window
        tk.Label(self.root, text="© AmrAhmedSanad 2024. All rights reserved.", bg="black", fg="limegreen", font=("Courier", 10)).grid(row=4, column=0, columnspan=3, pady=20)

    # Function to run StegMake
    def run_stegmake(self):
        self.run_script("StegMake.py")

    # Function to run StegAnalyze
    def run_steganalyze(self):
        self.run_script("StegAnalyze.py")

    # Function to run ImgRevive
    def run_imgrevive(self):
        self.run_script("ImgRevive.py")

    # Function to run Python scripts
    def run_script(self, script_name):
        try:
            subprocess.run(["python", script_name], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run {script_name}. Please make sure the file exists.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"{script_name} not found. Please ensure the script is in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomeApp(root)
    root.mainloop()
