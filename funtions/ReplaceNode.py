from NodeView.Node import BaseNode
class ReplaceNode(BaseNode):
    def __init__(self) -> None:
        self.description = "replace"
        self.nodeName="replace"
        self.values = {
            "input1": { "display": True,"value": "","type":"str"},
            "par1": { "display": False,"value": "","type":"str"},
        }
        self.outputs = {
            "output": "",
        }               

    def functions(self):
        input1 = self.values["input1"]["value"]
        par1 = self.values["par1"]["value"]
        # Replace all occurrences of par1 in input1 with an empty string
        self.outputs = {
            "output": input1.replace(par1)
        }
        
