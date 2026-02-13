# This script sends a POST request to http://pentest.segfaulthub.com:7777/actions/login_user.php and prints the response
import requests

url = "http://pentest.segfaulthub.com:7777/actions/login_user.php"
headers = {
	"Host": "pentest.segfaulthub.com:7777",
	"Cache-Control": "max-age=0",
	"Accept-Language": "ko-KR,ko;q=0.9",
	"Origin": "http://pentest.segfaulthub.com:7777",
	"Content-Type": "application/x-www-form-urlencoded",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Referer": "http://pentest.segfaulthub.com:7777/login.php",
	"Accept-Encoding": "gzip, deflate, br",
	"Cookie": "PHPSESSID=72b89408da0247d164d06acd68b5729c",
	"Connection": "keep-alive"
}
data = "username=testid1&password=testpwd1"

response = requests.request("POST", url, headers=headers, data=data, allow_redirects=False)
print("Status Code:", response.status_code)  # 1. 200코드
redirect_url = response.headers.get('Location')  # 2. redirect_url
print("Redirect Location:", redirect_url if redirect_url else "None")
cookies = response.headers.get('Set-Cookie')  # 3. cookie
print("Set-Cookie:", cookies if cookies else "None")
print("Response Body:\n", response.text)  # 4. response
