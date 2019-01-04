from app import app
import flask
import requests
import json

POST_SERVICE_URL = "http://127.0.0.1:5001/posting"
VIEW_SERVICE_URL = "http://127.0.0.1:5003/get-one"

SEND_DATA_FMT = {"department":
			{"name": None},
		"team": {"depart_id": None,
			"name": None,
			"manager_id": None},
		"employee": {"team_id": None,
			"name": None,
			"sname": None,
			"exp": None,
			"position": None,
			"salary": None,
			"coefficient": None}}


def get_info():
	response = requests.get(VIEW_SERVICE_URL)
	return response.content


def send_info(info: dict):
	info = json.dumps(info)
	headers = {'Content-Type': 'application/json'}
	response = requests.post(POST_SERVICE_URL, data=info, headers=headers)
	if response.status_code == 200:
		return True
	else:
		return False

@app.route("/salaries", methods=['GET'])
def get_all():
    a = json.loads(get_info())
    print(type(a))
    return flask.render_template("salaries.html", a=a)




@app.route("/")
def index():
	return flask.render_template("index.html")

def	try_send(key, form):
	"""
		Function parse user input and tries to send data to POST service
	"""
	data2sent = dict(SEND_DATA_FMT)
	for i in SEND_DATA_FMT[key]:
		if i not in form:
			print(i)
			return flask.make_response(("ERROR 1", 500))
		data2sent[key][i] = form[i]
	for i in data2sent:
		if i != key:
			data2sent[i] = None
	if not send_info(data2sent):
			return flask.make_response(("ERROR 2", 500))
	return flask.make_response(("OK", 200))


@app.route("/create-department", methods=['POST'])
def create_departament():
	return try_send('department', flask.request.form)


@app.route("/create-team", methods=['POST'])
def create_team():
	return try_send('team', flask.request.form)


@app.route("/hire-employee", methods=['POST'])
def hire_employee():
	return try_send('employee', flask.request.form)
