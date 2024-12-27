import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image


# Function to extract hidden message from an image using LSB steganography
def check_hidden_data(image_path):
    image = Image.open(image_path).convert('RGB')
    pixels = list(image.getdata())

    binary_message = ''
    for pixel in pixels:
        r, g, b = pixel
        binary_message += str(r & 1)  # Check the LSB of the red channel

    # Look for EOF marker (binary '1111111111111110')
    eof_marker = '1111111111111110'
    message_end = binary_message.find(eof_marker)

    if message_end != -1:
        hidden_message = binary_message[:message_end]
        hidden_message = ''.join(chr(int(hidden_message[i:i + 8], 2)) for i in range(0, len(hidden_message), 8))
        return hidden_message
    else:
        return None


# Function to clean hidden data from the image
def clean_hidden_data(image_path, output_path):
    image = Image.open(image_path).convert('RGB')
    pixels = list(image.getdata())

    # Cleaning the LSB from the red channel
    new_pixels = [(r & ~1, g, b) for r, g, b in pixels]
    image.putdata(new_pixels)
    image.save(output_path)


# Log output to the console with colors for different types of messages
def log_to_console(console, message, message_type, image_name):
    color = "limegreen"  # Default color for all text
    if message_type == "info":
        color = "cyan"
    elif message_type == "error":
        color = "red"
    elif message_type == "success":
        color = "green"

    console.configure(state='normal')
    console.insert(tk.END, f"{image_name}: {message}\n", ("color",))
    console.configure(state='disabled')
    console.see(tk.END)


# GUI Application class for ImgRevive
class ImgReviveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ImgRevive Tool")
        self.root.configure(bg="black")
        self.root.resizable(False, False)  # Fixed window size

        # Paths
        self.input_images_path = tk.StringVar()
        self.output_images_path = tk.StringVar()

        # GUI layout
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Input Images Folder Path:", bg="black", fg="limegreen").grid(row=0, column=0, padx=10,
                                                                                               pady=5, sticky='w')
        tk.Entry(self.root, textvariable=self.input_images_path, width=50, bg="black", fg="limegreen",
                 insertbackground="limegreen").grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_input_folder, bg="black", fg="limegreen").grid(row=0,
                                                                                                               column=2,
                                                                                                               padx=10,
                                                                                                               pady=5)

        tk.Label(self.root, text="Output Images Folder Path:", bg="black", fg="limegreen").grid(row=1, column=0,
                                                                                                padx=10, pady=5,
                                                                                                sticky='w')
        tk.Entry(self.root, textvariable=self.output_images_path, width=50, bg="black", fg="limegreen",
                 insertbackground="limegreen").grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_output_folder, bg="black", fg="limegreen").grid(row=1,
                                                                                                                column=2,
                                                                                                                padx=10,
                                                                                                                pady=5)

        self.console = tk.Text(self.root, height=15, width=80, state='disabled', bg='black', fg='limegreen',
                               font=("Courier", 12))
        self.console.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

        self.progress = ttk.Progressbar(self.root, orient='horizontal', mode='determinate', length=400)
        self.progress.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        tk.Button(self.root, text="Start Revive Process", command=self.start_revive, bg="black", fg="limegreen").grid(
            row=4, column=1, pady=10)

    def browse_input_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.input_images_path.set(path)

    def browse_output_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.output_images_path.set(path)

    def start_revive(self):
        input_folder = self.input_images_path.get()
        output_folder = self.output_images_path.get()

        if not os.path.isdir(input_folder):
            messagebox.showerror("Error", "Invalid input folder path.")
            return

        if not os.path.isdir(output_folder):
            messagebox.showerror("Error", "Invalid output folder path.")
            return

        images = [f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        self.progress['maximum'] = len(images)

        for i, image_name in enumerate(images, 1):
            image_path = os.path.join(input_folder, image_name)
            output_image_path = os.path.join(output_folder, f"revived_{image_name}")

            hidden_data = check_hidden_data(image_path)

            if hidden_data:
                log_to_console(self.console, f"Hidden data found in {image_name}: {hidden_data}", message_type="info",
                               image_name=image_name)
                clean_hidden_data(image_path, output_image_path)
                log_to_console(self.console, f"Hidden data cleaned and image saved as {output_image_path}",
                               message_type="success", image_name=image_name)
            else:
                log_to_console(self.console, f"No hidden data in {image_name}", message_type="info",
                               image_name=image_name)

            self.progress['value'] = i
            self.root.update_idletasks()

        messagebox.showinfo("Revive Process Complete", "Revive process complete! Images saved to the output folder.")


# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = ImgReviveApp(root)
    root.mainloop()
