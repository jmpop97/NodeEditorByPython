from NodeView.Node import nodeFuction
import tkinter as tk
import requests
import json

class RequestNode(nodeFuction):
    def __init__(self,node) -> None:
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
        self.nodeUI=node

    def functions(self):
        try:
            import urllib.parse
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

            # URL에서 쿼리 파라미터 파싱
            parsed_url = urllib.parse.urlparse(url)
            base_url = urllib.parse.urlunparse(parsed_url._replace(query=""))
            params = urllib.parse.parse_qs(parsed_url.query)
            # parse_qs는 값이 리스트로 반환되므로, 단일 값이면 값만 추출
            params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}

            response = requests.request(method.upper(), base_url, headers=headers, data=data, params=params if params else None)
            output = response.text
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