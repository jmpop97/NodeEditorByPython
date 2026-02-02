import tkinter as tk
from tkinter import Canvas

from typing import Optional
import json
import os
from tkinter import messagebox
from NodeListView.NodeListView import NodeListView
from NodeDetailView.NodeDetailView import NodeDetailView
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
    def __init__(self, parent):
        self.parent : NodeView = parent
        super().__init__(parent, width=100, bg="white")
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
            print("selected_nodes",self.parent.nodes)
        else:
            nodes = self.parent.selected_nodes
            print("selected_nodes",self.parent.selected_nodes)
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
            coords = node.rectPoint

            node_data = {
                'node_id': node_name,
                'className': type(node.nodeFunction).__name__,
                'nodeName': getattr(node.nodeFunction, 'nodeName', type(node.nodeFunction).__name__),
                'description': getattr(node.nodeFunction, 'description', ''),
                'values': getattr(node.nodeFunction, 'values', ''),
                'outputs': getattr(node.nodeFunction, 'outputs', ''),
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
        from NodeView.Node import NodeFunction
        from NodeView.Node import NodeBlock
        self.class_NodeFunction=NodeFunction
        self.class_NodeBlock=NodeBlock
        super().__init__(window, width=200, bg="white")
        self.parent = parent  # Store the reference to the app
        self.nodeListView : Optional[NodeListView] =None
        self.nodeDetailView :Optional[NodeDetailView] =None
        self.pack_propagate(False)

        # --- NodeTopView (NodeView 내부 위쪽, name/desc/save UI) ---
        self.node_top_view = NodeTopView(self)
        self.node_top_view.pack(fill=tk.X, padx=5, pady=5)

        # Add a canvas to draw nodes
        self.canvas = Canvas(self, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Store references to nodes
        self.nodes = {}
        self.node_num=0

        self.selected_node: Optional[NodeBlock] = None
        self.selected_nodes: dict[int, NodeBlock] = {}  # For multi-selection, key=node_id
        self.select_rect_id = None  # Rectangle ID for selection box
        self.select_start = None  # (x, y) start position for selection
        self.selected_pin: dict[str, Optional[tuple[int, NodeBlock,str]]] = {
            "input": None,
            "output": None
        }  # Track the currently selected pin
        self.offset_x = 0
        self.offset_y = 0

        # Store connections as a dict: key=(start_pin, end_pin), value=Connection
        self.connections = {}

        # Bind mouse events for node interaction
        # Bind right-click to remove connection

        # Bind mouse events for selection rectangle
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        # Bind double-click event to canvas
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)
        # Bind right-click to delete connection
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
    def on_canvas_double_click(self, event):
        # Print when double-clicking on empty canvas
        print("Canvas double-clicked at:", event.x, event.y)
        # Deselect all nodes
        for node in self.nodes.values():
            node.set_selected(False)
            if hasattr(node, 'frame'):
                node.frame.config(bg="white")
        self.selected_nodes.clear()

        nodeFuntion = self.class_NodeFunction()
        nodeFuntion.nodeDetailView=self.nodeDetailView
        # Optionally, update the UI to reflect the reset
        nodeFuntion.updateDetailUI()
        if self.nodeDetailView is not None:
            self.nodeDetailView.node = nodeFuntion

    def add_node(self, node_class, x1=50, y1=50, x2=150, y2=100):

        # Create a new Node instance with multiple input and output pins
        node = self.class_NodeBlock(self, node_class, x1, y1, x2, y2)
        self.nodes[node.node_id] = node
        # Bind click for selection (single and ctrl+multi)
        return node
    def add_nodes(self, nodes_info):
        nodes_data = nodes_info.get('nodes', [])
        connections_data = nodes_info.get('connections', [])
        nodeIdDic = {}
        # Restore nodes info and set nodeName, description, values, outputs
        for node_info in nodes_data:
            className = node_info.get('className')
            node_id = node_info.get('node_id')
            node_class = None
            if self.nodeListView is not None:
                node_class = self.nodeListView.get_node_by_classname(className)
            rectPoint = node_info.get('coords', (50, 50, 150, 100))
            node = self.add_node(node_class, *rectPoint)
            # Set nodeName, description, values, outputs if present
            node.nodeFunction.nodeName = node_info['nodeName']
            node.nodeFunction.description = node_info['description']
            node.nodeFunction.values = node_info['values']
            node.nodeFunction.outputs = node_info['outputs']
            nodeIdDic[node_id] = node.node_id
            node.nodeFunction.nodeUI()
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

        # Add to ChildNode mapping (reverse of remove_connection)
        if not hasattr(output_node, 'ChildNode'):
            output_node.ChildNode = {}
        if input_node not in output_node.ChildNode:
            output_node.ChildNode[input_node] = {}
        if output_label not in output_node.ChildNode[input_node]:
            output_node.ChildNode[input_node][output_label] = []
        if input_label not in output_node.ChildNode[input_node][output_label]:
            output_node.ChildNode[input_node][output_label].append(input_label)
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
    def remove_connection_by_line_id(self, line_id):
        # Remove connection by its line_id
        for key, connection in list(self.connections.items()):
            if connection.line_id == line_id:
                self.remove_connection(connection.input_pin)  # This will remove the line and update ChildNode
                break
    def on_pin_click(self, pin, pin_type: str, label,node):
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
            (input_pin, input_node,inputLabel) = self.selected_pin["input"]
            (output_pin, output_node,outputLabel) = self.selected_pin["output"]
            # Connect pins
            self.connect_pins(output_pin, input_pin, output_node, input_node,outputLabel,inputLabel)
            # Reset pin colors
            self.canvas.itemconfig(input_pin, fill="white")
            self.canvas.itemconfig(output_pin, fill="white")
            self.selected_pin = {"input": None, "output": None}

    def on_canvas_press(self, event):
        # Start selection rectangle
        self.select_start = (event.x, event.y)
        if self.select_rect_id is not None:
            self.canvas.delete(self.select_rect_id)
            self.select_rect_id = None

    def on_canvas_drag(self, event):
        # Draw selection rectangle
        if self.select_start:
            x0, y0 = self.select_start
            x1, y1 = event.x, event.y
            if self.select_rect_id is not None:
                self.canvas.delete(self.select_rect_id)
            self.select_rect_id = self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="blue", width=2
            )

    def on_canvas_release(self, event):
        # Select nodes within the rectangle
        if self.select_start:
            x0, y0 = self.select_start
            x1, y1 = event.x, event.y
            x_min, x_max = min(x0, x1), max(x0, x1)
            y_min, y_max = min(y0, y1), max(y0, y1)
            self.select_start = None
            if self.select_rect_id is not None:
                self.canvas.delete(self.select_rect_id)
                self.select_rect_id = None
            # Deselect all nodes first
            for node in self.nodes.values():
                node.set_selected(False)
                # Change node frame color to default (white)
                if hasattr(node, 'frame'):
                    node.frame.config(bg="white")
            self.selected_nodes.clear()
            # Select nodes inside rectangle
            for node_id, node in self.nodes.items():
                x, y, width, height = node.get_coords()
                if (x >= x_min and x + width <= x_max and
                    y >= y_min and y + height <= y_max):
                    node.set_selected(True)
                    self.selected_nodes[node_id] = node
                    # Change node frame color to blue for selected
                    node.frame.config(bg="blue")
            # If none selected, clear selected_nodes
            if not self.selected_nodes:
                self.selected_nodes = {}

    def on_canvas_right_click(self, event):
        # Detect if a connection line was right-clicked and remove it
        clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in clicked_items:
            for key, connection in list(self.connections.items()):
                if connection.line_id == item:
                    self.remove_connection_by_line_id(connection.line_id)
                    return  # Only remove one connection per click
