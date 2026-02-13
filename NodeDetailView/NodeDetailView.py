import tkinter as tk
from typing import Optional
class NodeDetailView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, width=200, bg="lightblue")
        from NodeView.Node import NodeFunction
        from NodeView.Node import NodeBlock
        self.class_NodeFunction=NodeFunction
        self.node: Optional[NodeBlock] = None
        self.parent = app
        self.nodeView=None
        self.nodeListView=None
        self.pack_propagate(False)

        # --- 스크롤 가능한 영역 생성 ---
        self.canvas = tk.Canvas(self, borderwidth=0, background="lightblue")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg="lightblue")
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self._on_frame_configure, add="+")
        self.canvas.bind('<Configure>', self._on_canvas_configure, add="+")

        # --- 기존 내용은 inner_frame에 배치 ---
        self.list_section = tk.Frame(self.inner_frame, bg="#e0e0e0", height=100)  # 연회색
        self.top_section = tk.Frame(self.inner_frame, bg="#90ee90", height=100)   # 연녹색
        self.middle_section = tk.Frame(self.inner_frame, bg="#ffffe0", height=100) # 연노랑
        self.bottom_section = tk.Frame(self.inner_frame, bg="#ffb6c1", height=100) # 연분홍

        self.list_section.pack(fill=tk.X, padx=5, pady=5)
        self.top_section.pack(fill=tk.X, padx=5, pady=5)
        self.middle_section.pack(fill=tk.X, padx=5, pady=5)
        self.bottom_section.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(self.list_section, text="List Section", bg="#e0e0e0").pack()
        tk.Label(self.top_section, text="Top Section", bg="lightgreen").pack()
        tk.Label(self.middle_section, text="Middle Section", bg="lightyellow").pack()
        tk.Label(self.bottom_section, text="Bottom Section", bg="lightpink").pack()

        self.node_name_label = tk.Label(self.top_section, text="Node Name", bg="lightgreen")
        self.node_name_label.pack(fill=tk.X, padx=5, pady=2)
        self.node_name_textbox = tk.Entry(self.top_section)
        self.node_name_textbox.pack(fill=tk.X, padx=5, pady=2)
        self.node_name_textbox.bind("<KeyRelease>", lambda event: self.update_node_name(self.node_name_textbox.get()), add="+")

        self.description_label = tk.Label(self.top_section, text="Description", bg="lightgreen")
        self.description_label.pack(fill=tk.X, padx=5, pady=2)
        self.description_textbox = tk.Entry(self.top_section)
        self.description_textbox.pack(fill=tk.X, padx=5, pady=2)
        self.description_textbox.bind("<KeyRelease>", lambda event: self.update_description(), add="+")

        self.priority_label = tk.Label(self.top_section, text="우선순위", bg="lightgreen")
        self.priority_label.pack(fill=tk.X, padx=5, pady=2)
        self.priority_textbox = tk.Entry(self.top_section)
        self.priority_textbox.pack(fill=tk.X, padx=5, pady=2)
        self.priority_textbox.bind("<KeyRelease>", lambda event: self.update_priority(), add="+")


        self.value_widgets = {}
        self.output_widgets = {}
        self.output_labels = {}

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.inner_frame_id, width=canvas_width)

    def update_description(self):
        description = self.description_textbox.get()
        self.node.nodeFunction.description = description
    def update_priority(self):
        priority = self.priority_textbox.get()
        try:
            self.node.priority = int(priority)
        except:
            pass
        self.nodeView.updateSelectedNode()
    def update_list_value(self, key: str, new_value: str, index: int):

        value_list = self.node.nodeFunction.values[key]["value"]
        value_list[index] = new_value
        self.node.nodeFunction.values[key]["value"] = value_list
        for label_key, label in self.output_labels.items():
            if label_key == key:
                # index값으로 해당 항목만 표시
                label.config(text=f"{key}[{index}]: {value_list[index]}")
                break
    def update_node_output(self, key: str, new_value: str):
        if self.node and key in self.node.values:
            self.node.outputs[key] = new_valueas.bbox
    def update_node_name(self, new_name: str):
        node= self.node
        node.nodeFunction.nodeName=new_name    
        node.button_frame_widgets.nodeName_label.config(text=new_name)

