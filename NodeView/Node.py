
import tkinter as tk
from typing import Optional

class BaseNode:
    def __init__(self) -> None:
        self.description = ""
        self.nodeName = ""
        self.values = {
            # "input1": {"value": 0, "display": True,"type":"int"},
        }
        self.outputs = {
            # "output1": 0,
        }
        self.nodeUI: Optional[Node] = None
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
            check_button = tk.Checkbutton(frame, variable=check_var, bg="lightyellow", command=lambda k=key, l=key: self.nodeUI.on_check(k, l))
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


class Node:
    def __init__(self, parent, Node_class: BaseNode, x1, y1, x2, y2):
        self.ChildNode = {}
        self.nodeClass = Node_class
        Node_class.nodeUI = self
        self.parent  = parent
        parent.node_num+=1
        node_id=self.parent.node_num
        self.priority = node_id  # 우선순위 속성 추가
        self.node_id=node_id
        self.rect = parent.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags=node_id)
        self.text = parent.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.nodeClass.nodeName, tags=node_id)
        # All pin creation and mapping handled in create_pins
        self.pins = self.create_pins(parent.canvas, x1, y1, y2, x2)

        # Play button
        self.play_button = parent.canvas.create_rectangle(x2 - 45, y1, x2 - 30, y1 + 15, fill="green", tags=node_id)
        self.play_text = parent.canvas.create_text(x2 - 37, y1 + 7, text="▶", fill="white", tags=node_id)
        parent.canvas.tag_bind(self.play_button, "<Button-1>", self.on_play)
        parent.canvas.tag_bind(self.play_text, "<Button-1>", self.on_play)

        # Stop button (square, with text)
        self.stop_button_state = False  # False: gray, True: red
        self.stop_button = parent.canvas.create_rectangle(x2 - 30, y1, x2 - 15, y1 + 15, fill="gray", tags=node_id)
        self.stop_text = parent.canvas.create_text(x2 - 22, y1 + 7, text="■", fill="white", tags=node_id)
        parent.canvas.tag_bind(self.stop_button, "<Button-1>", self.on_stop)
        parent.canvas.tag_bind(self.stop_text, "<Button-1>", self.on_stop)

        # Delete button
        self.delete_button = parent.canvas.create_rectangle(x2 - 15, y1, x2, y1 + 15, fill="gray", tags=node_id)
        self.delete_text = parent.canvas.create_text(x2 - 7, y1 + 7, text="X", fill="white", tags=node_id)
        parent.canvas.tag_bind(self.delete_button, "<Button-1>", self.on_delete)
        parent.canvas.tag_bind(self.delete_text, "<Button-1>", self.on_delete)
    def on_stop(self, event):
        # Toggle stop button color between gray and red
        self.stop_button_state = not self.stop_button_state
        color = "red" if self.stop_button_state else "gray"
        self.parent.canvas.itemconfig(self.stop_button, fill=color)


    def move(self, dx, dy):
        self.parent.canvas.move(self.rect, dx, dy)
        self.parent.canvas.move(self.text, dx, dy)
        # Move input pins and texts
        for pin_types in self.pins.values():
            for pin_type in pin_types.values():
                for pin in pin_type:
                    self.parent.canvas.move(pin, dx, dy)
        # Move the delete button and its text
        self.parent.canvas.move(self.delete_button, dx, dy)
        self.parent.canvas.move(self.delete_text, dx, dy)
        # Move the play button and its text
        self.parent.canvas.move(self.play_button, dx, dy)
        self.parent.canvas.move(self.play_text, dx, dy)
        # Move the stop button and its text
        self.parent.canvas.move(self.stop_button, dx, dy)
        self.parent.canvas.move(self.stop_text, dx, dy)

        # Update connected lines using Connection class
        # all_pins now contains (pin, text) tuples, so extract pin only
        all_pins = [pin for (pin, text) in self.pins['input_pin'].values()] + [pin for (pin, text) in self.pins['output_pin'].values()]
        for connection in self.parent.canvas.master.connections.values():
            if (connection.input_pin in all_pins) or (connection.output_pin in all_pins):
                start_coords = self.parent.canvas.coords(connection.output_pin)
                end_coords = self.parent.canvas.coords(connection.input_pin)
                self.parent.canvas.coords(
                    connection.line_id,
                    (start_coords[0] + start_coords[2]) // 2,
                    (start_coords[1] + start_coords[3]) // 2,
                    (end_coords[0] + end_coords[2]) // 2,
                    (end_coords[1] + end_coords[3]) // 2
                )

    def get_coords(self):
        return self.parent.canvas.coords(self.rect)

    def is_inside(self, x, y):
        coords = self.get_coords()
        return coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]

    def on_delete(self, event):
        # Remove all associated canvas items
        self.parent.canvas.delete(self.rect)
        self.parent.canvas.delete(self.text)
        # Delete input pins and texts
        input_texts = self.pins['input_texts'] if 'input_texts' in self.pins else []
        for pin_types in self.pins.values():
            for pin,text in pin_types.values():
                self.parent.canvas.delete(pin)
                self.parent.canvas.delete(text)
                self.parent.canvas.master.remove_connection(pin)  # Remove connections for input pins
        # Delete output pins and texts
        self.parent.canvas.delete(self.delete_button)
        self.parent.canvas.delete(self.delete_text)
        # Remove the play button and its text
        self.parent.canvas.delete(self.play_button)
        self.parent.canvas.delete(self.play_text)
        # Remove the stop button and its text
        self.parent.canvas.delete(self.stop_button)
        self.parent.canvas.delete(self.stop_text)
        # Remove the node from the center frame's node dictionary
        for node_id, node in self.parent.canvas.master.nodes.items():
            if node == self:
                del self.parent.canvas.master.nodes[node_id]
                break
        # Update RightFrame with a new BaseNode instance
        self.parent.canvas.master.parent.right_frame.update_node_details(BaseNode())

    def on_play(self, event):
        # Priority queue: (priority, node)
        play_functions = [(self.priority, self)]
        while play_functions:
            # Pop node with smallest priority
            play_functions.sort(key=lambda x: x[0])
            priority, node = play_functions.pop(0)
            try:
                outputValues=node.nodeClass.functions()
                # Update child nodes and add them to play_functions
                for input_node, dic in node.ChildNode.items():
                    for output, inputList in dic.items():
                        if outputValues and not (output in outputValues):
                            continue
                        for input in inputList:
                            input_node.nodeClass.values[input]["value"] = node.nodeClass.outputs[output]
            except Exception as e:
                print(f"Error executing functions for node {node.node_id}: {e}")
        node.nodeClass.updateNodeDetailUi(node.parent.parent.right_frame)
    def create_pins(self, canvas, x1, y1, y2, x2):
        # Prepare input and output keys
        input_keys = [k for k, v in self.nodeClass.values.items() if v.get("display", False)]
        output_keys = [k for k in self.nodeClass.outputs.keys()]

        # Remove 'input' from input_keys if present
        input_keys = [label for label in input_keys if label != 'input']

        # Create input pins
        input_pins = []
        input_texts = []
        num_inputs = len(input_keys)
        for i, label in enumerate(input_keys):
            pin_y = y1 + (i + 1) * (y2 - y1) // (num_inputs + 1)
            pin, text = self.create_pin(canvas, x1, pin_y, 'input', label)
            input_pins.append(pin)
            input_texts.append(text)

        # Create output pins
        output_pins = []
        output_texts = []
        num_outputs = len(output_keys)
        for i, label in enumerate(output_keys):
            pin_y = y1 + (i + 1) * (y2 - y1) // (num_outputs + 1)
            pin, text = self.create_pin(canvas, x2, pin_y, 'output', label)
            output_pins.append(pin)
            output_texts.append(text)

        # pins dict structure: {'input_pin': {text: pin, ...}, 'output_pin': {text: pin, ...},
        #   'input_pins': [...], 'input_texts': [...], 'output_pins': [...], 'output_texts': [...]}
        return {
            'input_pin': {key: (pin,text) for text, pin,key in zip(input_texts, input_pins,input_keys)},
            'output_pin': {key: (pin,text) for text, pin,key in zip(output_texts, output_pins,output_keys)},
        }

    def create_pin(self, canvas, x, pin_y, pin_type, label):
        if pin_type == "input":
            pin_x1, pin_y1 = x - 10, pin_y - 5
            pin_x2, pin_y2 = x, pin_y + 5
            pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="white")
            text = canvas.create_text(pin_x1 - 20, pin_y, anchor="e", text=label)
            canvas.tag_bind(pin, "<Button-1>", lambda event, pin=pin, pin_type=pin_type, label=label: self.on_pin_click(pin, pin_type, label))
        elif pin_type == "output":
            pin_x1, pin_y1 = x, pin_y - 5
            pin_x2, pin_y2 = x + 10, pin_y + 5
            pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="white")
            text = canvas.create_text(pin_x2 + 20, pin_y, anchor="w", text=label)
            canvas.tag_bind(pin, "<Button-1>", lambda event, pin=pin, pin_type=pin_type, label=label: self.on_pin_click(pin, pin_type, label))
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
            pass
        else:
            pin,text=self.pins["input_pin"].pop(key)
            self.parent.canvas.delete(pin)
            self.parent.canvas.delete(text)
            self.parent.canvas.master.remove_connection(pin) 
        print(f"Checkbutton clicked for key: {key}, label: {label}, checked: {checked}")
