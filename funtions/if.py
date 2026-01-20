from NodeView.Node import nodeFuction
class TestNode(nodeFuction):
    def __init__(self,node) -> None:
        self.description = "test"
        self.nodeName="test"
        self.values = {
            "input1": { "display": True,"value": 1,"type":"int"},
        }
        self.outputs = {
            "output1": 1,
            "output2": 2,
        }
        self.nodeUI=node

    def functions(self):
        input1 = self.values["input1"]["value"]
        input2 = self.values["input2"]["value"]
        if input1 == 1:
            self.outputs = {
            }
            return ["output1"]
        if input2 ==0:
            self.outputs = {
            }
            return ["output2"]
            