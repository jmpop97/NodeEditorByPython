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
        self.tree = ttk.Treeview(self, columns=("Name", "Type", "Description"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Description", text="Description")
        # Set column widths
        self.tree.column("Name", width=60, minwidth=50, anchor="w")
        self.tree.column("Type", width=60, minwidth=50, anchor="w")
        self.tree.column("Description", width=100, minwidth=50, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Dynamically load node types from the funtions directory
        self.sample_data = self.load_node_data()
        for item in self.sample_data:
            self.tree.insert("", "end", values=item)

        # Bind Treeview selection event
        self.tree.bind("<Double-1>", self.on_item_double_click)
        # Bind right-click event for context menu
        self.tree.bind("<Button-3>", self.show_context_menu)
        # Create context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="삭제", command=self.delete_selected_item)

    def load_node_data(self):
        node_data = []
        funtions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "funtions")
        for filename in os.listdir(funtions_dir):
            if filename.endswith("Node.py"):
                module_name = f"funtions.{filename[:-3]}"
                module = importlib.import_module(module_name)
                node_class = getattr(module, filename[:-3])
                node_instance = node_class()
                node_name = getattr(node_instance, "nodeName", filename[:-3])
                node_type = getattr(node_instance, "nodeType", "Node")
                node_data.append((node_name, node_type, node_instance.description, node_class))
            elif filename.endswith(".json"):
                json_path = os.path.join(funtions_dir, filename)
                try:
                    import json
                    with open(json_path, "r", encoding="utf-8") as f:
                        json_content = json.load(f)
                    # Use the 'name' field if present, else filename
                    json_name = json_content.get("name", filename)
                    json_desc = json_content.get("desc", "")
                    node_data.append((json_name, "Multy Nodes", json_desc, json_content))
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        return node_data

    def on_item_double_click(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            node_name = self.tree.item(selected_item[0], "values")[0]
            node_type = self.tree.item(selected_item[0], "values")[1]
            # Find the node_class/content from sample_data
            node_obj=self.get_node_by_name(node_name)
            if node_type == "Node":
                self.parent.center_frame.add_node(node_obj)
            elif node_type == "Multy Nodes":
                self.parent.center_frame.add_nodes(node_obj)

    def get_node_by_name(self, node_name):
        for item in self.sample_data:
            if item[0] == node_name:
                return item[3]
        return None
    def get_node_by_classname(self, class_name):
        for item in self.sample_data:
            if isinstance(item[3], type):
                if item[3].__name__ == class_name:
                    return item[3]
        return None
    def refresh(self):
        """Reload node data and update the treeview UI."""
        self.sample_data = self.load_node_data()
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert new data
        for item in self.sample_data:
            self.tree.insert("", "end", values=item)

    def show_context_menu(self, event):
        # Select the item under mouse
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_selected_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            node_name = self.tree.item(selected_item[0], "values")[0]
            node_type = self.tree.item(selected_item[0], "values")[1]
            if node_type != "Multy Nodes":
                # Only allow deletion for Multy Nodes
                return
            # Remove from treeview
            self.tree.delete(selected_item[0])
            # Remove from sample_data
            self.sample_data = [item for item in self.sample_data if item[0] != node_name]
            # Remove the corresponding JSON file from funtions directory
            funtions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "funtions")
            for filename in os.listdir(funtions_dir):
                if filename.endswith(".json"):
                    json_path = os.path.join(funtions_dir, filename)
                    try:
                        import json
                        with open(json_path, "r", encoding="utf-8") as f:
                            json_content = json.load(f)
                        json_name = json_content.get("name", filename)
                        if json_name == node_name:
                            os.remove(json_path)
                            break
                    except Exception as e:
                        print(f"Error deleting {filename}: {e}")