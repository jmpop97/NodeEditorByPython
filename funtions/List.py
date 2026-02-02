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
        self.outputs = {
            "result": None,
        }
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
        listbox = tk.Listbox(nodeBlock.function_frame, height=min(5, len(list_values)), selectmode=tk.SINGLE)
        for item in list_values:
            listbox.insert(tk.END, item)
        # Set selection to 'n' if present and valid
        n = value.get('n', 0)
        if 0 <= n < len(list_values):
            listbox.selection_set(n)
            listbox.see(n)
        listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Optional: bind selection event if needed
        def on_listbox_select(event, key=key, listbox=listbox):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                selected_value = listbox.get(index)
                self.values[key]["selected"] = selected_value
                # n 값을 선택한 인덱스로 변경
                self.values[key]["n"] = index
                if self.nodeDetailView.value_widgets["list"]:
                    (text_widget, check_var) = self.nodeDetailView.value_widgets["list"]
                    self.inputUI()
                    
        listbox.bind("<<ListboxSelect>>", on_listbox_select)
        self.listbox=listbox
    def on_listbox_select(self, event, key, listbox):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            selected_value = listbox.get(index)
            self.values[key]["selected"] = selected_value
            self.values[key]["n"] = index

            if self.nodeDetailView and hasattr(self.nodeDetailView, 'update_list_value'):
                self.nodeDetailView.update_list_value(key, selected_value, index)
                self.listbox.selection_set(index)