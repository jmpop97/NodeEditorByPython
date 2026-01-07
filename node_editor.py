import tkinter as tk
from tkinter import Canvas, ttk
from funtions.TestNode import TestNode
import os
import importlib
from Node import Node,BaseNode
from typing import Optional  # Add this import at the top of the file
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
        self.left_frame = LeftFrame(self.paned_window, self)  # Pass self as parent

        self.paned_window.add(self.left_frame, stretch="always")
        self.paned_window.add(self.center_frame, stretch="always")
        self.paned_window.add(self.right_frame, stretch="always")
class LeftFrame(tk.Frame):
    def __init__(self, parent, app:NodeEditor):  # Pass app as parent
        super().__init__(parent, width=200, bg="lightgray")
        self.parent = app  # Store the reference to the app
        self.pack_propagate(False)

        # Add a Treeview widget to the left frame for the node list
        self.tree = ttk.Treeview(self, columns=("Type", "Description"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Description", text="Description")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Dynamically load node types from the funtions directory
        self.sample_data = self.load_node_data()
        for item in self.sample_data:
            self.tree.insert("", "end", values=item)

        # Bind Treeview selection event
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def load_node_data(self):
        node_data = []
        funtions_dir = os.path.join(os.path.dirname(__file__), "funtions")
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

class CenterFrame(tk.Frame):
    def __init__(self, parent, app:NodeEditor):  # Pass app as parent
        super().__init__(parent, width=200, bg="white")
        self.parent = app  # Store the reference to the app
        self.pack_propagate(False)

        # Add a canvas to draw nodes
        self.canvas = Canvas(self, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Store references to nodes
        self.nodes = {}
        self.selected_node: Optional[Node] = None
        self.offset_x = 0
        self.offset_y = 0

        # Bind mouse events for node interaction
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_node_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def add_node(self, node_id, node_class, num_inputs=1, num_outputs=1):
        # Create a new Node instance with multiple input and output pins
        x1, y1, x2, y2 = 50, 50, 150, 100
        node = Node(self.canvas, node_id, node_class(), x1, y1, x2, y2, num_inputs, num_outputs)
        self.nodes[node_id] = node

    def on_canvas_click(self, event):
        # Detect if a node's rect is clicked, prioritize the topmost node
        overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        self.selected_node = None  # Reset selected node

        for item in reversed(overlapping_items):  # Check from topmost to bottommost
            for node_id, node in self.nodes.items():
                if item == node.rect and node.is_inside(event.x, event.y):
                    self.selected_node = node
                    coords = node.get_coords()
                    self.offset_x = event.x - coords[0]
                    self.offset_y = event.y - coords[1]

                    # Highlight the selected node
                    self.canvas.itemconfig(node.rect, outline="blue", width=3)

                    # Notify RightFrame about the selected node
                    if self.selected_node:
                        self.parent.right_frame.update_node_details(self.selected_node.node)
                    break

        # Reset all unselected nodes to default appearance
        for node_id, node in self.nodes.items():
            if node != self.selected_node:
                self.canvas.itemconfig(node.rect, outline="black", width=1)

    def on_node_drag(self, event):
        if self.selected_node:  # Only move if a node is selected
            # Move the selected node
            x, y = event.x - self.offset_x, event.y - self.offset_y
            coords = self.selected_node.get_coords()
            dx = x - coords[0]
            dy = y - coords[1]
            self.selected_node.move(dx, dy)

    def on_release(self, event):
        self.selected_node = None

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