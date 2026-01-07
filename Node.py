class BaseNode():
    def __init__(self) -> None:
        self.description = ""
        self.nodeName=""
        self.values = {
            # "input1": {"value": 0, "display": True},
        }
        self.outputs = {
            # "output1": 0,
        }

    def funtions(self):
        pass

class Node:
    def __init__(self, canvas, node_id, Node_class:BaseNode, x1, y1, x2, y2, num_inputs=1, num_outputs=1):
        self.node=Node_class # type: ignore
        self.canvas = canvas
        self.node_id = node_id
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags=node_id)
        self.text = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.node.nodeName, tags=node_id)
        num_inputs = sum(1 for v in self.node.values.values() if v.get("display", False))
        num_outputs = sum(1 for v in self.node.outputs.values())

        # Create multiple input pins
        self.input_pins = []
        self.input_texts = []
        for i in range(num_inputs):
            pin_y = y1 + (i + 1) * (y2 - y1) // (num_inputs + 1)
            pin_x1, pin_y1 = x1 - 10, pin_y - 5
            pin_x2, pin_y2 = x1, pin_y + 5
            pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="blue")
            text = canvas.create_text(pin_x1 - 20, pin_y, anchor="e", text=f"In {i + 1}")
            self.input_pins.append(pin)
            self.input_texts.append(text)

        # Create multiple output pins
        self.output_pins = []
        self.output_texts = []
        for i in range(num_outputs):
            pin_y = y1 + (i + 1) * (y2 - y1) // (num_outputs + 1)
            pin_x1, pin_y1 = x2, pin_y - 5
            pin_x2, pin_y2 = x2 + 10, pin_y + 5
            pin = canvas.create_oval(pin_x1, pin_y1, pin_x2, pin_y2, fill="green")
            text = canvas.create_text(pin_x2 + 20, pin_y, anchor="w", text=f"Out {i + 1}")
            self.output_pins.append(pin)
            self.output_texts.append(text)

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
        for pin, text in zip(self.output_pins, self.output_texts):
            self.canvas.delete(pin)
            self.canvas.delete(text)
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
        print(f"Play button clicked for node {self.node_id}")

