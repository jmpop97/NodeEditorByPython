from NodeView.Node import NodeFuntion
import tkinter as tk
class TextNode(NodeFuntion):
    def __init__(self) -> None:
        self.description = "text"
        self.nodeName = "text"
        self.values = {
            "text": {"value": "", "display": False, "type": "text"},
        }
        self.outputs = {
            "text": "",
        }


    def functions(self):
        text = self.values["text"]["value"]
        self.outputs = {
            "text": text,
        }
    
    def nodeUI(self, nodeBlock):
        # Text 박스 추가 (여러 줄 입력 가능)
        nodeBlock.text_widget = tk.Text(nodeBlock.function_frame, width=20, height=4)
        nodeBlock.text_widget.grid(row=3, column=1, columnspan=3, sticky="w", padx=(0,2), pady=(2,0))
        # self.values["text"] 값 보여주기
        nodeBlock.text_widget.insert(tk.END, self.values["text"]["value"])
        # 값 수정 시 self.values["text"] 업데이트
        def on_text_change(event):
            self.values["text"]["value"] = nodeBlock.text_widget.get("1.0", tk.END).rstrip("\n")
            self.inputUI(nodeBlock.parent.parent.nodeDetailView,nodeBlock)
        nodeBlock.text_widget.bind("<KeyRelease>", on_text_change)
