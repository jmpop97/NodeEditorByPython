import tkinter as tk
from typing import Optional

class NodeBlock:
    def __init__(self, parent, class_function, x, y, width=300, height=100):
        from NodeView.CenterFrame import NodeView
        self.rectPoint = (x, y, width, height)
        self.parent: Optional[NodeView] = parent
        self.nodeDetailView = parent.nodeDetailView
        self.nodeFunction=nodeFunction = self._createNodeFuntion(class_function)

        self.ChildNode = {}
        self.priority = node_id = self.parent.node_num = parent.node_num + 1
        self.node_id = node_id

        # self.frame = frame = tk.Frame(parent.canvas.master, bg="white", highlightbackground="white", highlightthickness=3)
        self.frame = frame = tk.Frame(parent.canvas.master, bg="white")
        self.frame_window = parent.canvas.create_window(x, y, anchor="nw", window=frame, width=width, height=height)
        self.content_frame = tk.Frame(frame, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self._add_event(frame)

        
        # Add a content_frame inside self.frame to hold all widgets
        # self._add_event(self.frame)
        # Create a frame for buttons at the top (height 10)
        self.button_frame =button_frame= tk.Frame(self.content_frame, bg="white", height=10)
        self.button_frame.pack(fill=tk.X, side=tk.TOP)
        self._add_event(self.button_frame)
        # Create a frame for function UI below the button frame

        # Move buttons to button_frame
        # Add a stretchable empty column to push buttons to the right
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame_widgets=NodeButtonFrame(button_frame,nodeFunction.nodeName,self)
        self.stop_button_state = False  # False: gray, True: red

        self.function_frame = tk.Frame(self.content_frame, bg="white")
        self.function_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self._add_event(self.function_frame)
        self.function_frame_widgets={}

        self.selected = False
        self.selection_border_id = None

        self._drag_data = {"x": 0, "y": 0, "last_x": 0, "last_y": 0, "moved": False}
        self.pins = self.create_pins(parent.canvas)

    def _createNodeFuntion(self, class_function):
        nodeFunction: Optional[NodeFunction] = class_function() if class_function is not None else NodeFunction()
        if nodeFunction is not None:
            nodeFunction.block = self
            nodeFunction.nodeDetailView = self.nodeDetailView
        return nodeFunction

    def select(self, ctrl=False):
        if ctrl:
            if self.selected:
                self.set_selected(False)
                if self.node_id in self.parent.selected_nodes:
                    del self.parent.selected_nodes[self.node_id]
            else:
                self.set_selected(True)
                self.parent.selected_nodes[self.node_id] = self

        else:
            # Deselect all nodes except this one
            for n in self.parent.nodes.values():
                n.set_selected(False)
                if hasattr(n, 'frame'):
                    n.frame.config(bg="white")
            self.parent.selected_nodes.clear()
            self.set_selected(True)
            self.parent.selected_nodes[self.node_id] = self
            # self.frame.config(bg="blue")

    def on_stop(self, event):
        # Toggle stop button color between gray and red
        self.stop_button_state = not self.stop_button_state
        color = "red" if self.stop_button_state else "gray"
        # Change the background color of the stop button directly
        self.button_frame_widgets.stop_button.config(bg=color)


    def set_selected(self, selected: bool):
        self.selected = selected
        canvas = self.parent.canvas
        x, y, width, height = self.rectPoint
        if selected:
            # Draw a blue border rectangle on the canvas
            if self.selection_border_id is not None:
                canvas.delete(self.selection_border_id)
            self.selection_border_id = canvas.create_rectangle(
                x - 2, y - 2, x + width + 2, y + height + 2,
                outline="blue", width=3
            )
            canvas.tag_raise(self.selection_border_id)
        else:
            # Remove the border rectangle
            if self.selection_border_id is not None:
                canvas.delete(self.selection_border_id)
                self.selection_border_id = None

    def get_coords(self):
        x, y, width, height = self.rectPoint
        return (x, y, width, height)

    def move(self, dx, dy):
        canvas = self.parent.canvas
        x, y, width, height = self.rectPoint
        new_x = x + dx
        new_y = y + dy
        self.rectPoint = (new_x, new_y, width, height)
        canvas.coords(self.frame_window, new_x, new_y)
        for pin_types in self.pins.values():
            for pin_tuple in pin_types.values():
                pin, text, _ = pin_tuple
                canvas.move(pin, dx, dy)
                canvas.move(text, dx, dy)
        if self.selected and self.selection_border_id is not None:
            canvas.move(self.selection_border_id, dx, dy)
        # 연결된 connection 선도 같이 이동
        for conn in self.parent.connections.values():
            # 이 노드의 핀과 연결된 선만 업데이트
            start_coords = canvas.coords(conn.output_pin)
            end_coords = canvas.coords(conn.input_pin)
            if len(start_coords) == 4 and len(end_coords) == 4:
                canvas.coords(
                    conn.line_id,
                    (start_coords[0] + start_coords[2]) // 2,
                    (start_coords[1] + start_coords[3]) // 2,
                    (end_coords[0] + end_coords[2]) // 2,
                    (end_coords[1] + end_coords[3]) // 2
                )

    def on_delete(self, event):
        for pin_types in self.pins.values():
            for pin,text,_ in pin_types.values():
                self.parent.canvas.delete(pin)
                self.parent.canvas.delete(text)
                self.parent.canvas.master.remove_connection(pin)  # Remove connections for input pins
        self.frame.destroy()
        self.parent.canvas.delete(self.frame_window)
        if self.selection_border_id is not None:
            self.parent.canvas.delete(self.selection_border_id)
        # Remove itself from selected_nodes
        if self.node_id in self.parent.selected_nodes:
            del self.parent.selected_nodes[self.node_id]
        # Remove itself from parent.nodes as well
        if self.node_id in self.parent.nodes:
            del self.parent.nodes[self.node_id]
        emty_node =NodeFunction()
        emty_node.nodeDetailView=self.nodeDetailView
        emty_node.updateDetailUI()

    def on_play(self, event):
        # Use a dict: {node: priority}
        play_functions = {self: self.priority}
        while play_functions:
            # Pop node with smallest priority
            node = min(play_functions, key=lambda n: play_functions[n])
            if node.stop_button_state:
                break
            print(node.nodeFunction.nodeName)
            _ = play_functions.pop(node)
            outputValues = node.nodeFunction.functions() # type: ignore
            # Update child nodes and add them to play_functions
            for input_node, dic in node.ChildNode.items():
                add_node=False
                for output, inputList in dic.items():
                    if outputValues and not (output in outputValues):
                        continue
                    if input_node.nodeFunction is None:
                        continue
                    for input in inputList:
                        if hasattr(input_node.nodeFunction, 'values') and output in getattr(node.nodeFunction, 'outputs', {}):
                            input_node.nodeFunction.values[input]["value"] = node.nodeFunction.outputs[output]
                            add_node=True
                # Add input_node to play_functions if not already in play_functions
                if add_node:
                    play_functions[input_node] = input_node.priority
        if self.parent.selected_node:
            self.parent.selected_node.nodeFunction.outputUI()
    def create_pins(self, canvas):
        self.pins={
            "input_pin":{},
            "output_pin":{}
            }
        nodeFunctions=self.nodeFunction
        # Prepare input and output keys
        input_keys = [k for k, v in self.nodeFunction.values.items() if v.get("display", False)]
        output_keys = [k for k in self.nodeFunction.outputs.keys()]
        # Remove 'input' from input_keys if present
        for label in input_keys:
            self.create_pin(canvas, 'input', label) 
        for label in output_keys:
            self.create_pin(canvas, 'output', label)
        return self.pins

    def create_pin(self, canvas, pin_type, label):
        x, y, width, height = self.rectPoint
        y += 10
        if pin_type == "input":
            x1 = x-5  # input은 x
            num = self.set_pin_num("input_pin")
            y += num * 10
            pin_x1, pin_y1 = x1 - 5, y - 5
            pin_x2, pin_y2 = x1 + 5, y + 5
            pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="white")
            text = canvas.create_text(pin_x1 - 20, pin_y2, anchor="e", text=label)
            canvas.tag_bind(pin, "<Button-1>", lambda event, pin=pin, pin_type=pin_type, label=label: self.on_pin_click(pin, pin_type, label), add="+")
            self.pins["input_pin"][label] = (pin, text, num)
        elif pin_type == "output":
            x2 = x + width+5  # output은 x+width
            num = self.set_pin_num("output_pin")
            y += num * 10
            pin_x1, pin_y1 = x2 - 5, y - 5
            pin_x2, pin_y2 = x2 + 5, y + 5
            pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="white")
            text = canvas.create_text(pin_x2 + 20, pin_y2, anchor="w", text=label)
            canvas.tag_bind(pin, "<Button-1>", lambda event, pin=pin, pin_type=pin_type, label=label: self.on_pin_click(pin, pin_type, label), add="+")
            self.pins["output_pin"][label] = (pin, text, num)
        else:
            pin = None
            text = None
        return pin, text
    def on_pin_click(self, pin,pin_type,label):
        print(f"Input pin '{pin}' pin_type '{pin_type}' clicked (Node: {self.nodeFunction.nodeName})")
        # Delegate the pin click handling to the CenterFrame
        self.parent.on_pin_click(pin,pin_type,label,self)

    def on_input_pin_click(self, pin_label, node):
        print(f"Input pin '{pin_label}' clicked (Node: {self.nodeFunction.nodeName})")

    def on_output_pin_click(self, pin_label, node):
        print(f"Output pin '{pin_label}' clicked (Node: {self.nodeFunction.nodeName})")
    def on_check(self, key, label):
        nodeDetailView=self.nodeDetailView
        checked = nodeDetailView.value_widgets[key][1].get()
        if checked:
            self.create_pin(self.parent.canvas,"input",label)
        else:
            pin,text,_=self.pins["input_pin"].pop(key)
            self.parent.canvas.delete(pin)
            self.parent.canvas.delete(text)
            self.parent.canvas.master.remove_connection(pin) 
        print(f"Checkbutton clicked for key: {key}, label: {label}, checked: {checked}")
    def set_pin_num(self, typeName):
        # Get (pin, text, num) tuples and sort by num
        tuples = self.pins.get(typeName,{}).values()
        sorted_tuples = sorted(tuples, key=lambda t: t[-1])
        i = 0
        for _,_,num in sorted_tuples:
            if i==num:
                i+=1
            else:
                return i
        return i
    def _add_event(self, widget):
        widget.bind("<ButtonPress-1>", self._on_frame_press, add="+")
        widget.bind("<ButtonRelease-1>", self._on_frame_release, add="+")
        widget.bind("<B1-Motion>", self._on_frame_drag, add="+")
    def _on_frame_press(self, event):
        if not self.parent.selected_node == self:
            self.update_selected_node()
        widget = event.widget
        # 드래그 시작 시, 마우스 위치와 노드 좌표 저장
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_data["last_x"] = event.x
        self._drag_data["last_y"] = event.y
        self._drag_data["moved"] = False
    def update_selected_node(self):
        self.parent.selected_node=self
        self.nodeDetailView.node=self
        self.nodeFunction.updateDetailUI()
        
    def _on_frame_release(self, event):
        # 드래그가 아니면(즉 클릭)만 선택 처리
        if not self._drag_data.get("moved", False):

            ctrl_pressed = (event.state & 0x0004) != 0  # Ctrl 키 체크
            if ctrl_pressed:
                self.select(ctrl=True)
            else:
                self.select(ctrl=False)
        self.parent.updateSelectedNode()
    def _on_frame_drag(self, event):
        # 마우스가 눌린 위치와 현재 위치의 차이 계산
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        # frame_window를 새 위치로 이동
        self._drag_data["last_x"] = event.x
        self._drag_data["last_y"] = event.y
        if dx != 0 or dy != 0:
            self._drag_data["moved"] = True
        else:
            return
        for _,node in self.parent.selected_nodes.items():
            node.move(dx,dy)

class NodeFunction:
    def __init__(self) -> None:
        from NodeView.Node import NodeBlock
        from NodeDetailView.NodeDetailView import NodeDetailView
        self.description = ""
        self.nodeName = ""
        self.values = {
            # "input1": {"value": 0, "display": True,"type":"int"},
        }
        self.outputs = {
            # "output1": 0,
        }
        self.block : Optional[NodeBlock] = None
        self.nodeDetailView: Optional[NodeDetailView] = None
        self.nodeUI_widget={
            # "key":widget
        }
    def functions(self):
        # return []
        pass
    def updateDetailUI(self):
        self.nameUI()
        self.inputUI()
        self.outputUI()
    def nameUI(self):
        nodeDetailView=self.nodeDetailView
        nodeDetailView.node_name_textbox.delete(0, tk.END)
        nodeDetailView.node_name_textbox.insert(0, self.nodeName)
        nodeDetailView.description_textbox.delete(0, tk.END)
        nodeDetailView.description_textbox.insert(0, self.description)

        priority=self.block.priority if self.block else ""
        nodeDetailView.priority_textbox.delete(0,tk.END)
        nodeDetailView.priority_textbox.insert(0, priority)
    def inputUI(self):
        for widget in self.nodeDetailView.middle_section.winfo_children():
            widget.destroy()
        for key, value in self.values.items():
            frame = tk.Frame(self.nodeDetailView.middle_section, bg="lightyellow")
            frame.pack(fill=tk.X, padx=5, pady=2)

            check_var = tk.BooleanVar(value=value.get("display", False))
            check_button = tk.Checkbutton(frame, variable=check_var, bg="lightyellow", command=lambda k=key, l=key: self.block.on_check(k, l) if self.nodeUI is not None else None)
            check_button.pack(side=tk.LEFT)

            label = tk.Label(frame, text=key, bg="lightyellow")
            label.pack(side=tk.LEFT, padx=5)

            text_frame = tk.Frame(frame, bg="lightyellow")
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            widget_type = value.get("type", "text")
            if widget_type == "int":
                text_widget = self._create_int_widget(text_frame, key, value)
            elif widget_type == "str":
                text_widget = self._create_str_widget(text_frame, key, value)
            elif widget_type == "list":
                text_widget = self._create_list_widget(text_frame, key, value)
            else:
                text_widget = self._create_default_widget(text_frame, key, value)
            check_var.trace_add("write", lambda *args, key=key, check_var=check_var: self.nodeDetailView.update_node_display(key, check_var.get()) if self.nodeDetailView.node else None)
            self.nodeDetailView.value_widgets[key] = (text_widget, check_var)

    def _create_int_widget(self, text_frame, key, value):
        text_widget = tk.Spinbox(text_frame, from_=0, to=100, width=8)
        text_widget.delete(0, tk.END)
        text_widget.insert(0, str(value.get("value", "")))
        text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

        text_widget.bind("<KeyRelease>", lambda event, k=key, w=text_widget: self.on_int_spinbox_change(k, w), add="+")
        text_widget.bind("<ButtonRelease>", lambda event, k=key, w=text_widget: self.on_int_spinbox_change(k, w), add="+")
        return text_widget
    
    def on_int_spinbox_change(self, key, text_widget):
        
        v = int(text_widget.get())
        print()
        self.values[key]["value"]=v
        return v
    def _create_str_widget(self, text_frame, key, value):
        text_widget = tk.Text(text_frame, height=1, wrap="none")
        text_widget.insert("1.0", value.get("value", ""))
        text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        text_widget.bind("<KeyRelease>", lambda event, key=key, text_widget=text_widget: self.on_text_change(event, key, text_widget, self.nodeDetailView), add="+")
        return text_widget

    def _create_list_widget(self, text_frame, key, value):
        list_values = value.get("value", [])
        # Listbox on top
        listbox = tk.Listbox(text_frame, height=5, selectmode=tk.SINGLE)
        for item in list_values:
            listbox.insert(tk.END, item)
        n = value.get('n', 0)
        listbox.selection_set(n)
        listbox.activate(n)
        listbox.see(n)
        listbox.pack(side=tk.TOP, fill=tk.X, expand=True)
        listbox.bind("<<ListboxSelect>>",self.on_listbox_select, add="+")
        

        listbox.bind("<Button-3>", lambda event, key=key, listbox=listbox: self.on_listbox_right_click(listbox.nearest(event.y)), add="+")

        # Add frame below the listbox
        add_frame = tk.Frame(text_frame, bg="lightyellow")
        add_frame.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2,0))
        add_entry = tk.Entry(add_frame, width=8)
        add_entry.pack(side=tk.LEFT)
        add_button = tk.Button(add_frame, text="+", command=lambda key=key, listbox=listbox, add_entry=add_entry: self.on_listbox_add_item(key, listbox, add_entry), bg="lightyellow")
        add_button.pack(side=tk.LEFT)



        add_entry.bind("<Return>", lambda event, key=key, listbox=listbox, add_entry=add_entry: self.on_listbox_entry_key(event, key, listbox, add_entry), add="+")
        add_entry.bind("<Shift-Return>", lambda event, key=key, listbox=listbox, add_entry=add_entry: self.on_listbox_entry_key(event, key, listbox, add_entry), add="+")

        return listbox

    def on_listbox_entry_key(self, event, key, listbox, add_entry):
        if event.keysym == "Return" and not (event.state & 0x0001):  # Enter only
            self.on_listbox_add_item(key, listbox, add_entry)
            return "break"
        elif event.keysym == "Return" and (event.state & 0x0001):  # Shift+Enter
            # Insert newline at cursor
            idx = add_entry.index(tk.INSERT)
            current = add_entry.get()
            add_entry.delete(0, tk.END)
            add_entry.insert(0, current[:idx] + "\n" + current[idx:])
            add_entry.icursor(idx + 1)
            return "break"
    def on_listbox_right_click(self, index):
        # Remove the item at the given index from the list value
        (listbox,_)=self.nodeDetailView.value_widgets["list"]
        value_list = self.values["list"]["value"]
        value_list.pop(index)
        listbox.delete(index)
    def on_listbox_add_item(self, key=None, listbox=None, add_entry=None):
        new_item = add_entry.get()
        self.values[key]["value"].append(new_item)
        listbox.insert(tk.END, new_item)
        add_entry.delete(0, tk.END)
        return new_item
    def on_listbox_select(self, event):
        src = event.widget
        if not src.curselection():
            return src ,None

        index = src.curselection()[0]
        if self.values["list"]["n"] == index:
            return src , None
        self.values["list"]["n"] = index
        return src,index

    def _create_default_widget(self, text_frame, key, value):
        text_widget = tk.Text(text_frame, height=5, wrap="none")
        text_widget.insert("1.0", value.get("value", ""))
        v_scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = tk.Scrollbar(text_frame, orient="horizontal", command=text_widget.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        def _resize_text(event, text_widget=text_widget):
            text_widget.config(width=max(10, int(text_widget.winfo_width() / 8)), height=5)
        text_frame.bind("<Configure>", _resize_text, add="+")
        text_widget.bind("<KeyRelease>", lambda event, key=key, text_widget=text_widget: self.on_text_change(event, key, text_widget, self.nodeDetailView), add="+")
        return text_widget
    def outputUI(self):
        for widget in self.nodeDetailView.bottom_section.winfo_children():
            widget.destroy()
        for key, value in self.outputs.items():
            frame = tk.Frame(self.nodeDetailView.bottom_section, bg="lightpink")
            frame.pack(fill=tk.X, padx=5, pady=2)

            label = tk.Label(frame, text=key, bg="lightpink")
            label.pack(side=tk.LEFT, padx=5)

            text_frame = tk.Frame(frame, bg="lightpink")
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            v_scrollbar = None
            h_scrollbar = None
            
                            # 기본: Text 위젯, 여러 줄
            text_widget = tk.Text(text_frame, height=5, wrap="none")
            if not value:
                value=""
            text_widget.insert("1.0", value)
            # Vertical scrollbar (right)
            v_scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            # Horizontal scrollbar (bottom, spans under the text widget)
            h_scrollbar = tk.Scrollbar(text_frame, orient="horizontal", command=text_widget.xview)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            text_widget.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            def _resize_text(event, text_widget=text_widget):
                text_widget.config(width=max(10, int(text_widget.winfo_width() / 8)), height=5)
            text_frame.bind("<Configure>", _resize_text, add="+")
            text_widget.bind("<KeyRelease>", lambda event, key=key, text_widget=text_widget: self.on_result_change(event, key, text_widget, self.nodeDetailView), add="+")
            self.nodeDetailView.output_widgets[key] = text_widget

    def on_text_change(self, event, key, text_widget, nodeDetailView):
        value = text_widget.get("1.0", tk.END).rstrip("\n")
        self.values[key]["value"] = value
    def on_result_change(self, event, key, text_widget, nodeDetailView):
        value = text_widget.get("1.0", tk.END).rstrip("\n")
        self.outputs[key]= value
        nodeDetailView.update_node_output(key, value)
    def nodeUI(self):
        pass
        # nodeBlock.nodeName = tk.Label(nodeBlock.function_frame, text=f"Node : {self.nodeName}", bg="white")
        # nodeBlock.nodeName.grid(row=1, column=1, sticky="w", padx=(0,2), pady=(2,0))
        # nodeBlock.hello_entry = tk.Entry(self.block.frame, width=12)
        # nodeBlock.hello_entry.grid(row=1, column=2, columnspan=2, sticky="w", padx=(0,2), pady=(2,0))
        # frame_window가 Frame이고, 내부에 canvas가 있다면 사용
        # frame_window가 tk.Frame인 경우에는 별도 처리하지 않음
class NodeButtonFrame:
    def __init__(self,button_frame,nodeName,nodeblock:NodeBlock) -> None:
        self.play_button = self.createButton(button_frame, "▶", "green", lambda: nodeblock.on_play(None), row=0, column=1)
        self.stop_button = self.createButton(button_frame, "■", "gray", lambda: nodeblock.on_stop(None), row=0, column=2)
        self.delete_button = self.createButton(button_frame, "X", "gray", lambda: nodeblock.on_delete(None), row=0, column=3)
        self.nodeName_label = tk.Label(button_frame, text=nodeName, bg="white")
        self.nodeName_label.grid(row=0, column=0, sticky="w", padx=(2,2), pady=(2,0))
    def createButton(self, parent, text, bg, command, row, column):
        btn = tk.Button(parent, text=text, bg=bg, fg="white", width=2, height=1, command=command)
        btn.grid(row=row, column=column, sticky="e", padx=(0,2), pady=(2,0))
        return btn