from NodeView.Node import NodeFunction
import tkinter as tk
class TextNode(NodeFunction):
    def __init__(self) -> None:
        super().__init__()
        self.description = "text"
        self.nodeName = "text"
        self.values = {
            "pass": {"value": "", "display": True, "type": "int"},
            "text": {"value": "", "display": False, "type": "text"},
        }
        self.outputs = {
            "text": "",
        }
        self.text_widget=None
    def functions(self):
        text = self.values["text"]["value"]
        self.outputs = {
            "text": text,
        }

    def nodeUI(self):
        nodeBlock = self.block
        # Text 박스 추가 (여러 줄 입력 가능)
        self.text_widget = text_widget = tk.Text(
            nodeBlock.function_frame,
            width=20,
            height=4,
        )
        text_widget.grid(row=3, column=1, columnspan=3, sticky="w", padx=(0,2), pady=(2,0))
        # self.values["text"] 값 보여주기
        text_widget.insert(tk.END, self.values["text"]["value"])
        # 값 수정 시 self.values["text"] 업데이트 (엔터키는 줄바꿈만)
        text_widget.bind("<KeyRelease>", lambda event, key="text", text_widget=text_widget: self.on_text_change(event, key, text_widget, self.nodeDetailView), add="+")

        self.text_widget = text_widget
    def on_text_change(self, event, key, text_widget, nodeDetailView):
        super().on_text_change(event, key, text_widget, nodeDetailView)
        change_text_widget=None
        if event.widget==self.text_widget:
            if not self.nodeDetailView.node ==self.block:
                return
            (change_text_widget, check_var) = self.nodeDetailView.value_widgets["text"]
        else:
            change_text_widget=self.text_widget
        # Save current cursor position
        # Update the text_widget content to match self.values[key]["value"]
        change_text_widget.delete("1.0", tk.END)
        change_text_widget.insert(tk.END, self.values[key]["value"])
