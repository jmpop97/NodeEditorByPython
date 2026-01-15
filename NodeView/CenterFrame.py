import tkinter as tk
from tkinter import Canvas
from NodeView.Node import Node
from typing import Optional

class Connection:
    def __init__(self, output_pin, input_pin, output_node, input_node,output_label,input_label, line_id):
        self.input_node = input_node
        self.output_label = output_label
        self.input_pin = input_pin
        self.output_node = output_node
        self.input_label = input_label
        self.output_pin = output_pin
        self.line_id = line_id


class CenterFrame(tk.Frame):
    def __init__(self, parent, app):  # Pass app as parent
        super().__init__(parent, width=200, bg="white")
        self.parent = app  # Store the reference to the app
        self.pack_propagate(False)

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

    def add_node(self, node_class, num_inputs=1, num_outputs=1):
        # Create a new Node instance with multiple input and output pins
        x1, y1, x2, y2 = 50, 50, 150, 100
        node = Node(self, node_class(), x1, y1, x2, y2, num_inputs, num_outputs)
        self.nodes[node.node_id] = node

    def connect_pins(self, output_pin, input_pin, output_node, input_node, output_label, input_label):
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
        # Store with key sorted by id for uniqueness
        key = tuple(sorted([input_pin, output_pin], key=id))
        self.connections[key] = Connection(output_pin, input_pin, output_node, input_node, output_label, input_label, line_id)
        # Update ChildNode mapping for output_node
        if output_node is not None:
            if not hasattr(output_node, 'ChildNode'):
                output_node.ChildNode = {}
            if input_node not in output_node.ChildNode:
                output_node.ChildNode[input_node] = {}
            # output_label을 리스트로 관리
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
