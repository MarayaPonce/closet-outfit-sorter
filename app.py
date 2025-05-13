#UI's code
import tkinter as tk
from tkinter import messagebox

# List to hold saved clothing items
wardrobe_data = []

#Buttons
def add_clothes():
    form = tk.Toplevel()
    form.title("Add Clothing Item")
    form.geometry("400x400")

    # Create form fields
    tk.Label(form, text="Name:").pack()
    name_entry = tk.Entry(form)
    name_entry.pack()

    tk.Label(form, text="Type (top, bottom, etc.):").pack()
    type_entry = tk.Entry(form)
    type_entry.pack()

    tk.Label(form, text="Color:").pack()
    color_entry = tk.Entry(form)
    color_entry.pack()

    tk.Label(form, text="Tags (comma-separated):").pack()
    tags_entry = tk.Entry(form)
    tags_entry.pack()

    tk.Label(form, text="Custom Tag:").pack()
    custom_entry = tk.Entry(form)
    custom_entry.pack()

    # Submit button inside this function
    def submit():
        name = name_entry.get()
        type_ = type_entry.get()
        color = color_entry.get()
        tags = [t.strip() for t in tags_entry.get().split(",")]
        custom = custom_entry.get()

        item = {
            "name": name,
            "type": type_,
            "color": color,
            "tags": tags,
            "custom_tag": custom
        }

        wardrobe_data.append(item)
        messagebox.showinfo("Saved", f"Item saved: {item['name']}")
        form.destroy()

    tk.Button(form, text="Save Item", command=submit).pack(pady=20)

def view_clothes():
    print("All saved items:")
    for item in wardrobe_data:
        print(item)

# Home page
root = tk.Tk()
root.title("Closet")
root.geometry("400x300")

# Welcome label
label = tk.Label(root, text="Welcome to your Wardrobe!", font=("Arial", 16))
label.pack(pady=20)

# Buttons
btn_add = tk.Button(root, text="Add Clothing Item", command=add_clothes)
btn_add.pack(pady=10)

btn_view = tk.Button(root, text="View Wardrobe", command=view_clothes)
btn_view.pack(pady=10)

# Run the app. This always goes at the end!
root.mainloop()


