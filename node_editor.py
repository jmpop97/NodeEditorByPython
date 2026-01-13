import tkinter as tk
from tkinter import Canvas, ttk
from funtions.TestNode import TestNode
import os
import importlib
from NodeView.Node import Node, BaseNode
from NodeView.CenterFrame import CenterFrame
from typing import Optional  # Add this import at the top of the file
from NodeListView.NodeListView import NodeListView
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




class RightFrame(tk.Frame):
    def __init__(self, parent, app:NodeEditor):  # Pass app as parent
        super().__init__(parent, width=200, bg="lightblue")
        self.node = None
        self.parent = app  # Store the reference to the app
        self.pack_propagate(False)

        # Create three sections
        self.top_section = tk.Frame(self, bg="lightgreen", height=100)
        self.middle_section = tk.Frame(self, bg="lightyellow", height=100)
        self.bottom_section = tk.Frame(self, bg="lightpink", height=100)

        # Pack sections vertically
        self.top_section.pack(fill=tk.X, padx=5, pady=5)
        self.middle_section.pack(fill=tk.X, padx=5, pady=5)
        self.bottom_section.pack(fill=tk.X, padx=5, pady=5)

        # Add example widgets to each section
        tk.Label(self.top_section, text="Top Section", bg="lightgreen").pack()
        tk.Label(self.middle_section, text="Middle Section", bg="lightyellow").pack()
        tk.Label(self.bottom_section, text="Bottom Section", bg="lightpink").pack()

        # Add Entry widgets for nodeName and description in the top section
        self.node_name_label = tk.Label(self.top_section, text="Node Name", bg="lightgreen")
        self.node_name_label.pack(fill=tk.X, padx=5, pady=2)
        self.node_name_textbox = tk.Entry(self.top_section)
        self.node_name_textbox.pack(fill=tk.X, padx=5, pady=2)

        self.description_label = tk.Label(self.top_section, text="Description", bg="lightgreen")
        self.description_label.pack(fill=tk.X, padx=5, pady=2)
        self.description_textbox = tk.Entry(self.top_section)
        self.description_textbox.pack(fill=tk.X, padx=5, pady=2)

        # Bind an event to detect changes in the Entry widget
        self.node_name_textbox.bind("<KeyRelease>", lambda event: self.update_node_name(self.node, self.node_name_textbox.get()) if self.node else None)

        # Bind an event to detect changes in the description Entry widget
        self.description_textbox.bind("<KeyRelease>", lambda event: self.update_description(self.node, self.description_textbox.get()) if self.node else None)

        # Dynamically display self.values in the middle section
        self.value_widgets = {}

        # Dynamically display outputs in the bottom section
        self.output_labels = {}

    def update_node_details(self, node: BaseNode):  # Added explicit type annotation for node
        self.node = node  # Store the reference to the selected node
        # Populate the Entry widgets with the selected node's details
        self.node_name_textbox.delete(0, tk.END)
        self.node_name_textbox.insert(0, node.nodeName)

        self.description_textbox.delete(0, tk.END)
        self.description_textbox.insert(0, node.description)

        # Clear existing widgets in the middle section
        for widget in self.middle_section.winfo_children():
            widget.destroy()

        # Add widgets for self.values
        self.value_widgets.clear()
        for key, value in node.values.items():
            frame = tk.Frame(self.middle_section, bg="lightyellow")
            frame.pack(fill=tk.X, padx=5, pady=2)

            check_var = tk.BooleanVar(value=value.get("display", False))
            check_button = tk.Checkbutton(frame, variable=check_var, bg="lightyellow")
            check_button.pack(side=tk.LEFT)

            label = tk.Label(frame, text=key, bg="lightyellow")
            label.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(frame)
            entry.insert(0, value.get("value", ""))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Bind an event to detect changes in the Entry widget
            entry.bind("<KeyRelease>", lambda event, key=key, entry=entry: self.update_node_value(key, entry.get()) if self.node else None)

            # Bind an event to detect changes in the Checkbutton
            check_var.trace_add("write", lambda *args, key=key, check_var=check_var: self.update_node_display(key, check_var.get()) if self.node else None)

            self.value_widgets[key] = (entry, check_var)

        # Clear existing widgets in the bottom section
        for widget in self.bottom_section.winfo_children():
            widget.destroy()

        # Add widgets for outputs
        self.output_labels.clear()
        for key, value in node.outputs.items():
            label = tk.Label(self.bottom_section, text=f"{key}: {value}", bg="lightpink")
            label.pack(fill=tk.X, padx=5, pady=2)
            self.output_labels[key] = label

    def update_node_name(self, node: BaseNode, new_name: str):
        """Update the nodeName of the given node."""
        if node and new_name:
            node.nodeName = new_name
            # Update the Treeview item text
            selected_item = self.parent.left_frame.tree.selection()
            if selected_item:
                self.parent.left_frame.tree.item(selected_item[0], text=new_name)
            # Update the node's position in the center frame
            for node_id, n in self.parent.center_frame.nodes.items():
                if n.node == node:
                    n.update_id()  # Update the node's ID
                    break

    def update_description(self, node: BaseNode, new_description: str):
        """Update the description of the given node."""
        if node and new_description:
            node.description = new_description
            # Update the corresponding label in the bottom section
            for key, label in self.output_labels.items():
                if key == "description":
                    label.config(text=f"description: {new_description}")
                    break

    def update_node_value(self, key: str, new_value: str):
        print(key,new_value)
        if self.node and key in self.node.values:
            self.node.values[key]["value"] = new_value
            # Update the corresponding label in the bottom section
            for label_key, label in self.output_labels.items():
                if label_key == key:
                    label.config(text=f"{key}: {new_value}")
                    break

    def update_node_display(self, key: str, new_display: bool):
        """Update the display status of the given key in the node's values."""
        if self.node and key in self.node.values:
            self.node.values[key]["display"] = new_display
            # Update the corresponding Checkbutton in the middle section
            if key in self.value_widgets:
                entry, check_var = self.value_widgets[key]
                check_var.set(new_display)




if __name__ == "__main__":    
    app = NodeEditor()    
    app.mainloop()