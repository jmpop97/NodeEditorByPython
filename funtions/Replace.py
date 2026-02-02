from NodeView.Node import NodeFunction
import tkinter as tk
class Replace(NodeFunction):
    def __init__(self) -> None:
        super().__init__()
        self.description = "Replace"
        self.nodeName = "Replace"
        self.values = {
            "text": {"value": "Hello World", "display": True, "type": "text"},
            "before": {"value": "World", "display": False, "type": "text"},
            "after": {"value": "Python", "display": True, "type": "text"},
        }
        self.outputs = {
            "result": "",
        }

    def functions(self):
        text = self.values["text"]["value"]
        before = self.values["before"]["value"]
        after = self.values["after"]["value"]
        result = text.replace(before, after)
        self.outputs = {
            "result": result,
        }

    def nodeUI(self):
        nodeBlock = self.block
        # Entry for 'before'
        before_label = tk.Label(nodeBlock.function_frame, text="Before:")
        before_label.grid(row=4, column=1, sticky="w", padx=(0,2), pady=(2,0))
        nodeBlock.before_entry = tk.Entry(nodeBlock.function_frame, width=20)
        nodeBlock.before_entry.grid(row=4, column=2, columnspan=2, sticky="w", padx=(0,2), pady=(2,0))
        nodeBlock.before_entry.insert(0, self.values["before"]["value"])
        def on_before_change(event=None):
            self.values["before"]["value"] = nodeBlock.before_entry.get()
            self.inputUI()
        nodeBlock.before_entry.bind("<KeyRelease>", on_before_change)

        # Entry for 'after'
        after_label = tk.Label(nodeBlock.function_frame, text="After:")
        after_label.grid(row=5, column=1, sticky="w", padx=(0,2), pady=(2,0))
        nodeBlock.after_entry = tk.Entry(nodeBlock.function_frame, width=20)
        nodeBlock.after_entry.grid(row=5, column=2, columnspan=2, sticky="w", padx=(0,2), pady=(2,0))
        nodeBlock.after_entry.insert(0, self.values["after"]["value"])
        def on_after_change(event=None):
            self.values["after"]["value"] = nodeBlock.after_entry.get()
            self.inputUI()
        nodeBlock.after_entry.bind("<KeyRelease>", on_after_change)
