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
        self.widget={}
    def functions(self):
        text = self.values["text"]["value"]
        before = self.values["before"]["value"]
        after = self.values["after"]["value"]
        print(after,before)
        result = text.replace(before, after)
        self.outputs = {
            "result": result,
        }

    def nodeUI(self):
        nodeBlock = self.block
        self.widget = {}  # Store widgets and labels by key
        before_label = tk.Label(nodeBlock.function_frame, text="Before:")
        before_label.grid(row=4, column=1, sticky="w", padx=(0,2), pady=(2,0))
        before_text = tk.Text(nodeBlock.function_frame, width=20, height=1)
        before_text.grid(row=4, column=2, columnspan=2, sticky="w", padx=(0,2), pady=(2,0))
        before_text.insert("1.0", self.values["before"]["value"])
        before_text.bind("<KeyRelease>", lambda event, key="before", text_widget=before_text: self.on_text_change(event, key, text_widget, self.nodeDetailView), add="+")
        self.widget["before"] = (before_text, before_label)

        # Textbox for 'after' (same as 'before')
        after_label = tk.Label(nodeBlock.function_frame, text="After:")
        after_label.grid(row=5, column=1, sticky="w", padx=(0,2), pady=(2,0))
        after_text = tk.Text(nodeBlock.function_frame, width=20, height=1)
        after_text.grid(row=5, column=2, columnspan=2, sticky="w", padx=(0,2), pady=(2,0))
        after_text.insert("1.0", self.values["after"]["value"])
        after_text.bind("<KeyRelease>", lambda event, key="after", text_widget=after_text: self.on_text_change(event, key, text_widget, self.nodeDetailView), add="+")
        self.widget["after"] = (after_text, after_label)

    def on_text_change(self, event, key, text_widget, nodeDetailView):
        super().on_text_change(event, key, text_widget, nodeDetailView)
        change_text_widget=None
        (node_widget,_)=self.widget[key]
        if event.widget==node_widget:
            if not self.nodeDetailView.node ==self.block:
                return
            (change_text_widget, check_var) = self.nodeDetailView.value_widgets[key]
        else:
            change_text_widget=node_widget
        # Save current cursor position
        # Update the text_widget content to match self.values[key]["value"]
        change_text_widget.delete("1.0", tk.END)
        change_text_widget.insert(tk.END, self.values[key]["value"])
