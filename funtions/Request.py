from NodeView.Node import NodeFuntion
import requests

class Request(NodeFuntion):
    def __init__(self) -> None:
        self.description = "Request"
        self.nodeName = "Request"
        self.values = {
            "method": {"value": "", "display": True, "type": "text"},
            "url": {"value": "", "display": True, "type": "text"},
            "param": {"value": "", "display": True, "type": "text"},
            "headers": {"value": "", "display": True, "type": "text"},
            "data": {"value": "", "display": True, "type": "text"},
        }
        self.outputs = {
            "response": "",

        }


    def functions(self):
        method = self.values["method"]["value"].upper()
        url = self.values["url"]["value"]
        param = self.values["param"]["value"]
        headers = self.values["headers"]["value"]
        data = self.values["data"]["value"]

        # Parse headers and params if they are in JSON-like string
        import json
        try:
            headers_dict = json.loads(headers) if headers else {}
        except Exception:
            headers_dict = {}
        try:
            params_dict = json.loads(param) if param else {}
        except Exception:
            params_dict = {}
        try:
            data_dict = json.loads(data) if data else data
        except Exception:
            data_dict = data


        response = requests.request(method, url, params=params_dict, headers=headers_dict, data=data_dict)
        self.outputs = {
            "response": response.text,
        }

