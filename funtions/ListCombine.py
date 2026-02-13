from NodeView.Node import NodeFunction
import tkinter as tk
from tkinter import ttk

class ListCombine(NodeFunction):
    def __init__(self) -> None:
        super().__init__()
        self.description = "ListCombine"
        self.nodeName = "ListCombine"
        self.values = {
            "sql": {"value": "1", "display": True, "type": "text"},
            "response": {"value": "2", "display": True, "type": "text"},
            "cookie": {"value": "3", "display": True, "type": "text"},
            "redirect_url": {"value": "4", "display": True, "type": "text"},
            "status_code": {"value": "5", "display": True, "type": "text"},
            # 샘플 데이터 추가
        }
        self.outputs = {
            "list": [],
        }


    def functions(self):
        self.outputs["list"]=[v["value"] for v in self.values.values() if v.get("display", False)]
    
    def outputUI(self):
        for widget in self.nodeDetailView.bottom_section.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.nodeDetailView.bottom_section, bg="lightpink")
        frame.pack(fill=tk.BOTH, padx=5, pady=2, expand=True)

        columns = list(self.values.keys())
        self.detail_tree=tree= ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=50, anchor='center')

        tree.insert('', 'end', values=self.outputs.get("list"))
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2)
