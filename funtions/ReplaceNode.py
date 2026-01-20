from NodeView.Node import nodeFuction
class ReplaceNode(nodeFuction):
    def __init__(self,node) -> None:
        self.description = "replace"
        self.nodeName="replace"
        self.values = {
            "input": { "display": True,"value": "","type":"text"},
            "before": { "display": False,"value": "","type":"str"},
            "after": { "display": False,"value": "","type":"str"},
        }
        self.outputs = {
            "output": "",
        }               
        self.nodeUI=node
    def functions(self):
        input = self.values["input"]["value"]
        before = self.values["before"]["value"]
        after = self.values["after"]["value"]
        # Replace all occurrences of par1 in input1 with an empty string
        self.outputs = {
            "output": input.replace(before,after)
        }
        
