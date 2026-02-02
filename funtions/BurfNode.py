from NodeView.Node import NodeFunction
import tkinter as tk
from urllib.parse import urlparse, parse_qs
class BurfNode(NodeFunction):
    def __init__(self) -> None:
        self.description = "burf suite"
        self.nodeName = "burf suite"
        self.values = {
            "text": {
                "value": """""", 
                "display": True
            },
        }
        self.outputs = {
            "method": "",
            "url": "",
            "param": "",
            "headers": "",
            "data": "",
        }


    def functions(self):
        # Parse the POST body text into a dict and store in values["parsed"]
        request = self.values["text"]["value"]
        # Split request into headers and body, handle missing post_body
        if "\n\n" in request:
            header_part, post_body = request.split("\n\n", 1)
        else:
            header_part = request
            post_body = ""
        # Parse request line and headers
        lines = header_part.split("\n")
        request_line = lines[0]
        headers = {}
        for line in lines[1:]:
            if ':' in line:
                k, v = line.split(':', 1)
                headers[k.strip()] = v.strip()
        # Parse URL and method
        try:
            method, path, _ = request_line.split()
        except ValueError:
            method, path = "POST", "/"

        # base_url을 Host 헤더에서 추출
        base_url = None
        for line in lines:
            if line.lower().startswith("host:"):
                host = line.split(":", 1)[1].strip()
                base_url = f"https://{host}"
                break
        if not base_url:
            base_url = "https://www.google.com"
        url = base_url + path

        # param 구분 (쿼리스트링)
        parsed_url = urlparse(path)
        param = parse_qs(parsed_url.query)

        # Store post_body as data

        self.outputs = {
            "method": method,
            "url": url,
            "param": param,
            "headers": headers,
            "data": post_body,
        }
    