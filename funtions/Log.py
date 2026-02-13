from NodeView.Node import NodeFunction
import tkinter as tk
from tkinter import ttk

class Log(NodeFunction):
    def __init__(self) -> None:
        super().__init__()
        self.description = "Log"
        self.nodeName = "Log"
        self.values = {
            "tag":{"value": ["sql","response","cookie","redirect_url","status_code"], "display": False, "type": "list"},
            "list": {"value": [], "display": True, "type": "list"},
            # 샘플 데이터 추가
        }
        self.outputs = {
            "list": [],
        }


    def functions(self):
        # 입력값을 outputs['list']에 append
        value_list = self.values["list"]["value"]
        self.outputs["list"].append(value_list)

        # nodeUI 트리 추가
        self.tree.insert('', 'end', values=value_list)
        if self.nodeDetailView.node ==self.block:
            self.detail_tree.insert('', 'end', values=value_list)

    def nodeUI(self):
        nodeBlock = self.block
        # Increase nodeBlock size by 100 for width and height
        x, y, width, height = nodeBlock.rectPoint
        width, height  = 300,300
        nodeBlock.rectPoint = (x, y, width, height)
        # Update frame size on canvas
        nodeBlock.parent.canvas.itemconfig(nodeBlock.frame_window, width=width, height=height)

        # values의 key를 칼럼으로 Treeview에 보여주기
        columns = self.values["tag"]["value"]
        self.tree = tree= ttk.Treeview(nodeBlock.function_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=50, anchor='center')
        # for indexs in self.values.get("list"):
        #     tree.insert('', 'end', values=indexs)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2)
        tree.bind("<Button-3>", self.on_right_click)
    
    def outputUI(self):
        for widget in self.nodeDetailView.bottom_section.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.nodeDetailView.bottom_section, bg="lightpink")
        frame.pack(fill=tk.BOTH, padx=5, pady=2, expand=True)

        # Treeview for output list
        columns =  self.values["tag"]["value"]
        self.detail_tree=tree= ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=50, anchor='center')
        # outputs['list']를 가로(컬럼) 방향으로 한 줄에 넣기
        for indexs in self.outputs.get("list"):
            tree.insert('', 'end', values=indexs)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2)
        tree.bind("<Button-3>", self.on_right_click)

    def on_right_click(self, event):
        # Determine which tree was clicked
        widget = event.widget
        item = widget.identify_row(event.y)
        if not item:
            return
        idx = widget.index(item)
        widget.delete(item)
        # outputs['list']에서 해당 index 값 삭제
        if idx < len(self.outputs["list"]):
            del self.outputs["list"][idx]
        # 두 트리 모두 동기화
        for tree_attr in ("tree", "detail_tree"):
            tree_obj = getattr(self, tree_attr, None)
            if tree_obj:
                for i in tree_obj.get_children():
                    tree_obj.delete(i)
                for indexs in self.outputs.get("list", []):
                    tree_obj.insert('', 'end', values=indexs)
