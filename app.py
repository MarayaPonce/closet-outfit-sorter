#UI: User interface: 
import tkinter as tk

# UI's Home page
root = tk.Tk()
root.title("closet")
root.geometry("400x300")

# Add a label
label = tk.Label(root, text="Welcome to your Wardrobe!", font=("Archivo Black", 20))
label.pack(pady=20)

# Run the window. This 
root.mainloop()

#Buttons: 
def add_clothes():
    print("Add clothes")

def view_clothes():
    print("Show all saved clothes")

btn_add = tk.Button(root, text="Add Clothing Item", command=add_clothes)
btn_add.pack(pady=10)

btn_view = tk.Button(root, text="View Wardrobe", command=view_clothes)
btn_view.pack(pady=10)


