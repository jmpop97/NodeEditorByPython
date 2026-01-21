import tkinter as tk
from typing import Optional

class nodeFuction:
    def __init__(self) -> None:
        self.description = ""
        self.nodeName = ""
        self.values = {
            # "input1": {"value": 0, "display": True,"type":"int"},
        }
        self.outputs = {
            # "output1": 0,
        }
    def functions(self):
        # return []
        pass
    def updateNodeDetailUi(self, right_frame=None):
        """
        Update the UI in the given RightFrame to reflect this node's details.
        """
        if right_frame is None:
            return
        right_frame.node_name_textbox.delete(0, right_frame.node_name_textbox.get().__len__())
        right_frame.node_name_textbox.delete(0, 'end')
        right_frame.node_name_textbox.insert(0, self.nodeName)
        right_frame.description_textbox.delete(0, 'end')
        right_frame.description_textbox.insert(0, self.description)
        for widget in right_frame.middle_section.winfo_children():
            widget.destroy()
        right_frame.value_widgets.clear()
        self.inputUI(right_frame)
        for widget in right_frame.bottom_section.winfo_children():
            widget.destroy()
        right_frame.output_labels.clear()
        self.outputUI(right_frame)

    def outputUI(self, right_frame):
        for key, value in self.outputs.items():
            frame = tk.Frame(right_frame.bottom_section, bg="lightpink")
            frame.pack(fill=tk.X, padx=5, pady=2)
            label = tk.Label(frame, text=f"{key}:", bg="lightpink")
            label.pack(side=tk.LEFT, padx=(0,5))
            text_widget = tk.Text(frame, height=2, wrap="word", bg="#ffe4ec")
            text_widget.insert("1.0", str(value))
            text_widget.config(state="disabled")
            text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
            right_frame.output_labels[key] = text_widget

    def inputUI(self, right_frame):
        for key, value in self.values.items():
            frame = tk.Frame(right_frame.middle_section, bg="lightyellow")
            frame.pack(fill=tk.X, padx=5, pady=2)
            check_var = tk.BooleanVar(value=value.get("display", False))
            check_button = tk.Checkbutton(frame, variable=check_var, bg="lightyellow", command=lambda k=key, l=key: self.nodeUI.on_check(k, l) if self.nodeUI is not None else None)
            check_button.pack(side=tk.LEFT)
            label = tk.Label(frame, text=key, bg="lightyellow")
            label.pack(side=tk.LEFT, padx=5)
            text_frame = tk.Frame(frame, bg="lightyellow")
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            v_scrollbar = None
            h_scrollbar = None
            widget_type = value.get("type", "text")
            if widget_type == "int":
                # Entry 위젯 (작게)
                text_widget = tk.Entry(text_frame, width=8)
                text_widget.insert(0, str(value.get("value", "")))
                text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                def on_entry_change(event, key=key, text_widget=text_widget):
                    if right_frame.node:
                        try:
                            value = int(text_widget.get())
                        except ValueError:
                            value = 0
                        right_frame.update_node_value(key, value)
                text_widget.bind("<KeyRelease>", on_entry_change)
            elif widget_type == "str":
                # Text 위젯, 한 줄만 보이게
                text_widget = tk.Text(text_frame, height=1, wrap="none")
                text_widget.insert("1.0", value.get("value", ""))
                text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                def on_text_change(event, key=key, text_widget=text_widget):
                    if right_frame.node:
                        right_frame.update_node_value(key, text_widget.get("1.0", tk.END).rstrip("\n"))
                text_widget.bind("<KeyRelease>", on_text_change)
            else:
                # 기본: Text 위젯, 여러 줄
                text_widget = tk.Text(text_frame, height=5, wrap="none")
                text_widget.insert("1.0", value.get("value", ""))
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
                text_frame.bind("<Configure>", _resize_text)
                def on_text_change(event, key=key, text_widget=text_widget):
                    if right_frame.node:
                        right_frame.update_node_value(key, text_widget.get("1.0", tk.END).rstrip("\n"))
                text_widget.bind("<KeyRelease>", on_text_change)
            check_var.trace_add("write", lambda *args, key=key, check_var=check_var: right_frame.update_node_display(key, check_var.get()) if right_frame.node else None)
            right_frame.value_widgets[key] = (text_widget, check_var)

    def nodeUI(self, nodeBlock):
        nodeBlock.hello_label = tk.Label(nodeBlock.frame, text="안녕", bg="white")
        nodeBlock.hello_label.grid(row=1, column=1, sticky="w", padx=(0,2), pady=(2,0))
        nodeBlock.hello_entry = tk.Entry(nodeBlock.frame, width=12)
        nodeBlock.hello_entry.grid(row=1, column=2, columnspan=2, sticky="w", padx=(0,2), pady=(2,0))
        # frame_window가 Frame이고, 내부에 canvas가 있다면 사용
        # frame_window가 tk.Frame인 경우에는 별도 처리하지 않음
class NodeBlock:
    def __init__(self, parent, Node_class, x, y, width=150, height=100):
        self.ChildNode = {}
        self.rectPoint = (x,y,width,height)
        self.parent  = parent
        self.nodeClass = Node_class()
        (x1,y1,x2,y2) = self.rectPoint
        parent.node_num+=1
        node_id=self.parent.node_num
        self.priority = node_id  # 우선순위 속성 추가
        self.node_id=node_id
        # self.nodeClass.createNodeUI()
        # All pin creation and mapping handled in create_pins
        self.pins = {
            "input_pin":{},
            "output_pin":{}
            }
        self.frame = tk.Frame(parent.canvas.master, bg="white", highlightthickness=0)
        self.frame_window = parent.canvas.create_window(x1, y1, anchor="nw", window=self.frame, width=width, height=height)
        
        self._drag_data = {"x": 0, "y": 0, "last_x": 0, "last_y": 0, "moved": False}
        self.frame.bind("<ButtonPress-1>", self._on_frame_press)
        self.frame.bind("<ButtonRelease-1>", self._on_frame_release)  # <- 새로 추가
        self.frame.bind("<B1-Motion>", self._on_frame_drag)
        
        self.create_pins(parent.canvas)

        # Create a frame for buttons at the top (height 10)
        self.button_frame = tk.Frame(self.frame, bg="white", height=10)
        self.button_frame.pack(fill=tk.X, side=tk.TOP)
        self.button_frame.bind("<ButtonPress-1>", self._on_frame_press)
        self.button_frame.bind("<B1-Motion>", self._on_frame_drag)
        # Create a frame for function UI below the button frame
        self.function_frame = tk.Frame(self.frame, bg="white")
        self.function_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.function_frame.bind("<ButtonPress-1>", self._on_frame_press)
        self.function_frame.bind("<B1-Motion>", self._on_frame_drag)
        # Move buttons to button_frame
        self.stop_button_state = False  # False: gray, True: red
        # Add a stretchable empty column to push buttons to the right
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.play_button = self.createButton(self.button_frame, "▶", "green", lambda: self.on_play(None), row=0, column=1)
        self.stop_button = self.createButton(self.button_frame, "■", "gray", lambda: self.on_stop(None), row=0, column=2)
        self.delete_button = self.createButton(self.button_frame, "X", "gray", lambda: self.on_delete(None), row=0, column=3)
        # self.nodeClass.nodeUI(self)
        self.selected = False
        self.selection_border_id = None
        
    def createButton(self, parent, text, bg, command, row, column):
        btn = tk.Button(parent, text=text, bg=bg, fg="white", width=2, height=1, command=command)
        btn.grid(row=row, column=column, sticky="e", padx=(0,2), pady=(2,0))
        return btn

    def _on_frame_press(self, event):
        widget = event.widget
        abs_x = widget.winfo_rootx() + event.x
        abs_y = widget.winfo_rooty() + event.y
        self._drag_data["x"] = abs_x
        self._drag_data["y"] = abs_y
        self._drag_data["last_x"] = abs_x
        self._drag_data["last_y"] = abs_y
        # Do not clear selected_nodes on click-drag
        ctrl_pressed = (event.state & 0x0004) != 0  # Tkinter state mask for Ctrl
        if ctrl_pressed:
            self.select(ctrl=True)
        else:
            self.select(ctrl=False)
        # Do not modify parent.selected_nodes here to preserve selection during drag

    def select(self, ctrl=False):
        if ctrl:
            if self.selected:
                self.set_selected(False)
                self.frame.config(bg="white")
                if self.node_id in self.parent.selected_nodes:
                    del self.parent.selected_nodes[self.node_id]
            else:
                self.set_selected(True)
                self.parent.selected_nodes[self.node_id] = self
                self.frame.config(bg="blue")
        else:
            # Deselect all nodes except this one
            for n in self.parent.nodes.values():
                n.set_selected(False)
                if hasattr(n, 'frame'):
                    n.frame.config(bg="white")
            self.parent.selected_nodes.clear()
            self.set_selected(True)
            self.parent.selected_nodes[self.node_id] = self
            self.frame.config(bg="blue")
    def _on_frame_drag(self, event):
        widget = event.widget
        abs_x = widget.winfo_rootx() + event.x
        abs_y = widget.winfo_rooty() + event.y
        dx = abs_x - self._drag_data["last_x"]
        dy = abs_y - self._drag_data["last_y"]
        self._drag_data["last_x"] = abs_x
        self._drag_data["last_y"] = abs_y
        if dx != 0 or dy != 0:
            self._drag_data["moved"] = True  # 실제로 움직였으면 moved 플래그 True
        self.move(dx, dy)

    def _on_frame_release(self, event):
        # 드래그가 아니면(즉 클릭)만 선택 처리
        if not self._drag_data.get("moved", False):
            ctrl_pressed = (event.state & 0x0004) != 0  # Ctrl 키 체크
            if ctrl_pressed:
                self.select(ctrl=True)
            else:
                self.select(ctrl=False)
    def on_stop(self, event):
        # Toggle stop button color between gray and red
        self.stop_button_state = not self.stop_button_state
        color = "red" if self.stop_button_state else "gray"
        self.parent.canvas.itemconfig(self.stop_button, fill=color)


    def set_selected(self, selected: bool):
        self.selected = selected
        if selected:
            # Draw blue border rectangle around the node frame
            x, y, width, height = self.rectPoint
            if self.selection_border_id is not None:
                self.parent.canvas.delete(self.selection_border_id)
            self.selection_border_id = self.parent.canvas.create_rectangle(
                x-2, y-2, x+width+2, y+height+2,
                outline="blue", width=3
            )
            # Move border below pins but above frame
            self.parent.canvas.tag_lower(self.selection_border_id, self.frame_window)
            # Also set frame color to blue
            self.frame.config(bg="blue")
        else:
            if self.selection_border_id is not None:
                self.parent.canvas.delete(self.selection_border_id)
                self.selection_border_id = None
            # Reset frame color to white
            self.frame.config(bg="white")

    def get_coords(self):
        x, y, width, height = self.rectPoint
        return (x, y, width, height)

    def move(self, dx, dy):
        # Move all selected nodes if self is in selected_nodes, else move only self
        selected_nodes = getattr(self.parent, 'selected_nodes', None)
        if selected_nodes and self in selected_nodes:
            for node in selected_nodes:
                node._move_single(dx, dy)
        else:
            self._move_single(dx, dy)

    def _move_single(self, dx, dy):
        x, y, width, height = self.rectPoint
        self.rectPoint = (x + dx, y + dy, width, height)
        self.parent.canvas.move(self.frame_window, dx, dy)
        for pin_types in self.pins.values():
            for pin_tuple in pin_types.values():
                pin, text, _ = pin_tuple
                self.parent.canvas.move(pin, dx, dy)
                self.parent.canvas.move(text, dx, dy)
        if self.selected and self.selection_border_id is not None:
            self.parent.canvas.move(self.selection_border_id, dx, dy)

    def on_delete(self, event):
        # Delete input pins and texts
        for pin_types in self.pins.values():
            for pin,text,_ in pin_types.values():
                self.parent.canvas.delete(pin)
                self.parent.canvas.delete(text)
                self.parent.canvas.master.remove_connection(pin)  # Remove connections for input pins
        self.frame.destroy()
        self.parent.canvas.delete(self.frame_window)
        if self.selection_border_id is not None:
            self.parent.canvas.delete(self.selection_border_id)

        # # Remove the node from the center frame's node dictionary
        # for node_id, node in self.parent.canvas.master.nodes.items():
        #     if node == self:
        #         del self.parent.canvas.master.nodes[node_id]
        #         break
        # # Update RightFrame with a new BaseNode instance
        # self.parent.canvas.master.parent.right_frame.update_node_details(nodeFuction(None))

    def on_play(self, event):
        # Priority queue: (priority, node)
        play_functions = [(self.priority, self)]
        while play_functions:
            # Pop node with smallest priority
            play_functions.sort(key=lambda x: x[0])
            priority, node = play_functions.pop(0)
            try:
                outputValues = node.nodeClass.functions()
                # Update child nodes and add them to play_functions
                print(node.ChildNode)
                print(outputValues)
                for input_node, dic in node.ChildNode.items():
                    for output, inputList in dic.items():
                        if outputValues and not (output in outputValues):
                            continue
                        for input in inputList:
                            input_node.nodeClass.values[input]["value"] = node.nodeClass.outputs[output]
                        # Add input_node to play_functions if not already in play_functions
                    if not any(n == input_node for _, n in play_functions):
                        play_functions.append((input_node.priority, input_node))
            except Exception as e:
                print(f"Error executing functions for node {node.node_id}: {e}")
        node.nodeClass.updateNodeDetailUi(node.parent.parent.right_frame)
    def create_pins(self, canvas):
        # Prepare input and output keys
        input_keys = [k for k, v in self.nodeClass.values.items() if v.get("display", False)]
        output_keys = [k for k in self.nodeClass.outputs.keys()]

        # Remove 'input' from input_keys if present
        for label in input_keys:
            self.create_pin(canvas, 'input', label) 
        for label in output_keys:
            self.create_pin(canvas, 'output', label)


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
            canvas.tag_bind(pin, "<Button-1>", lambda event, pin=pin, pin_type=pin_type, label=label: self.on_pin_click(pin, pin_type, label))
            self.pins["input_pin"][label] = (pin, text, num)
        elif pin_type == "output":
            x2 = x + width+5  # output은 x+width
            num = self.set_pin_num("output_pin")
            y += num * 10
            pin_x1, pin_y1 = x2 - 5, y - 5
            pin_x2, pin_y2 = x2 + 5, y + 5
            pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="white")
            text = canvas.create_text(pin_x2 + 20, pin_y2, anchor="w", text=label)
            canvas.tag_bind(pin, "<Button-1>", lambda event, pin=pin, pin_type=pin_type, label=label: self.on_pin_click(pin, pin_type, label))
            self.pins["output_pin"][label] = (pin, text, num)
        else:
            pin = None
            text = None
        return pin, text
    def on_pin_click(self, pin,pin_type,label):
        print(f"Input pin '{pin}' pin_type '{pin_type}' clicked (Node: {self.nodeClass.nodeName})")
        # Delegate the pin click handling to the CenterFrame
        self.parent.on_pin_click(pin,pin_type,label,self)

    def on_input_pin_click(self, pin_label, node):
        print(f"Input pin '{pin_label}' clicked (Node: {self.nodeClass.nodeName})")

    def on_output_pin_click(self, pin_label, node):
        print(f"Output pin '{pin_label}' clicked (Node: {self.nodeClass.nodeName})")
    def on_check(self, key, label):
        right_frame = self.parent.parent.right_frame
        checked = right_frame.value_widgets[key][1].get()
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
