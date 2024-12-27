import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import random


# Function to hide the words in the image
def hide_words_in_image(image_path, output_path, words):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    draw = ImageDraw.Draw(img)

    # Set a font for the words (use a default font if unavailable)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()

    # Loop through each word and place it in a random position
    for word in words:
        word_width, word_height = draw.textsize(word, font)

        # Find a random position where the word can fit
        max_x = width - word_width
        max_y = height - word_height
        if max_x <= 0 or max_y <= 0:
            continue  # Skip if word can't fit in the image

        random_x = random.randint(0, max_x)
        random_y = random.randint(0, max_y)

        # Draw the word on the image
        draw.text((random_x, random_y), word, font=font, fill=(255, 255, 255))  # White text

    # Save the modified image
    img.save(output_path)
    print(f"Image saved at {output_path}")


# Function to select the input and output paths through a GUI
def select_files():
    # Set up the file dialog to choose input files (images)
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Select multiple image files
    input_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not input_paths:
        print("No images selected!")
        return

    # Select the folder to save the output images
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        print("No output folder selected!")
        return

    # Words to hide
    words = ["This", "Data", "Set", "is", "Fake", "and", "Useless"]

    # Process each image
    for input_path in input_paths:
        # Generate output path
        output_path = f"{output_folder}/{input_path.split('/')[-1]}"

        # Call the function to hide the words in the image
        hide_words_in_image(input_path, output_path, words)


if __name__ == "__main__":
    select_files()
