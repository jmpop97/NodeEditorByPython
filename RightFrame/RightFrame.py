import tkinter as tk
from NodeView.Node import BaseNode

class RightFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, width=200, bg="lightblue")
        self.node = None
        self.parent = app
        self.pack_propagate(False)

        self.top_section = tk.Frame(self, bg="lightgreen", height=100)
        self.middle_section = tk.Frame(self, bg="lightyellow", height=100)
        self.bottom_section = tk.Frame(self, bg="lightpink", height=100)

        self.top_section.pack(fill=tk.X, padx=5, pady=5)
        self.middle_section.pack(fill=tk.X, padx=5, pady=5)
        self.bottom_section.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(self.top_section, text="Top Section", bg="lightgreen").pack()
        tk.Label(self.middle_section, text="Middle Section", bg="lightyellow").pack()
        tk.Label(self.bottom_section, text="Bottom Section", bg="lightpink").pack()

        self.node_name_label = tk.Label(self.top_section, text="Node Name", bg="lightgreen")
        self.node_name_label.pack(fill=tk.X, padx=5, pady=2)
        self.node_name_textbox = tk.Entry(self.top_section)
        self.node_name_textbox.pack(fill=tk.X, padx=5, pady=2)

        self.description_label = tk.Label(self.top_section, text="Description", bg="lightgreen")
        self.description_label.pack(fill=tk.X, padx=5, pady=2)
        self.description_textbox = tk.Entry(self.top_section)
        self.description_textbox.pack(fill=tk.X, padx=5, pady=2)

        self.node_name_textbox.bind("<KeyRelease>", lambda event: self.update_node_name(self.node, self.node_name_textbox.get()) if self.node else None)
        self.description_textbox.bind("<KeyRelease>", lambda event: self.update_description(self.node, self.description_textbox.get()) if self.node else None)

        self.value_widgets = {}
        self.output_labels = {}

    def update_node_details(self, node: BaseNode):
        self.node = node
        node.updateNodeDetailUi(self)

    def update_node_name(self, node: BaseNode, new_name: str):
        if node and new_name:
            node.nodeName = new_name
            selected_item = self.parent.left_frame.tree.selection()
            if selected_item:
                self.parent.left_frame.tree.item(selected_item[0], text=new_name)
            for node_id, n in self.parent.center_frame.nodes.items():
                if n.node == node:
                    n.update_id()
                    break

    def update_description(self, node: BaseNode, new_description: str):
        if node and new_description:
            node.description = new_description
            for key, label in self.output_labels.items():
                if key == "description":
                    label.config(text=f"description: {new_description}")
                    break

    def update_node_value(self, key: str, new_value: str):
        if self.node and key in self.node.values:
            self.node.values[key]["value"] = new_value
            for label_key, label in self.output_labels.items():
                if label_key == key:
                    label.config(text=f"{key}: {new_value}")
                    break

    def update_node_display(self, key: str, new_display: bool):
        if self.node and key in self.node.values:
            self.node.values[key]["display"] = new_display
            if key in self.value_widgets:
                entry, check_var = self.value_widgets[key]
                check_var.set(new_display)
