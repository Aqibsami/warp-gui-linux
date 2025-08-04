import tkinter as tk
from tkinter import Canvas
import subprocess

# Check WARP status
def get_status():
    try:
        result = subprocess.run(['warp-cli', 'status'], capture_output=True, text=True)
        return 'Connected' in result.stdout
    except:
        return False

# Toggle WARP
def toggle():
    global is_connected
    if is_connected:
        subprocess.run(['sudo', 'warp-cli', 'disconnect'])
    else:
        subprocess.run(['sudo', 'warp-cli', 'connect'])
    update_status()

# Update GUI based on WARP status
def update_status():
    global is_connected
    is_connected = get_status()

    status_var.set("Connected" if is_connected else "Disconnected")
    status_label.config(fg="#FF6B35" if is_connected else "#666666")
    status_message.config(text="Your Internet is private." if is_connected else "Your Internet is not private.")

    # Update switch with smooth rounded design
    if is_connected:
        # Connected state - orange background, circle on right
        canvas.itemconfig(switch_bg_left, fill="#FF6B35")
        canvas.itemconfig(switch_bg_right, fill="#FF6B35")
        canvas.itemconfig(switch_bg_center, fill="#FF6B35")
        canvas.coords(switch_circle, 67, 7, 93, 33)  # Move circle to right
    else:
        # Disconnected state - gray background, circle on left
        canvas.itemconfig(switch_bg_left, fill="#E0E0E0")
        canvas.itemconfig(switch_bg_right, fill="#E0E0E0")
        canvas.itemconfig(switch_bg_center, fill="#E0E0E0")
        canvas.coords(switch_circle, 7, 7, 33, 33)  # Move circle to left

    root.after(1000, update_status)

# Main GUI
root = tk.Tk()
root.title("1.1.1.1")
root.geometry("300x400")
root.configure(bg="white")

# Title with gradient-like effect
tk.Label(root, text="WARP", font=("Helvetica", 32, "bold"), fg="#FF4D4D", bg="white").pack(pady=30)

# Status
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 16, "bold"), bg="white")
status_label.pack(pady=15)

# Improved rounded toggle switch
canvas = Canvas(root, width=100, height=40, bg="white", highlightthickness=0)
canvas.pack(pady=30)

# Create rounded toggle background using overlapping shapes
# Left rounded end
switch_bg_left = canvas.create_oval(0, 0, 40, 40, fill="#E0E0E0", outline="")
# Right rounded end  
switch_bg_right = canvas.create_oval(60, 0, 100, 40, fill="#E0E0E0", outline="")
# Center rectangle
switch_bg_center = canvas.create_rectangle(20, 0, 80, 40, fill="#E0E0E0", outline="")

# Movable round button (white circle with subtle shadow effect)
switch_circle = canvas.create_oval(7, 7, 33, 33, fill="white", outline="#D0D0D0", width=1)

# Click event to toggle
canvas.bind("<Button-1>", lambda e: toggle())

# Status message (dynamically updated)
status_message = tk.Label(root, text="", font=("Helvetica", 12), fg="#666666", bg="white")
status_message.pack(pady=20)

# Initialize status
is_connected = False
update_status()

root.mainloop()