from email.errors import ObsoleteHeaderDefect
import deprecation
import sqlite3
import typing

#création d'un objet connection
# set the sqlite connection in "manual transaction mode"
# (by default, all execute calls are performed in their own transactions, not what we want)
def GetConnection() -> sqlite3.Connection:
    db_connection = sqlite3.connect("./database.db", check_same_thread=False)
    db_connection.isolation_level = None
    return db_connection

"""
# start transaction
cur.execute("begin")

# save the question to db
insertion_result = cur.execute(
	f"insert into Question (title) values"
	f"('{input_question.title}')")
#send the request
cur.execute("commit")
#in case of exception, roolback the transaction
cur.execute('rollback')
"""
primitive = (int, str, bool)

def is_primitive(thing):
    return isinstance(thing, primitive)

class Answer():
    def __init__(self, text: str, is_correct: bool):
        self.text = text
        self.is_correct = is_correct

class Question():
    def __init__(self, texte: str, title: str, image: str, position: int, answers: typing.List[Answer]):
        self.texte = texte
        self.title = title
        self.image = image
        self.position = position
        self.answers = answers

    def ToJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def ToSQLInsert(self):
        return f"insert into Question (texte, title, image, position) values ('{self.texte}', '{self.title}', '{self.image}', {self.position})"

    @staticmethod
    def ToSQLDelete(position: int):
        return f"delete from Question where position = {position}"
    
    @staticmethod
    def AnswerToSQLInsert(answer: Answer):
        return f"insert into Answer (text, is_correct) values ('{answer.text}', {answer.is_correct})"


def ToJson(obj: object) -> str:
    return json.dumps()

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

def AddQuestion(question):
    query: str = ToSQLInsert(question, "Question")
    with GetConnection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        
    
def DeleteQuestion(fieldValue):
    query: str = ToSQLDelete("Question", "Position", 1)
    with GetConnection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return cur.rowcount
    return 0

def GetQuestion(fieldValue):
    query: str = ToSQLGet("Question", "Position", 1)
    with GetConnection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchone()
    return None