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
    def AddQuestion(question):
        connection = GetConnection()
        cursor = connection.cursor()
        Question.DeleteQuestion(question.position)
        cursor.execute(f"insert or replace into Question (text, title, image, position) values (\"{question.text}\", \"{question.title}\", '{question.image}', {question.position})")
        for answer in question.possibleAnswers:
            Answer.AddAnswer(answer.text, answer.isCorrect, question.position)
        connection.commit()
        connection.close()

    @staticmethod
    def GetQuestion(position: int) :
        db_connection = GetConnection()
        cursor = db_connection.cursor()
        cursor.execute(f"select * from Question where position = {position}")
        question: Question = cursor.fetchone()
        if question is None: return None
        cursor.execute(f"select * from Answer where questionPosition = {position}")
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



def ToJson(obj: object) -> str:
    return json.dumps(obj)



@deprecation.deprecated()
def ToObject(json_str: str) -> object:
    return json.loads(json_str)

@deprecation.deprecated()
def ToSQLInsert(obj: object, objName: str) -> str:
    query: str = f"INSERT OR IGNORE INTO {objName} VALUES (Null, "
    for field in obj:
        if not is_primitive(obj[field]): continue
        fieldText: str = str(obj[field])
        if type(obj[field]) == str: fieldText = "\"" + fieldText + "\"" 
        query += fieldText + ", "
    query = query[:-2] + ")"
    return query

@deprecation.deprecated()
def ToSQLDelete(objTable: str, fieldNam: str, fieldValue: str) -> str:
    query: str = f"DELETE FROM {objTable} WHERE {fieldNam} = {fieldValue}"
    return query

@deprecation.deprecated()
def ToSQLGet(objTable: str, fieldNam: str, fieldValue: str) -> str:
    query: str = f"SELECT * FROM {objTable} WHERE {fieldNam} = {fieldValue}"
    return query