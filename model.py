from email.errors import ObsoleteHeaderDefect
import json
import deprecation
import sqlite3
import typing
from typing import List


#création d'un objet connection
# set the sqlite connection in "manual transaction mode"
# (by default, all execute calls are performed in their own transactions, not what we want)
def GetConnection() -> sqlite3.Connection:
    db_connection = sqlite3.connect("./database.db", check_same_thread=False)
    db_connection.isolation_level = None
    return db_connection


primitive = (int, str, bool)
def is_primitive(thing):
    return isinstance(thing, primitive)

class Participation():
    def __init__(self, playerName: str, answers: List[int]):
        self.playerName = playerName
        self.answers = answers

    
    def GetScore(self) -> int:
        score: int = 0
        for i in range(len(self.answers)):
            questionI: Question = Question.GetQuestion(i+1)
            if questionI is None:
                print("Error: question " + str(i+1) + " not found")
                continue
            if questionI.possibleAnswers[self.answers[i]-1].isCorrect == 1:
                score += 1
        return score

    @staticmethod
    def FromJson(json: dict):
        return Participation(json['playerName'], json['answers'])

    def AddParticipation(self):
        db_connection = GetConnection()
        db_connection.execute("INSERT INTO participation (playerName, answers) VALUES (?, ?)", (self.playerName, json.dumps(self.answers)))
        db_connection.commit()
        db_connection.close()
    
    @staticmethod
    def GetParticipation(id: int):
        db_connection = GetConnection()
        cursor = db_connection.execute("SELECT * FROM participation WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Participation(row[0], row[1], json.loads(row[2]))

    @staticmethod
    def GetParticipations():
        db_connection = GetConnection()
        cursor = db_connection.execute("SELECT * FROM participation")
        rows = cursor.fetchall()
        participations: List[Participation] = []
        for row in rows:
            participations.append(Participation(row[0], json.loads(row[1])))
        return participations

    @staticmethod
    def GetScoreByParticipation():
        result = []
        participations: List[Participation] = Participation.GetParticipations()
        for participation in participations:
            result.append({"playerName": participation.playerName ,"score": participation.GetScore()})
        return result

    @staticmethod
    def DeleteParticipations():
        db_connection = GetConnection()
        db_connection.execute("DELETE FROM participation")
        db_connection.commit()
        db_connection.close()


class Answer():
    def __init__(self, text: str, isCorrect: bool):
        self.text = text
        self.isCorrect = isCorrect

    @staticmethod
    def AddAnswer(text: str, isCorrect: bool, questionPosition: int):
        connection = GetConnection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO answer (text, isCorrect, questionPosition) VALUES (?, ?, ?)", (text, isCorrect, questionPosition))
        connection.commit()
        cursor.close()  
        connection.close()

    @staticmethod
    def FromJson(json: str):
        return Answer(**json)

    @staticmethod
    def MultipleFromJson(json: str):
        return [Answer.FromJson(answer) for answer in json]

    @staticmethod
    def DeleteAnswer(questionPosition: int):
        connection = GetConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM answer WHERE questionPosition = ?", (questionPosition,))
        connection.commit()
        cursor.close()
        connection.close()

class Question():
    def __init__(self, text: str, title: str, image: str, position: int, answers: List[Answer]):
        self.text = text
        self.title = title
        self.image = image
        self.position = position
        self.possibleAnswers = answers

    def ToJson(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)

    @staticmethod
    def FromJson(json: str):
        possibleAnswers: List[Answer] = []
        for (element) in json["possibleAnswers"]:
            possibleAnswers.append(Answer.FromJson(element))

        return Question(json["text"], json["title"], json["image"], json["position"], possibleAnswers)
            
    @staticmethod
    def GetNumberOfQuestions():
        connection = GetConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Question")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0]

    @staticmethod   
    def AddQuestion(question):
        connection = GetConnection()
        cursor = connection.cursor()

        previousQuestion: Question = Question.GetQuestion(question.position)
        if previousQuestion is not None:
            Question.DeleteQuestion(question.position)
            previousQuestion.position += 1 #Question.GetNextPosition()
            Question.AddQuestion(previousQuestion)

        cursor.execute(f"insert or replace into Question (text, title, image, position) values (\"{question.text}\", \"{question.title}\", '{question.image}', {question.position})")
        for answer in question.possibleAnswers:
            Answer.AddAnswer(answer.text, answer.isCorrect, question.position)
        
        connection.commit()
        connection.close()

    @staticmethod
    def GetQuestion(position: int):
        db_connection = GetConnection()
        cursor = db_connection.cursor()
        cursor.execute(f"select * from Question where position = {position}")
        question: Question = cursor.fetchone()
        if question is None: return None
        cursor.execute(f"select * from Answer where questionPosition = {position} order by id")
        answers = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return Question(question[1], question[2], question[3], question[4], [Answer(answer[1], answer[2] == 1) for answer in answers])

    @staticmethod
    def DeleteQuestion(position: int):
        db_connection = GetConnection()
        cursor = db_connection.cursor()
        cursor.execute(f"delete from Question where position = {position}")
        Answer.DeleteAnswer(position)
        cursor.close()
        return cursor.rowcount > 0

    @staticmethod
    def ReorderQuestions():
        db_connection = GetConnection()
        cursor = db_connection.cursor()
        # fill every position with the next question
        cursor.execute("select * from Question order by position")
        questions = cursor.fetchall()
        for i in range(len(questions)):
            cursor.execute(f"update Question set position = {i+1} where position = {questions[i][4]}")
            cursor.execute(f"update Answer set questionPosition = {i+1} where questionPosition = {questions[i][4]}")
        db_connection.commit()
        cursor.close()
        db_connection.close()


def ToJson(obj: object) -> str:
    return json.dumps(obj)
