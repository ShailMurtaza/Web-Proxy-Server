from flask import Flask, render_template, request, session, redirect, send_file, Response, abort
# from WebRequests import Request
import requests

app = Flask(__name__)
app.secret_key = 'key'
req_session = requests.session()

@app.route("/")
def index():
	return render_template("index.html", error=None)


@app.route('/proxy', methods=["GET", "POST"])
def proxy():
	if request.method == "POST":
		url = request.form["url"]
		if not (url.startswith("http://") or url.startswith("https://")):
			url = "http://" + url
		if not url.endswith("/"):
			url += "/"
		session["url"] = url
		return redirect(f"/website/{url}")
	return redirect("/")


@app.route("/website/<path:url>")
def url_request(url):
	url = request.full_path
	url = url[url.find("http"):]
	html_content = request_url(url)

	#  resp_headers = r.headers
	resp = Response(html_content)
	#  print(resp_headers)

	#  resp.headers = resp_headers
	# print(type(resp.headers))
	# print(f"${url}$")
	# print("########")
	# html_content = get(url).content
	# open("test.jpg", "wb").write(html_content)
	# print(html_content[:100])
	# html_content = Markup(html_content)
	# print("DONE")
	# return render_template("index.html", html_content=html_content)
	# print(type(html_content))

	return resp

@app.route("/website/<path:url>", methods=["post"])
def url_request_post(url):
	url = request.full_path
	url = url[url.find("http"):]
	html_content = request_url(url, request.form)
	resp = Response(html_content)
	return resp


@app.route("/<path:path>")
def additional_request(path):
	url = session.get("url")
	if url:
		url += request.full_path
		return redirect(f"/website/{url}")
	abort(404)


def printf(*args):
	print("#################")
	print(*args)
	print("#################")

def request_url(url, request_form=None):
	if request_form:
		req_resp = req_session.post(url, data=request_form, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"})
	else:
		req_resp = req_session.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"})
	html_content = req_resp.content.decode('utf-8', 'ignore')
	html_content = html_content.replace("=\'http://", "=\'/website/http://")
	html_content = html_content.replace("=\"http://", "=\"/website/http://")
	html_content = html_content.replace("=\'https://", "=\'/website/https://")
	html_content = html_content.replace("=\"https://", "=\"/website/https://")
	#  print(url, req_resp.url)
	#  if url != req_resp.url:
		#  return redirect("/website/" + req_resp.url)
	return html_content
    #  response = req_session.post(url, data=request_form, allow_redirects=False)
    #  assert response.status_code == 302
    #  assert 'c_user' in response.cookies
    #  return response.cookies
   
app.run(host="0.0.0.0", port=8000, debug=True)
