import tkinter as tk
from gui.main_window import ColdCompressGUI


def main():
    """Initialize and run the ColdCompress application."""
    root = tk.Tk()
    app = ColdCompressGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()