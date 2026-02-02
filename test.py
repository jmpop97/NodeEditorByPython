# This script sends a POST request to http://127.0.0.1:5555/case1/main.php and prints the response
import requests

url = "http://127.0.0.1:5555/case1/main.php"
headers = {
	"Host": "127.0.0.1:5555",
	"Cache-Control": "max-age=0",
	"sec-ch-ua": '"Chromium";v="143", "Not A(Brand";v="24"',
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": '"Windows"',
	"Accept-Language": "ko-KR,ko;q=0.9",
	"Origin": "http://127.0.0.1:5555",
	"Content-Type": "application/x-www-form-urlencoded",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Sec-Fetch-Site": "same-origin",
	"Sec-Fetch-Mode": "navigate",
	"Sec-Fetch-User": "?1",
	"Sec-Fetch-Dest": "document",
	"Referer": "http://127.0.0.1:5555/case1/main.php",
	"Accept-Encoding": "gzip, deflate, br",
	"Cookie": "csrftoken=JLo4pvmpbPBlbFJxFSHnwoi9H8lzsWbD; PHPSESSID=e848d56efd34bb50b4e361858868b4ae",
	"Connection": "keep-alive"
}
data = "id=testid1&pwd=pwd"

response = requests.request("POST", url, headers=headers, data=data, allow_redirects=False)
	print("Status Code:", response.status_code)  # 1. 200코드
	redirect_url = response.headers.get('Location')  # 2. redirect_url
	print("Redirect Location:", redirect_url if redirect_url else "None")
	cookies = response.headers.get('Set-Cookie')  # 3. cookie
	print("Set-Cookie:", cookies if cookies else "None")
	print("Response Body:\n", response.text)  # 4. response
