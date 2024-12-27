import os
import random
import string
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import openpyxl
from openpyxl import Workbook

# Function to hide text in an image using LSB steganography
def hide_text_in_image(image_path, text, output_path):
    image = Image.open(image_path).convert('RGB')
    binary_text = ''.join(format(ord(char), '08b') for char in text) + '1111111111111110'  # EOF marker

    pixels = list(image.getdata())
    pixel_index = 0
    new_pixels = []

    for i, pixel in enumerate(pixels):
        if pixel_index < len(binary_text):
            r, g, b = pixel
            r = (r & ~1) | int(binary_text[pixel_index])
            pixel_index += 1
            new_pixels.append((r, g, b))
        else:
            new_pixels.append(pixel)

    image.putdata(new_pixels)
    image.save(output_path)


# GUI Application class
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StegMake")  # Set the title
        self.root.configure(bg="black")  # Dark background
        self.root.resizable(False, False)  # Fixed window size

        # Paths
        self.images_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.excel_path = tk.StringVar()
        self.start_number = tk.IntVar(value=1)  # Default starting number for renaming

        # GUI layout
        self.create_widgets()

    def create_widgets(self):
        # Title label with hacker-style font
        tk.Label(self.root, text="StegMake", bg="black", fg="limegreen", font=("Anonymous Pro", 24, "bold")).grid(row=0,
                                                                                                                  column=0,
                                                                                                                  columnspan=3,
                                                                                                                  pady=20)

        tk.Label(self.root, text="Path to Images:", bg="black", fg="limegreen", font=("Anonymous Pro", 12)).grid(row=1,
                                                                                                                 column=0,
                                                                                                                 padx=10,
                                                                                                                 pady=5,
                                                                                                                 sticky='w')
        tk.Entry(self.root, textvariable=self.images_path, width=50, bg="black", fg="limegreen",
                 insertbackground="limegreen", font=("Anonymous Pro", 12)).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_images, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Anonymous Pro", 12)).grid(row=1, column=2, padx=10, pady=5)

        tk.Label(self.root, text="Output Path:", bg="black", fg="limegreen", font=("Anonymous Pro", 12)).grid(row=2,
                                                                                                              column=0,
                                                                                                              padx=10,
                                                                                                              pady=5,
                                                                                                              sticky='w')
        tk.Entry(self.root, textvariable=self.output_path, width=50, bg="black", fg="limegreen",
                 insertbackground="limegreen", font=("Anonymous Pro", 12)).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_output, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Anonymous Pro", 12)).grid(row=2, column=2, padx=10, pady=5)

        tk.Label(self.root, text="Excel File Path:", bg="black", fg="limegreen", font=("Anonymous Pro", 12)).grid(row=3,
                                                                                                                  column=0,
                                                                                                                  padx=10,
                                                                                                                  pady=5,
                                                                                                                  sticky='w')
        tk.Entry(self.root, textvariable=self.excel_path, width=50, bg="black", fg="limegreen",
                 insertbackground="limegreen", font=("Anonymous Pro", 12)).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_excel, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Anonymous Pro", 12)).grid(row=3, column=2, padx=10, pady=5)

        tk.Label(self.root, text="Starting Number for Renaming:", bg="black", fg="limegreen", font=("Anonymous Pro", 12)).grid(row=4,
                                                                                                                  column=0,
                                                                                                                  padx=10,
                                                                                                                  pady=5,
                                                                                                                  sticky='w')
        tk.Entry(self.root, textvariable=self.start_number, width=10, bg="black", fg="limegreen", font=("Anonymous Pro", 12)).grid(row=4, column=1, padx=10, pady=5)

        self.console = tk.Text(self.root, height=10, state='disabled', bg='black', fg='limegreen',
                               font=("Courier", 12))  # Changed font to Courier
        self.console.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

        self.progress = ttk.Progressbar(self.root, orient='horizontal', mode='determinate', length=400)
        self.progress.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        tk.Button(self.root, text="Start", command=self.start_processing, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Anonymous Pro", 12)).grid(row=7, column=1, pady=10)

    def browse_images(self):
        path = filedialog.askdirectory()
        if path:
            self.images_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def browse_excel(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.excel_path.set(path)

    def log_to_console(self, message):
        self.console.configure(state='normal')
        self.console.insert(tk.END, message + "\n\n")  # Added empty line after every log message
        self.console.configure(state='disabled')
        self.console.see(tk.END)

    def start_processing(self):
        images_path = self.images_path.get()
        output_path = self.output_path.get()
        excel_path = self.excel_path.get()
        starting_number = self.start_number.get()

        if not os.path.isdir(images_path):
            messagebox.showerror("Error", "Invalid images folder path.")
            return

        if not os.path.isdir(output_path):
            messagebox.showerror("Error", "Invalid output folder path.")
            return

        if not excel_path:
            messagebox.showerror("Error", "Invalid Excel file path.")
            return

        # Create Excel file
        wb = Workbook()
        ws = wb.active
        ws.append(["Image Name", "Hidden Message"])

        images = [f for f in os.listdir(images_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        self.progress['maximum'] = len(images)

        for i, image_name in enumerate(images, starting_number):
            image_path = os.path.join(images_path, image_name)
            new_image_name = f"hidden_{i}_{image_name}"
            output_image_path = os.path.join(output_path, new_image_name)

            hidden_text = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            hide_text_in_image(image_path, hidden_text, output_image_path)

            ws.append([image_name, hidden_text])
            self.log_to_console(f"Processed: {new_image_name}, Hidden Text: {hidden_text}")
            self.progress['value'] = i - starting_number + 1
            self.root.update_idletasks()

        wb.save(excel_path)
        messagebox.showinfo("Success", "Processing complete!")

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
