from NodeView.Node import nodeFuction
import tkinter as tk
import requests
import json
from urllib.parse import urlparse, parse_qs

class BurfNode(nodeFuction):
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
        # Split request into headers and body
        try:
            header_part, post_body = request.split("\n\n", 1)
        except ValueError:
            header_part, post_body = request, ""
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

        self.outputs = {
            "method": method,
            "url": url,
            "param": param,
            "headers": headers,
            "data": "",
        }
    def outputUI(self, right_frame):
        for key, value in self.outputs.items():
            frame = tk.Frame(right_frame.bottom_section, bg="lightpink")
            frame.pack(fill=tk.X, padx=5, pady=2)
            label = tk.Label(frame, text=f"{key}:", bg="lightpink")
            label.pack(side=tk.LEFT, padx=(0,5))
            # value가 JSON 형식이면 보기 좋게 정렬
            formatted = str(value)
            try:
                parsed_json = json.loads(value)
                formatted = json.dumps(parsed_json, ensure_ascii=False, indent=2)
            except Exception:
                pass
            # 줄 수 계산 (최소 2줄)
            num_lines = max(formatted.count('\n') + 1, 2)
            text_widget = tk.Text(frame, height=num_lines, wrap="word", bg="#ffe4ec")
            text_widget.insert("1.0", formatted)
            text_widget.config(state="disabled")
            text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
            right_frame.output_labels[key] = text_widget