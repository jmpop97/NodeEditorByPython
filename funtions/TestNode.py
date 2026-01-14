from NodeView.Node import BaseNode
class TestNode(BaseNode):
    def __init__(self) -> None:
        self.description = "test"
        self.nodeName="test"
        self.values = {
            "input1": { "display": True,"value": 1,"type":"int"},
            "input2": { "display": True,"value": 2,"type":"int"},
            "input3": { "display": True,"value": 3,"type":"int"},
        }
        self.outputs = {
            "output1": 1,
            "output2": 2,
        }

    def functions(self):
        input1 = self.values["input1"]["value"]
        input2 = self.values["input2"]["value"]
        input3 = self.values["input3"]["value"]
        self.outputs = {
            "output1": input1 + input2 + input3,
            "output2": input1 * input2 * input3,
        }
