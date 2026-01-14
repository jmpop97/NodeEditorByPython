from NodeView.Node import BaseNode

class AddNode(BaseNode):
    def __init__(self):
        self.description = "Addition of two numbers"
        self.nodeName = "Add"
        self.values = {
            "input1": { "display": True,"value": 0,"type":"int"},
            "input2": { "display": True,"value": 0,"type":"int"},
        }
        self.outputs = {
            "output": 0,
        }

    def functions(self):
        input1 = self.values["input1"]["value"]
        input2 = self.values["input2"]["value"]
        self.outputs = {
            "output": input1 + input2,
        }
