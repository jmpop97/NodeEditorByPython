import os
import importlib
import tkinter as tk
from tkinter import ttk
from NodeView.Node import BaseNode  # Ensure this import is correct

class NodeListView(tk.Frame):
    def __init__(self, parent, app):  # Pass app as parent
        super().__init__(parent, width=100, bg="lightgray")
        self.parent = app  # Store the reference to the app
        self.pack_propagate(False)

        # Add a Treeview widget to the left frame for the node list
        self.tree = ttk.Treeview(self, columns=("Type", "Description"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Description", text="Description")
        # Set column widths to fit 10 characters (approx 80 pixels for typical font)
        self.tree.column("Type", width=50, minwidth=50, anchor="w")
        self.tree.column("Description", width=50, minwidth=50, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Dynamically load node types from the funtions directory
        self.sample_data = self.load_node_data()
        for item in self.sample_data:
            self.tree.insert("", "end", values=item)

        # Bind Treeview selection event
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def load_node_data(self):
        node_data = []
        funtions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "funtions")
        for filename in os.listdir(funtions_dir):
            if filename.endswith("Node.py"):
                module_name = f"funtions.{filename[:-3]}"
                module = importlib.import_module(module_name)
                node_class = getattr(module, filename[:-3])
                node_instance = node_class()
                node_data.append((filename[:-3], node_instance.description, node_class))
        return node_data

    def on_item_double_click(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            node_name = self.tree.item(selected_item[0], "values")[0]
            node_id = f"node_{len(self.parent.center_frame.nodes) + 1}"
            # Find the node_class from sample_data
            for item in self.sample_data:
                if item[0] == node_name:
                    node_class = item[2]
                    break
            self.parent.center_frame.add_node(node_id, node_class)
