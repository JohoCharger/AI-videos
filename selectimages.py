import tkinter as tk
from PIL import Image, ImageTk
import makemovie

# List of image paths (replace with your image paths)
image_paths1 = [
    {"filename": 'images/26-07-2024/Guardians-of-Time6dd27c.jpg', "caption": "Guardians of Time"},
    {"filename": 'images/26-07-2024/Guardians-of-Time33ea83.jpg', "caption": "Guardians of Time"},
    {"filename": 'images/26-07-2024/Guardians-of-Time308473.jpg', "caption": "Guardians of Time"},
    {"filename": 'images/26-07-2024/Secrets-of-the-Past2c14d0.jpg', "caption": "Secrets of the Past"},
    {"filename": 'images/26-07-2024/Guardians-of-Time33ea83.jpg', "caption": "Guardians of Time"},
    {"filename": 'images/26-07-2024/Guardians-of-Time308473.jpg', "caption": "Guardians of Time"},
]

selected_images = []

# Global variables
current_index = 0
selected_image = None

root = tk.Tk()
root.title("Image Selector")

# Create image labels
image_labels = []
for i in range(3):
    label = tk.Label(root, width=200, height=512, borderwidth=2, relief="solid")
    label.grid(row=0, column=i, padx=10, pady=10)
    image_labels.append(label)


def show_images(image_paths):
    global current_index, selected_image

    # Clear previous images
    for i in range(3):
        image_labels[i].config(image=None)

    # Load and display the next three images
    for i in range(3):
        idx = current_index + i
        if idx < len(image_paths):
            image = Image.open(image_paths[idx]["filename"])
            image = image.resize((288, 512), Image.LANCZOS)  # Resize image as needed
            photo = ImageTk.PhotoImage(image)
            image_labels[i].config(image=photo)
            image_labels[i].image = photo  # Keep reference to prevent garbage collection
            image_labels[i].bind("<Button-1>", lambda event, index=idx: choose_image(index, image_paths))
        else:
            break

    # Reset selected_image
    selected_image = None


def choose_image(index, image_paths):
    global selected_image
    selected_image = index
    selected_images.append(image_paths[index])
    next_images(image_paths)


def next_images(image_paths):
    global current_index
    current_index += 3
    if current_index >= len(image_paths):
        root.quit()
    show_images(image_paths)


def choose_images(imageList):
    # Show the initial set of images
    show_images(imageList)
    root.mainloop()


if __name__ == "__main__":
    choose_images(image_paths1)
    makemovie.make_movie(selected_images)
    print(selected_images)
