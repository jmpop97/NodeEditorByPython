from NodeView.Node import NodeFunction
import requests
import json
from urllib.parse import urljoin

class Request(NodeFunction):
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
            "cookie": "",
            "redirect_url": "",
            "status_code": 0,
        }


    def functions(self):
        method = self.values["method"]["value"].upper()
        url = self.values["url"]["value"]
        param = self.values["param"]["value"]
        headers = self.values["headers"]["value"]
        data = self.values["data"]["value"]

        # URL이 https로 시작하고, 127.0.0.1 또는 localhost면 http로 자동 변환
        if url.startswith("https://127.0.0.1") or url.startswith("https://localhost"):
            url = url.replace("https://", "http://", 1)

        # Parse headers and params if they are in JSON-like string
        try:
            print(type(headers))
            headers_dict = json.loads(headers)
        except Exception:
            headers_dict = headers
        try:
            params_dict = json.loads(param) if param else {}
        except Exception:
            params_dict = {}
        try:
            data_dict = json.loads(data) if data else data
        except Exception:
            data_dict = data

        try:
            response = requests.request(method, url, params=params_dict, headers=headers_dict, data=data_dict, allow_redirects=False, verify=False)
        except requests.exceptions.SSLError:
            # Retry with HTTP if HTTPS fails
            if url.startswith("https://"):
                url = url.replace("https://", "http://", 1)
            response = requests.request(method, url, params=params_dict, headers=headers_dict, data=data_dict, allow_redirects=False, verify=False)
        
        # Extract cookies as a dictionary
        cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
        # Extract redirect URL if present
        redirect_url = response.headers.get('Location', '')
        self.outputs = {
            "response": response.text,
            "cookie": cookie_dict,
            "redirect_url": redirect_url,
            "status_code": response.status_code,
        }


