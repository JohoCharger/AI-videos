import tkinter as tk
from PIL import Image, ImageTk

# List of image paths (replace with your image paths)
image_paths = [
    'Guardians-of-the-Past2c9ccc.jpg',
    'Guardians-of-the-Past66c07c.jpg',
    'Guardians-of-the-Past716863.jpg',
    'Temporal-Protectors2c904b.jpg',
    'Temporal-Protectors8a9514.jpg',
    'Temporal-Protectors8c85b9.jpg'
]

# Global variables
current_index = 0
selected_image = None


def show_images():
    global current_index, selected_image

    # Clear previous images
    for i in range(3):
        image_labels[i].config(image=None)

    # Load and display the next three images
    for i in range(3):
        idx = current_index + i
        if idx < len(image_paths):
            image = Image.open("images/23-07-2024/" + image_paths[idx])
            image = image.resize((288, 512), Image.LANCZOS)  # Resize image as needed
            photo = ImageTk.PhotoImage(image)
            image_labels[i].config(image=photo)
            image_labels[i].image = photo  # Keep reference to prevent garbage collection
            image_labels[i].bind("<Button-1>", lambda event, index=idx: choose_image(index))
        else:
            break

    # Reset selected_image
    selected_image = None


def choose_image(index):
    global selected_image
    selected_image = index
    print(index)
    next_images()


def next_images():
    global current_index
    current_index += 3
    if current_index >= len(image_paths):
        current_index = 0
    show_images()


# Create the main window
root = tk.Tk()
root.title("Image Selector")

# Create image labels
image_labels = []
for i in range(3):
    label = tk.Label(root, width=200, height=512, borderwidth=2, relief="solid")
    label.grid(row=0, column=i, padx=10, pady=10)
    image_labels.append(label)

# Create buttons
next_button = tk.Button(root, text="Next", command=next_images)
next_button.grid(row=1, column=1, pady=10)

# Show the initial set of images
show_images()

# Start the main loop
root.mainloop()