from NodeView.Node import BaseNode
import requests

class RequestNode(BaseNode):
    def __init__(self) -> None:
        self.description = "요청"
        self.nodeName = "RequestNode"
        self.values = {
            "text": {
                "value": """GET /api/v1/players/PEACEANDCHIPS/profile HTTP/2
Host: er.dakgg.io
Sec-Ch-Ua: "Chromium";v="143", "Not A(Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: ko-KR,ko;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Connection: keep-alive

""", 
                "display": True},
            "parsed": {"value": {}, "display": False},
        }
        self.outputs = {
            "output1": "",
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

        base_url = None
        for line in lines:
            if line.lower().startswith("origin:"):
                base_url = line.split(":", 1)[1].strip()
                break
        if not base_url:
            for line in lines:
                if line.lower().startswith("referer:"):
                    ref = line.split(":", 1)[1].strip()
                    if ref.startswith("http"):
                        from urllib.parse import urlparse
                        parsed = urlparse(ref)
                        base_url = f"{parsed.scheme}://{parsed.netloc}"
                        break
        if not base_url:
            base_url = "https://www.google.com"
        url = base_url + path
        # Parse body as dict
        data = {}
        for pair in post_body.split('&'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                data[k] = v
        self.values["parsed"]["value"] = data
        # Send the request using requests.post
        try:
            response = requests.post(url, headers=headers, data=data)
            output = response.text
            print(output)
        except Exception as e:
            output = str(e)
        self.outputs = {
            "output1": output,
        }
