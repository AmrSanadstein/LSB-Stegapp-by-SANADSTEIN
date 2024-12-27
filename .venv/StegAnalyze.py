import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import openpyxl
from openpyxl.styles import PatternFill
import re


# Function to sanitize the extracted text (remove any illegal characters)
def sanitize_text(text):
    # Remove any non-printable characters or control characters
    return re.sub(r'[^\x20-\x7E]', '', text)


# Function to extract hidden text from an image using LSB steganography
def extract_text_from_image(image_path):
    image = Image.open(image_path).convert('RGB')
    pixels = list(image.getdata())
    binary_text = ""

    for pixel in pixels:
        r, g, b = pixel
        binary_text += str(r & 1)  # Extract the least significant bit of the red channel

    # Find the end-of-file marker (EOF) in the binary string
    eof_marker = '1111111111111110'
    binary_text = binary_text.split(eof_marker)[0]

    # If there's no binary data before the EOF marker, treat it as empty text
    if len(binary_text) == 0:
        return ""

    # Convert binary to text
    extracted_text = ""
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i + 8]
        if len(byte) == 8:
            extracted_text += chr(int(byte, 2))

    # Sanitize the extracted text to remove any illegal characters
    return sanitize_text(extracted_text)


# Function to determine if the extracted text is clear or contains hidden data
def is_clear(extracted_text):
    # If the extracted text is empty, or if it consists of non-printable characters, it's considered clear
    if not extracted_text or len(extracted_text.strip()) == 0:
        return True
    return False


# GUI Application class
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StegAnalyze")  # Set the title to "StegAnalyze"
        self.root.configure(bg="black")  # Dark background
        self.root.resizable(False, False)  # Fixed window size

        # Paths
        self.images_path = tk.StringVar()
        self.excel_path = tk.StringVar()

        # GUI layout
        self.create_widgets()

    def create_widgets(self):
        # Title label with hacker-style font
        tk.Label(self.root, text="StegAnalyze", bg="black", fg="limegreen", font=("Anonymous Pro", 24, "bold")).grid(
            row=0,
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

        tk.Label(self.root, text="Excel File Path:", bg="black", fg="limegreen", font=("Anonymous Pro", 12)).grid(row=2,
                                                                                                                  column=0,
                                                                                                                  padx=10,
                                                                                                                  pady=5,
                                                                                                                  sticky='w')
        tk.Entry(self.root, textvariable=self.excel_path, width=50, bg="black", fg="limegreen",
                 insertbackground="limegreen", font=("Anonymous Pro", 12)).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_excel, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Anonymous Pro", 12)).grid(row=2, column=2, padx=10, pady=5)

        self.console = tk.Text(self.root, height=10, state='disabled', bg='black', fg='limegreen',
                               font=("Courier", 12))  # Changed font to Courier
        self.console.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

        self.progress = ttk.Progressbar(self.root, orient='horizontal', mode='determinate', length=400)
        self.progress.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        tk.Button(self.root, text="Start", command=self.start_processing, bg="black", fg="limegreen", relief="raised",
                  bd=3, font=("Anonymous Pro", 12)).grid(row=5, column=1, pady=10)

    def browse_images(self):
        path = filedialog.askdirectory()
        if path:
            self.images_path.set(path)

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
        excel_path = self.excel_path.get()

        if not os.path.isdir(images_path):
            messagebox.showerror("Error", "Invalid images folder path.")
            return

        if not excel_path:
            messagebox.showerror("Error", "Invalid Excel file path.")
            return

        # Create Excel file
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Image Name", "Status"])

        green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
        red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

        images = [f for f in os.listdir(images_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        self.progress['maximum'] = len(images)

        for i, image_name in enumerate(images):
            image_path = os.path.join(images_path, image_name)
            extracted_text = extract_text_from_image(image_path)

            # Check if the image is clear (i.e., contains no hidden text)
            if is_clear(extracted_text):
                ws.append([image_name, "Clear"])
                ws[f"B{i + 2}"].fill = green_fill  # Mark with green color if clear
            else:
                ws.append([image_name, extracted_text])
                ws[f"B{i + 2}"].fill = red_fill  # Mark with red color if there is hidden text

            self.log_to_console(f"Processed: {image_name}, Extracted Text: {extracted_text or 'No hidden text'}")
            self.progress['value'] = i + 1
            self.root.update_idletasks()

        wb.save(excel_path)
        messagebox.showinfo("Success", "Analysis complete!")


# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
