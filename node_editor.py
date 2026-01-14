import tkinter as tk
from tkinter import Canvas, ttk
from funtions.TestNode import TestNode
import os
import importlib
from NodeView.Node import Node, BaseNode
from NodeView.CenterFrame import CenterFrame
from typing import Optional  # Add this import at the top of the file
from NodeListView.NodeListView import NodeListView
from RightFrame.RightFrame import RightFrame
class NodeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Node Editor")
        self.geometry("1200x600")

        # Use PanedWindow to allow resizing between frames
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Add frames to the PanedWindow
        self.right_frame = RightFrame(self.paned_window, self)  # Pass self as parent
        self.center_frame = CenterFrame(self.paned_window, self)  # Pass self as parent
        self.left_frame = NodeListView(self.paned_window, self)  # Pass self as parent

        self.paned_window.add(self.left_frame, stretch="always")
        self.paned_window.add(self.center_frame, stretch="always")
        self.paned_window.add(self.right_frame, stretch="always")






if __name__ == "__main__":    
    app = NodeEditor()    
    app.mainloop()