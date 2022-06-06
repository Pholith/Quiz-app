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
	return {"size": model.Question.GetNumberOfQuestions(), "scores": model.Participation.GetScoreByParticipation()}, 200

	
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
	model.Question.AddQuestion(model.Question.FromJson(request.get_json()))
	return {}, 200

@app.route('/questions/<section>', methods=['DELETE'])
def DeleteQuestion(section):
	if not IsAuthorized(request):
		return {}, 401
	if not section.isdigit():
		return {}, 400
	if model.Question.DeleteQuestion(int(section)) == 0:
		return {}, 404
	model.Question.ReorderQuestions()
	return {}, 204

@app.route('/questions/<section>', methods=['GET'])
def GetQuestion(section):
	if not section.isdigit():
		return {}, 400
	question: model.Question = model.Question.GetQuestion(section)
	if question is None:
		return {}, 404
	return question.ToJson(), 200

@app.route('/questions/<section>', methods=['PUT'])
def UpdateQuestion(section):
	if not IsAuthorized(request):
		return {}, 401
	if not section.isdigit():
		return {}, 400
	question: model.Question = model.Question.GetQuestion(section)
	if question is None:
		return {}, 404
	question.text = request.get_json()['text']
	question.title = request.get_json()['title']
	question.image = request.get_json()['image']
	question.position = request.get_json()['position']
	question.possibleAnswers = model.Answer.MultipleFromJson(request.get_json()['possibleAnswers'])
	model.Question.DeleteQuestion(section)
	model.Question.ReorderQuestions()
	model.Question.AddQuestion(question)
	model.Question.ReorderQuestions()
	return {}, 200

@app.route('/participations', methods=['POST'])
def AddParticipation():
	payload = request.get_json()
	participation: model.Participation = model.Participation.FromJson(payload)
	if model.Question.GetNumberOfQuestions() > len(participation.answers) or len(participation.answers) > model.Question.GetNumberOfQuestions():
		return {}, 400
	model.Participation.AddParticipation(model.Participation.FromJson(payload))
	return {"playerName": participation.playerName, "score": participation.GetScore()}, 200

@app.route('/participations', methods=['DELETE'])
def DeleteParticipation():
	model.Participation.DeleteParticipations()
	return {}, 204

if __name__ == "__main__":
    app.run()
	