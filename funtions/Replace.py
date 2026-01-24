from NodeView.Node import NodeFuntion
import requests

class Replace(NodeFuntion):
    def __init__(self) -> None:
        self.description = "Replace"
        self.nodeName = "Replace"
        self.values = {
            "text": {"value": "", "display": True, "type": "text"},
            "before": {"value": "", "display": False, "type": "text"},
            "after": {"value": "", "display": False, "type": "text"},

        }
        self.outputs = {
            "result": "",
        }


    def functions(self):
        text = self.values["text"]["value"]
        before = self.values["before"]["value"]
        after = self.values["after"]["value"]
        result = text.replace(before, after)
        self.outputs = {
            "result": result,
        }

