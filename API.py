from flask import Flask, request as req
from snapsave_downloader import SnapSave
import os


app = Flask(__name__)

@app.route("/",methods=["GET"])
def index():
	try:
		data = req.args
		facebook_video_url = data["url"]
		result = SnapSave(facebook_video_url)
		if result:
			ret_data = {"success":True,"result":result,"message":"Unofficial SnapSave API by Karjok Pangesty"}
		else:
			ret_data = {"success":False,"result":None,"message":"Invalid URL or video is private"}
	except:
		ret_data = {"success":False,"result":None,"message":"URL params required"}
	return ret_data
if __name__=="__main__":
	app.run(host="0.0.0.0",port=os.environ.get("PORT"),debug=True)
