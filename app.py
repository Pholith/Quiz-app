from flask import Flask, request
from typing import *
import jwt_utils
import model

app = Flask(__name__)


def IsAuthorized(request) -> bool:
	token = request.headers.get('Authorization')
	if token is None:
		return False
	try:
		token = token.replace('Bearer ', '')
		jwt_utils.decode_token(token)
		return True
	except:
		return False


@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

	
@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()
	if (payload['password'] == 'admin'):
		return {"token": jwt_utils.build_token()}, 200
	return {}, 401

	
@app.route('/questions', methods=['POST'])
def AddQuestion():
	if not IsAuthorized(request):
		return {}, 401
	payload = request.get_json()
	model.AddQuestion(request.get_json())
	return {}, 200

	
if __name__ == "__main__":
    app.run(ssl_context='adhoc')