#UI: User interface: 
import tkinter as tk

# Main window
root = tk.Tk()
root.title("closet")
root.geometry("400x300")

# Add a label
label = tk.Label(root, text="Welcome to your Wardrobe!", font=("Helvetica", 16))
label.pack(pady=20)

# Run the window
root.mainloop()

