import tkinter as tk
from gui.app import GaussGameApp  # Correct import for the GaussGameApp class

if __name__ == "__main__":
    root = tk.Tk()
    app = GaussGameApp(root)
    root.mainloop()