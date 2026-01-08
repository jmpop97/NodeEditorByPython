from NodeView.Node import BaseNode
class TestNode(BaseNode):
    def __init__(self) -> None:
        self.description = "test"
        self.nodeName="test"
        self.values = {
            "input1": {"value": 1, "display": True},
            "input2": {"value": 2, "display": True},
            "input3": {"value": 3, "display": True},
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
