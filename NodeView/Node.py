from typing import Optional

class BaseNode:
    def __init__(self) -> None:
        self.description = ""
        self.nodeName = ""
        self.values = {
            # "input1": {"value": 0, "display": True},
        }
        self.outputs = {
            # "output1": 0,
        }
        self.nodeUI: Optional[Node] = None

    def functions(self):
        pass


class Node:
    def __init__(self, canvas, node_id, Node_class: BaseNode, x1, y1, x2, y2, num_inputs=1, num_outputs=1):
        self.node = Node_class
        Node_class.nodeUI = self
        self.canvas = canvas
        self.node_id = node_id
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags=node_id)
        self.text = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.node.nodeName, tags=node_id)
        self.inputKeys = [k for k, v in self.node.values.items() if v.get("display", False)]
        self.outputKeys = [k for k, v in self.node.outputs.items()]

        # Create multiple input pins
        self.input_pins, self.input_texts = self.create_pins(
            canvas, x1, y1, y2, pin_type="input", pin_labels=self.inputKeys
        )

        # Create multiple output pins
        self.output_pins, self.output_texts = self.create_pins(
            canvas, x2, y1, y2, pin_type="output", pin_labels=self.outputKeys
        )

        # Delete button
        self.delete_button = canvas.create_rectangle(x2 - 15, y1, x2, y1 + 15, fill="red", tags=node_id)
        self.delete_text = canvas.create_text(x2 - 7, y1 + 7, text="X", fill="white", tags=node_id)
        canvas.tag_bind(self.delete_button, "<Button-1>", self.on_delete)
        canvas.tag_bind(self.delete_text, "<Button-1>", self.on_delete)

        # Play button
        self.play_button = canvas.create_rectangle(x2 - 30, y1, x2 - 15, y1 + 15, fill="green", tags=node_id)
        self.play_text = canvas.create_text(x2 - 22, y1 + 7, text="▶", fill="white", tags=node_id)
        canvas.tag_bind(self.play_button, "<Button-1>", self.on_play)
        canvas.tag_bind(self.play_text, "<Button-1>", self.on_play)


    def move(self, dx, dy):
        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.text, dx, dy)
        for pin, text in zip(self.input_pins, self.input_texts):
            self.canvas.move(pin, dx, dy)
            self.canvas.move(text, dx, dy)
        for pin, text in zip(self.output_pins, self.output_texts):
            self.canvas.move(pin, dx, dy)
            self.canvas.move(text, dx, dy)
        # Move the delete button and its text
        self.canvas.move(self.delete_button, dx, dy)
        self.canvas.move(self.delete_text, dx, dy)
        # Move the play button and its text
        self.canvas.move(self.play_button, dx, dy)
        self.canvas.move(self.play_text, dx, dy)

        # Update connected lines
        for connection in self.canvas.master.connections:
            start_pin, end_pin, line_id = connection
            if start_pin in self.input_pins + self.output_pins or end_pin in self.input_pins + self.output_pins:
                start_coords = self.canvas.coords(start_pin)
                end_coords = self.canvas.coords(end_pin)
                self.canvas.coords(
                    line_id,
                    (start_coords[0] + start_coords[2]) // 2,
                    (start_coords[1] + start_coords[3]) // 2,
                    (end_coords[0] + end_coords[2]) // 2,
                    (end_coords[1] + end_coords[3]) // 2
                )

    def get_coords(self):
        return self.canvas.coords(self.rect)

    def is_inside(self, x, y):
        coords = self.get_coords()
        return coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]

    def on_delete(self, event):
        # Remove all associated canvas items
        self.canvas.delete(self.rect)
        self.canvas.delete(self.text)
        for pin, text in zip(self.input_pins, self.input_texts):
            self.canvas.delete(pin)
            self.canvas.delete(text)
            self.canvas.master.remove_connection(pin)  # Remove connections for input pins
        for pin, text in zip(self.output_pins, self.output_texts):
            self.canvas.delete(pin)
            self.canvas.delete(text)
            self.canvas.master.remove_connection(pin)  # Remove connections for output pins
        self.canvas.delete(self.delete_button)
        self.canvas.delete(self.delete_text)
        # Remove the play button and its text
        self.canvas.delete(self.play_button)
        self.canvas.delete(self.play_text)
        # Remove the node from the center frame's node dictionary
        for node_id, node in self.canvas.master.nodes.items():
            if node == self:
                del self.canvas.master.nodes[node_id]
                break
        # Update RightFrame with a new BaseNode instance
        self.canvas.master.parent.right_frame.update_node_details(BaseNode())

    def on_play(self, event):
        try:
            self.node.functions()
        except Exception as e:
            print(f"Error executing funtions for node {self.node_id}: {e}")

    def create_pins(self, canvas, x, y1, y2, pin_labels, pin_type):
        pins = []
        texts = []
        num_pins = len(pin_labels)  # Determine the number of pins from the length of pin_labels
        for i, label in enumerate(pin_labels):
            pin_y = y1 + (i + 1) * (y2 - y1) // (num_pins + 1)
            if pin_type == "input":
                pin_x1, pin_y1 = x - 10, pin_y - 5
                pin_x2, pin_y2 = x, pin_y + 5
                pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="blue")
                text = canvas.create_text(pin_x1 - 20, pin_y, anchor="e", text=label)
                canvas.tag_bind(pin, "<Button-1>", lambda event, pin=pin: self.on_pin_click(pin, pin_type))
            elif pin_type == "output":
                pin_x1, pin_y1 = x, pin_y - 5
                pin_x2, pin_y2 = x + 10, pin_y + 5
                pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="green")
                text = canvas.create_text(pin_x2 + 20, pin_y, anchor="w", text=label)
                canvas.tag_bind(pin, "<Button-1>", lambda event, pin=pin: self.on_pin_click(pin, pin_type))
            pins.append(pin)
            texts.append(text)
        return pins, texts
    def on_pin_click(self, pin, pin_type):
        # Delegate the pin click handling to the CenterFrame
        self.canvas.master.on_pin_click(pin)

    def on_input_pin_click(self, pin_label, node):
        print(f"Input pin '{pin_label}' clicked (Node: {node.nodeName})")

    def on_output_pin_click(self, pin_label, node):
        print(f"Output pin '{pin_label}' clicked (Node: {node.nodeName})")
