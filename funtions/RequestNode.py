from NodeView.Node import BaseNode
import tkinter as tk
import requests
import json

class RequestNode(BaseNode):
    def __init__(self) -> None:
        self.description = "request"
        self.nodeName = "Request"
        self.values = {
            "method": {
                "value": "",
                "display": True,
                "type": "text"
            },
            "url": {
                "value": "",
                "display": True,
                "type": "text"
            },
            "headers": {
                "value": "",
                "display": True,
                "type": "text"
            },
            "data": {
                "value": "",
                "display": True,
                "type": "text"
            },
        }
        self.outputs = {
            "response": "",
        }

    def functions(self):
        try:
            method = self.values.get("method", {}).get("value", "GET")
            url = self.values.get("url", {}).get("value", "")
            headers = self.values.get("headers", {}).get("value", "")
            data = self.values.get("data", {}).get("value", "")
            # headers가 문자열이면 dict로 변환 시도
            if isinstance(headers, str) and headers.strip():
                try:
                    headers = json.loads(headers)
                except Exception:
                    headers = {}
            if not isinstance(headers, dict):
                headers = {}
            response = requests.request(method.upper(), url, headers=headers, data=data)
            output = response.text
            print(output)
        except Exception as e:
            output = str(e)
        self.outputs = {
            "output1": output,
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