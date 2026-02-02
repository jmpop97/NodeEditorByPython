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

        response = requests.request(method, url, params=params_dict, headers=headers_dict, data=data_dict, allow_redirects=False)
        # Print HTTP response in raw format
        status_line = f"HTTP/1.1 {response.status_code} {response.reason}"
        headers = '\n'.join(f"{k}: {v}" for k, v in response.headers.items())
        # Extract cookies as a dictionary
        cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
        # Extract redirect URL if present and make it a full URL
        redirect_url = response.headers.get('Location', '')
        if redirect_url and not redirect_url.lower().startswith(('http://', 'https://')):
            redirect_url = urljoin(url, redirect_url)
        self.outputs = {
            "response": response.text,
            "cookie": cookie_dict,
            "redirect_url": redirect_url,
            "status_code": response.status_code,
        }


