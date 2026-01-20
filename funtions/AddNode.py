from NodeView.Node import nodeFuction

class AddNode(nodeFuction):
    def __init__(self,node):
        self.description = "Addition of two numbers"
        self.nodeName = "Add"
        self.values = {
            "input1": { "display": True,"value": 0,"type":"int"},
            "input2": { "display": True,"value": 0,"type":"int"},
        }
        self.outputs = {
            "output": 0,
        }
        self.nodeUI=node

    def functions(self):
        input1 = self.values["input1"]["value"]
        input2 = self.values["input2"]["value"]
        self.outputs = {
            "output": input1 + input2,
        }
