from NodeView.Node import nodeFuction
import tkinter as tk
class TextNode(nodeFuction):
    def __init__(self,node) -> None:
        self.description = "Text"
        self.nodeName="Text"
        self.values = {
            "input": { "display": False,"value": "","type":"text"},
        }
        self.outputs = {
            "output": "",
        }
        self.nodeUI=node

        if node:        # rectPoint의 크기를 오른쪽 아래로 50씩 키움
            x1, y1, x2, y2 = node.rectPoint
            node.rectPoint = [x1, y1, x2 + 50, y2 + 50]
        # node.rectPoint
    def functions(self):
        self.outputs["output"]=self.values["input"]["value"]
    def createNodeUI(self):
        node = self.nodeUI
        x1, y1, x2, y2 = node.rectPoint
        # Text 위젯 생성 (수정 가능, 줄바꿈 지원)
        text_widget = tk.Text(node.parent.canvas.master, wrap='word', height=3, width=20)
        text_widget.insert('1.0', self.values['input']['value'])
        text_widget.bind('<KeyRelease>', self.on_text_change)
        # nodeName을 왼쪽 위 20만큼 공간에 표시할 Label 추가
        # name_label을 왼쪽 위 20만큼 빈공간에 표시
        name_label = node.parent.canvas.create_text(
            x1 + 20,
            y1 ,
            text=self.nodeName,
            tags=node.node_id,
            anchor='nw'  # 왼쪽 위 기준
        )
        # 위치 지정 (y 위치를 20만큼 아래로 이동)
        text_widget.place(x=(x1 + x2) // 2, y=((y1 + y2) // 2) + 30, anchor='center')
        node.nodeUI = [name_label, text_widget]
    def on_text_change(self, event=None):
        widget = event.widget if event else None
        if widget:
            self.values['input']['value'] = widget.get('1.0', 'end-1c')
        self.updateNodeDetailUi(self.nodeUI.parent.parent.right_frame)
    def moveUI(self, dx, dy):
        node = self.nodeUI
        (x1, y1, x2, y2) = node.rectPoint
        # Move name_label (nodeName label)
        name_label = node.nodeUI[0]
        node.parent.canvas.move(name_label, dx, dy)
        # Move text_widget
        text_widget = node.nodeUI[1]
        text_widget.place(x=(x1 + x2) // 2 + dx, y=((y1 + y2) // 2) + 30 + dy, anchor='center')
    def delete(self):
        node = self.nodeUI
        name_label = node.nodeUI[0]
        text_widget = node.nodeUI[1]
        # Remove Canvas text item
        node.parent.canvas.delete(name_label)
        # Destroy the tk.Text widget
        text_widget.destroy()
        node.nodeUI = []
