import tkinter as tk
from NodeView.Node import NodeFuntion


class NodeDetailView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, width=200, bg="lightblue")
        self.node = None
        self.parent = app
        self.pack_propagate(False)

        # --- 스크롤 가능한 영역 생성 ---
        self.canvas = tk.Canvas(self, borderwidth=0, background="lightblue")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg="lightblue")
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # --- 기존 내용은 inner_frame에 배치 ---
        self.top_section = tk.Frame(self.inner_frame, bg="lightgreen", height=100)
        self.middle_section = tk.Frame(self.inner_frame, bg="lightyellow", height=100)
        self.bottom_section = tk.Frame(self.inner_frame, bg="lightpink", height=100)

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

        # Print changed node name value when it is updated
        self.node_name_textbox.bind("<KeyRelease>", lambda event: self.print_and_update_node_name(self.node, self.node_name_textbox.get()) if self.node else None)
        self.description_textbox.bind("<KeyRelease>", lambda event: self.update_description(self.node, self.description_textbox.get()) if self.node else None)

        self.value_widgets = {}
        self.output_widgets = {}
        self.output_labels = {}

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.inner_frame_id, width=canvas_width)

    def update_description(self, node: NodeFuntion, new_description: str):

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
    def update_node_output(self, key: str, new_value: str):
        if self.node and key in self.node.values:
            self.node.outputs[key] = new_value
    def print_and_update_node_name(self, node: NodeFuntion, new_name: str):
        print(f"Node name changed to: {new_name}")

