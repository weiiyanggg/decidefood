from tkinter import ttk
from frame import DescriptionFrame, QuestionFrame


class Controller:
    '''
    Takes control of the root (or main window provided by tkinter.Tk()) 
    Responsible for instantiating all widgets and root wide interactions or changes
    '''

    def __init__(self, root):
        self.root = root
        self.set_root()
        self.create_widgets()

    def set_root(self):
        self.set_title()
        self.set_style()
        self.set_dimensions()

    def set_title(self):
        self.root.title("Places To Eat Generator")

    def set_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Next.TButton", padding=7, font=(
            "Comic Sans MS", 10, "bold"), foreground="white", background="#4d658a", borderwidth=0)
        self.root.configure(bg='#7c8ba3')

    def set_dimensions(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        self.description_frame = DescriptionFrame(self)
        self.description_frame.pack(pady=10)
        self.question_frame = QuestionFrame(self)
        self.question_frame.pack(pady=10)
