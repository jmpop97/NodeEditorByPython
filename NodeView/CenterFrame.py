import tkinter as tk
from tkinter import Canvas
from NodeView.Node import Node
from typing import Optional
import json
import os
from tkinter import messagebox
class Connection:
    def __init__(self, output_pin, input_pin, output_node, input_node,output_label,input_label, line_id):
        self.input_node = input_node
        self.output_label = output_label
        self.input_pin = input_pin
        self.output_node = output_node
        self.input_label = input_label
        self.output_pin = output_pin
        self.line_id = line_id
class NodeTopView(tk.Frame):
    def __init__(self, window, parent):
        super().__init__(parent, width=100, bg="white")
        self.parent = parent
        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(top_frame, text="Name:", bg="white").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(top_frame, width=15)
        self.name_entry.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(top_frame, text="Description:", bg="white").pack(side=tk.LEFT)
        self.desc_entry = tk.Entry(top_frame, width=25)
        self.desc_entry.pack(side=tk.LEFT, padx=(0, 10))

        save_btn = tk.Button(top_frame, text="저장", command=self.save_selected_node_info)
        save_btn.pack(side=tk.LEFT)

    def save_selected_node_info(self):
        # Save name/description to all selected nodes (if any)
        nodes = {}
        if not self.parent.selected_nodes:
            nodes = self.parent.nodes
        else:
            nodes = self.parent.selected_nodes
        # Sort nodes by node.priority (ascending)
        sorted_nodes = dict(sorted(nodes.items(), key=lambda item: getattr(item[1], 'priority', 0)))
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        save_dir = os.path.join(os.path.dirname(__file__), '..', 'funtions')
        os.makedirs(save_dir, exist_ok=True)

        # Save node info
        nodes_data = []
        node_id_dic = {}
        for i, node in enumerate(sorted_nodes.values()):
            node_name = i
            node_id_dic[node.node_id] = node_name
            coords = node.get_coords()

            node_data = {
                'node_id': node_name,
                'className': type(node.nodeClass).__name__,
                'nodeName': getattr(node.nodeClass, 'nodeName', type(node.nodeClass).__name__),
                'description': getattr(node.nodeClass, 'description', ''),
                'values': getattr(node.nodeClass, 'values', ''),
                'outputs': getattr(node.nodeClass, 'outputs', ''),
                'coords': coords,
            }
            nodes_data.append(node_data)

        # Save connections related to selected nodes
        connections_data = []
        for key, conn in self.parent.connections.items():
            output_node_id = getattr(conn.output_node, 'node_id', None)
            input_node_id = getattr(conn.input_node, 'node_id', None)
            if output_node_id in sorted_nodes and input_node_id in sorted_nodes:
                connections_data.append({
                    'output_node_id': node_id_dic[output_node_id],
                    'input_node_id': node_id_dic[input_node_id],
                    'output_label': conn.output_label,
                    'input_label': conn.input_label
                })

        # Find next available file number
        existing_files = [f for f in os.listdir(save_dir) if f.endswith('.json') and f[:-5].isdigit()]
        if existing_files:
            max_num = max([int(f[:-5]) for f in existing_files])
            next_num = max_num + 1
        else:
            next_num = 1
        file_name = f"{next_num}.json"
        file_path = os.path.join(save_dir, file_name)
        save_data = {
            'name': name,
            'desc': desc,
            'nodes': nodes_data,
            'connections': connections_data,
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        print("save", file_path)
        self.parent.parent.nodeListView.refresh()
        messagebox.showinfo("저장 완료", "노드 및 연결 정보가 성공적으로 저장되었습니다.")
        # Optionally, clear fields or show a message

class NodeView(tk.Frame):
    def __init__(self, window, parent):  # Pass app as parent
        super().__init__(window, width=200, bg="white")
        self.parent = parent  # Store the reference to the app
        self.pack_propagate(False)

        # --- NodeTopView (NodeView 내부 위쪽, name/desc/save UI) ---
        self.node_top_view = NodeTopView(window, self)
        self.node_top_view.pack(fill=tk.X, padx=5, pady=5)

        # Add a canvas to draw nodes
        self.canvas = Canvas(self, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Store references to nodes
        self.nodes = {}
        self.node_num=0
        self.selected_node: Optional[Node] = None
        self.selected_nodes: dict[int, Node] = {}  # For multi-selection, key=node_id
        self.select_rect_id = None  # Rectangle ID for selection box
        self.select_start = None  # (x, y) start position for selection
        self.selected_pin: dict[str, Optional[tuple[int, Node,str]]] = {
            "input": None,
            "output": None
        }  # Track the currently selected pin
        self.offset_x = 0
        self.offset_y = 0

        # Store connections as a dict: key=(start_pin, end_pin), value=Connection
        self.connections = {}

        # Bind mouse events for node interaction
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)  # Bind right-click to remove connection

    def add_node(self, node_class, x1=50, y1=50, x2=150, y2=100):
        # Create a new Node instance with multiple input and output pins
        node = Node(self, node_class, x1, y1, x2, y2)
        self.nodes[node.node_id] = node
        return node
    def add_nodes(self, nodes_info):
        nodes_data = nodes_info.get('nodes', [])
        connections_data = nodes_info.get('connections', [])
        nodeIdDic = {}
        # Restore nodes info and set nodeName, description, values, outputs
        for node_info in nodes_data:
            className = node_info.get('className')
            node_id = node_info.get('node_id')
            node_class = self.parent.nodeListView.get_node_by_classname(className)
            coords = node_info.get('coords', (50, 50, 150, 100))
            x1, y1, x2, y2 = coords
            node = self.add_node(node_class, x1, y1, x2, y2)
            # Set nodeName, description, values, outputs if present
            if hasattr(node, 'nodeClass'):
                if 'nodeName' in node_info:
                    setattr(node.nodeClass, 'nodeName', node_info['nodeName'])
                if 'description' in node_info:
                    setattr(node.nodeClass, 'description', node_info['description'])
                if 'values' in node_info:
                    setattr(node.nodeClass, 'values', node_info['values'])
                if 'outputs' in node_info:
                    setattr(node.nodeClass, 'outputs', node_info['outputs'])
            nodeIdDic[node_id] = node.node_id
        # Restore connections (only between existing nodes)
        for conn_info in connections_data:
            output_node_id = nodeIdDic.get(conn_info.get('output_node_id'))
            input_node_id = nodeIdDic.get(conn_info.get('input_node_id'))
            output_label = conn_info.get('output_label')
            input_label = conn_info.get('input_label')
            output_node = self.nodes.get(output_node_id)
            input_node = self.nodes.get(input_node_id)
            output_pin = None
            input_pin = None
            # Use pins dict for pin lookup by label (now returns (pin, text) tuple)
            if output_node and hasattr(output_node, 'pins'):
                output_pin_tuple = output_node.pins['output_pin'].get(output_label)
                if output_pin_tuple:
                    output_pin, _,_ = output_pin_tuple
                else:
                    output_pin = None
            if input_node and hasattr(input_node, 'pins'):
                input_pin_tuple = input_node.pins['input_pin'].get(input_label)
                if input_pin_tuple:
                    input_pin, _,_ = input_pin_tuple
                else:
                    input_pin = None
            if output_node and input_node and output_pin is not None and input_pin is not None:
                self.connect_pins(output_pin, input_pin, output_node, input_node, output_label, input_label)

    def connect_pins(self, output_pin, input_pin, output_node, input_node, output_label, input_label):
        # Prevent duplicate connections
        key = tuple(sorted([input_pin, output_pin], key=id))
        if key in self.connections:
            return  # Already connected, do not create again
        # Draw a line between the two pins
        start_coords = self.canvas.coords(output_pin)
        end_coords = self.canvas.coords(input_pin)
        line_id = self.canvas.create_line(
            (start_coords[0] + start_coords[2]) // 2,
            (start_coords[1] + start_coords[3]) // 2,
            (end_coords[0] + end_coords[2]) // 2,
            (end_coords[1] + end_coords[3]) // 2,
            fill="yellow",
            width=2
        )
        # Move the line behind the pins
        self.canvas.tag_lower(line_id)
        self.connections[key] = Connection(output_pin, input_pin, output_node, input_node, output_label, input_label, line_id)

    def remove_connection(self, pin):
        # Remove connections associated with a pin
        to_remove = []
        for key, connection in list(self.connections.items()):
            if pin == connection.input_pin or pin == connection.output_pin:
                self.canvas.delete(connection.line_id)
                # Remove from ChildNode mapping if present
                output_node = connection.output_node
                input_node = connection.input_node
                output_label = connection.output_label
                input_label = connection.input_label
                if hasattr(output_node, 'ChildNode') and input_node in output_node.ChildNode:
                    if output_label in output_node.ChildNode[input_node]:
                        label_list = output_node.ChildNode[input_node][output_label]
                        if input_label in label_list:
                            label_list.remove(input_label)
                        # Clean up empty lists and dicts
                        if not label_list:
                            del output_node.ChildNode[input_node][output_label]
                    if not output_node.ChildNode[input_node]:
                        del output_node.ChildNode[input_node]
                to_remove.append(key)
        for key in to_remove:
            del self.connections[key]

    def on_canvas_click(self, event):
        # Start selection rectangle
        self.select_start = (event.x, event.y)
        ctrl_pressed = (event.state & 0x0004) != 0  # 0x0004 is the mask for Control key
        self.selected_node = None
        overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        found_node = False
        for item in reversed(overlapping_items):
            for node_id, node in self.nodes.items():
                if item == node.rect and node.is_inside(event.x, event.y):
                    self.selected_node = node
                    coords = node.get_coords()
                    self.offset_x = event.x - coords[0]
                    self.offset_y = event.y - coords[1]
                    # Ctrl+Click: add/remove node from selection
                    if ctrl_pressed:
                        if node_id in self.selected_nodes:
                            del self.selected_nodes[node_id]
                            self.canvas.itemconfig(node.rect, outline="black", width=1)
                        else:
                            self.selected_nodes[node_id] = node
                            self.canvas.itemconfig(node.rect, outline="blue", width=3)
                    else:
                        # If already selected, do not reset selection (for drag)
                        if node_id in self.selected_nodes:
                            # Just prep for drag, keep selection
                            pass
                        else:
                            # Normal click: select only this node
                            self.selected_nodes = {node_id: node}
                            self.canvas.itemconfig(node.rect, outline="blue", width=3)
                            # Notify RightFrame about the selected node
                            if self.selected_node:
                                self.parent.right_frame.update_node_details(self.selected_node.nodeClass)
                    found_node = True
                    break
            if found_node:
                break
        if not found_node and not ctrl_pressed:
            # Clicked empty space: clear selection
            self.selected_nodes = {}
        # Reset all unselected nodes to default appearance
        for node_id, node in self.nodes.items():
            if node_id not in self.selected_nodes:
                self.canvas.itemconfig(node.rect, outline="black", width=1)

    def on_canvas_drag(self, event):
        # If a node is selected, drag all selected nodes together
        if self.selected_node:
            x, y = event.x - self.offset_x, event.y - self.offset_y
            coords = self.selected_node.get_coords()
            dx = x - coords[0]
            dy = y - coords[1]
            # Move all selected nodes (no duplicates)
            moved_ids = set()

            for node_id, node in self.selected_nodes.items():
                if node_id not in moved_ids:
                    node.move(dx, dy)
                    moved_ids.add(node_id)
        else:
            # Draw selection rectangle
            if self.select_start:
                x0, y0 = self.select_start
                x1, y1 = event.x, event.y
                if self.select_rect_id:
                    self.canvas.coords(self.select_rect_id, x0, y0, x1, y1)
                else:
                    self.select_rect_id = self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", dash=(2,2))
                # Highlight nodes inside the rectangle
                self.selected_nodes = {}
                for node_id, node in self.nodes.items():
                    nx1, ny1, nx2, ny2 = node.get_coords()
                    # Check if node is inside selection rectangle
                    if (min(x0, x1) <= nx1 and nx2 <= max(x0, x1) and
                        min(y0, y1) <= ny1 and ny2 <= max(y0, y1)):
                        self.selected_nodes[node_id] = node
                        self.canvas.itemconfig(node.rect, outline="blue", width=3)
                    else:
                        self.canvas.itemconfig(node.rect, outline="black", width=1)

    def on_release(self, event):
        # End selection rectangle
        if self.select_rect_id:
            self.canvas.delete(self.select_rect_id)
            self.select_rect_id = None
        self.select_start = None
        # If nodes were selected by rectangle, update their appearance
        if self.selected_nodes:
            for node_id, node in self.nodes.items():
                if node_id in self.selected_nodes:
                    self.canvas.itemconfig(node.rect, outline="blue", width=3)
                else:
                    self.canvas.itemconfig(node.rect, outline="black", width=1)
        self.selected_node = None

    def on_pin_click(self, pin, pin_type: str, label,node):
        # pin_type: 'input' or 'output'


        if self.selected_pin[pin_type] is None:
            self.selected_pin[pin_type] = (pin, node,label)
            self.canvas.itemconfig(pin, fill="red")
        else:
            past = self.selected_pin[pin_type]
            if past is not None:
                past_pin, past_node,label = past
                self.canvas.itemconfig(past_pin, fill="white")
                self.selected_pin[pin_type]=None
            if past_pin!=pin:
                self.selected_pin[pin_type] = (pin, node,label)
                self.canvas.itemconfig(pin, fill="red")
            return
        # Check if both pins are selected
        if self.selected_pin["input"] and self.selected_pin["output"]:
            (input_pin, input_node,input_label) = self.selected_pin["input"]
            (output_pin, output_node,output_label) = self.selected_pin["output"]
            # Connect pins
            self.connect_pins(output_pin, input_pin, output_node, input_node,output_label,input_label)
            # Reset pin colors
            self.canvas.itemconfig(input_pin, fill="white")
            self.canvas.itemconfig(output_pin, fill="white")
            self.selected_pin = {"input": None, "output": None}
        
    def on_right_click(self, event):
        # Detect if a line (connection) is clicked
        overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in overlapping_items:
            for key, connection in list(self.connections.items()):
                if item == connection.line_id:
                    self.canvas.delete(connection.line_id)
                    del self.connections[key]
                    return
