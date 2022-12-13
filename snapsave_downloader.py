from requests import get,post
# pip install headerz
# https://pypi.org/project/headerz/
from headerz import Headerz
import re
import html



def SnapSave(facebook_video_url):
	head = Headerz()
	headraw = """
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: text/html
accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: max-age=0
content-length: 64
content-type: application/x-www-form-urlencoded
cookie: _ga=GA1.2.1509060997.165677849; __gads=ID=14bf8adad89d006c-2262a93930d500d1:T=1657716831:RT=1657716831:S=ALNI_Ma89sSwxwGFETAXf0SaugcMNkWP4Q; __atssc=google;13; __gpi=UID=000007abf8eb7d95:T=1657716831:RT=1668338163:S=ALNI_MbquR5QL9MufCzkyUL_ouvJAzWFkA; __atuvc=0|43,10|44,0|45,1|46,1|47
origin: https://snapsave.app
referer: https://snapsave.app/
sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: iframe
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
"""

	snapsave_url = "https://snapsave.app/action.php"
	header = head.header_builder(headraw)
	post_data = {"url":facebook_video_url}

	# snapsave server return encoded javascript code
	raw_result_contain_js = post(snapsave_url,data=post_data,headers=header).text
	try:
		the_js_result = re.search(r"javascript\">(.*?)<\/script>",raw_result_contain_js).group(1)
	except:
		the_js_result = raw_result_contain_js

	try:
		# translate the encoded javascript code to readable code using https://onecompiler.com/javascript/
		translated_js = JSRunner(the_js_result)

		# then get download url (higher quality video)
		url_result = re.search(r"href=\\\\\\\"(http.*?)\\\\\\\"",translated_js).group(1)

		return url_result
	except:
		return None

def JSRunner(js_string):
	# get token from https://onecompiler.com/javascript/
	token = get("https://onecompiler.com/api/getIdAndToken").json()
	# result is
	# {"id":"xxxx","token":"xxxxxxx"}

	TOKEN_TITLE = token["id"]
	TOKEN = token["token"]
	JS_CONTENT = js_string.replace('"','\"')+";"
	js_translate_data = {"name":"JavaScript","title":TOKEN_TITLE,"version":"ES6","mode":"javascript","description":None,"extension":"js","languageType":"programming","active":True,"properties":{"language":"javascript","docs":True,"tutorials":True,"cheatsheets":True,"filesEditable":True,"filesDeletable":True,"files":[{"name":"index.js","content":JS_CONTENT}],"newFileOptions":[{"helpText":"New JS file","name":"script${i}.js","content":"/**\n *  In main file\n *  let script${i} = require('./script${i}');\n *  console.log(script${i}.sum(1, 2));\n */\n\nfunction sum(a, b) {\n    return a + b;\n}\n\nmodule.exports = { sum };"},{"helpText":"Add Dependencies","name":"package.json","content":"{\n  \"name\": \"main_app\",\n  \"version\": \"1.0.0\",\n  \"description\": \"\",\n  \"main\": \"HelloWorld.js\",\n  \"dependencies\": {\n    \"lodash\": \"^4.17.21\"\n  }\n}"}]},"_id":TOKEN_TITLE,"user":None,"idToken":TOKEN,"visibility":"public"}

	# post js data to js translator sever
	translated_js_from_js_runner = post("https://onecompiler.com/api/code/exec",json=js_translate_data).text
	return translated_js_from_js_runner


if __name__=="__main__":
	facebook_video_url = input("Facebook url: ")
	print("Processing your url..")
	download_url = SnapSave(facebook_video_url)
	print("Your download url:",download_url)
