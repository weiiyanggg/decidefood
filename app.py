import tkinter as tk
from controller import Controller


class App():
    def __init__(self) -> None:
        root = tk.Tk()
        app = Controller(root)
        root.mainloop()
