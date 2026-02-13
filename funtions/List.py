from NodeView.Node import NodeFunction
import tkinter as tk
class List(NodeFunction):
    def __init__(self) -> None:
        super().__init__()
        self.description = "List"
        self.nodeName = "List"
        self.values = {
            "get": {"value": "", "display": True, "type": "text"},
            # 샘플 데이터 추가
            "list": {"value": [], 'n': 0, "display": False, "type": "list"},
        }
        self.outputs={"result":None}
        self.listbox=None
    def functions(self):
        lst = self.values["list"]["value"]
        n = self.values["list"].get("n", 0)
        if not lst or not (0 <= n < len(lst)):
            self.outputs = {
                "result": None,
            }
        else:
            self.outputs = {
                "result": lst[n],
            }
            # n을 다음 인덱스로 증가 (범위 초과 시 0으로 순환)
            next_n = n + 1 if n + 1 < len(lst) else 0
            self.values["list"]["n"] = next_n
    def nodeUI(self):
        nodeBlock=self.block
        # Listbox 위젯으로 리스트 보여주기
        key = "list"
        value = self.values[key]
        list_values = value.get("value", [])
        listbox = tk.Listbox(nodeBlock.function_frame, height=5, selectmode=tk.SINGLE)
        for item in list_values:
            listbox.insert(tk.END, item)
        n = value.get('n', 0)
        listbox.selection_set(n)
        listbox.activate(n)
        listbox.see(n)
        nodeBlock._add_event(listbox)
        self.listbox = listbox
        # Set selection to 'n' if present and valid
        listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        listbox.bind("<<ListboxSelect>>",self.on_listbox_select, add="+")

    def on_listbox_select(self, event):
        src, index = super().on_listbox_select(event)
        if index is not None:
            target=None
            if src is self.listbox:
                (target,_)=self.nodeDetailView.value_widgets["list"]
            else: 
                target=self.listbox
            target.selection_clear(0, tk.END)
            target.selection_set(index)
            target.activate(index)
            target.see(index)
    def on_listbox_right_click(self, index):
        super().on_listbox_right_click(index)
        self.listbox.delete(index)

    def on_listbox_add_item(self, key=None, listbox=None, add_entry=None):
        new_item =super().on_listbox_add_item(key, listbox,add_entry)
        self.listbox.insert(tk.END, new_item)
