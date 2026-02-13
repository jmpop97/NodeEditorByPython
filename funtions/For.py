from NodeView.Node import NodeFunction
import tkinter as tk
from tkinter import ttk

class For(NodeFunction):
    def __init__(self) -> None:
        super().__init__()
        self.description = "For"
        self.nodeName = "For"
        self.values = {
            "input":{"value": "", "display": True, "type": "text"},
            "tryTime":{"value": 0, "display": False, "type": "int"},
            "Limit": {"value": 0, "display": False, "type": "int"},
            # 샘플 데이터 추가
        }
        self.outputs = {
            "tryTime": 0,
            "output":""
        }

        self.limit_spinbox=None
    def functions(self):
        n=self.values["tryTime"]["value"]
        self.outputs["tryTime"] = n
        print("work time : ", n)
        self.outputs["output"] = self.values["input"]["value"]

        n+=1
        if n >= self.values["Limit"]["value"]:
            self.block.on_stop(None)
            n=0
        self.values["tryTime"]["value"]=n
        if self.nodeDetailView.node==self.block:
            (detail_spinbox,_)=self.nodeDetailView.value_widgets["tryTime"]
            detail_spinbox.delete(0, tk.END)
            detail_spinbox.insert(0, n)
        spinbox=self.nodeUI_widget["tryTime"]
        spinbox.delete(0, tk.END)
        spinbox.insert(0, n)
        print(self.values)
    def nodeUI(self):
        nodeBlock = self.block
        frame = tk.Frame(nodeBlock.function_frame, bg="white")
        frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        # tryTime label and spinbox
        tryTime_frame = tk.Frame(frame, bg="white")
        tryTime_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(tryTime_frame, text="tryTime:", bg="white").pack(side=tk.LEFT)
        tryTime_spinbox = tk.Spinbox(
            tryTime_frame,
            from_=0,
            to=1000,
            textvariable=tk.StringVar(value=self.values["tryTime"]["value"]),
            width=10
        )
        tryTime_spinbox.pack(side=tk.LEFT, padx=5)
        tryTime_spinbox.bind("<KeyRelease>", lambda event, k="tryTime", w=tryTime_spinbox: self.on_int_spinbox_change(k, w), add="+")
        tryTime_spinbox.bind("<ButtonRelease>", lambda event, k="tryTime", w=tryTime_spinbox: self.on_int_spinbox_change(k, w), add="+")
        self.nodeUI_widget["tryTime"] = tryTime_spinbox
        
        # Limit label and spinbox
        limit_frame = tk.Frame(frame, bg="white")
        limit_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(limit_frame, text="Limit:", bg="white").pack(side=tk.LEFT)
        limit_spinbox = tk.Spinbox(
            limit_frame,
            from_=0,
            to=1000,
            textvariable=tk.StringVar(value=self.values["Limit"]["value"]),
            width=10
        )
        limit_spinbox.pack(side=tk.LEFT, padx=5)
        limit_spinbox.bind("<KeyRelease>", lambda event, k="Limit", w=limit_spinbox: self.on_int_spinbox_change(k, w), add="+")
        limit_spinbox.bind("<ButtonRelease>", lambda event, k="Limit", w=limit_spinbox: self.on_int_spinbox_change(k, w), add="+")
        self.nodeUI_widget["Limit"] = limit_spinbox

    def on_int_spinbox_change(self, key, text_widget):
        n=super().on_int_spinbox_change(key, text_widget)
        print(self.values)
        if self.nodeDetailView.node!=self.block:
            return
        spinbox=None
        if self.nodeUI_widget[key]==text_widget:
            (spinbox,_)=self.nodeDetailView.value_widgets[key]
        else:
            spinbox=self.nodeUI_widget[key]
        spinbox.delete(0, tk.END)
        spinbox.insert(0, n)


