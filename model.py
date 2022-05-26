import json
import sqlite3
import typing
#création d'un objet connection
db_connection = sqlite3.connect("./database.db")
# set the sqlite connection in "manual transaction mode"
# (by default, all execute calls are performed in their own transactions, not what we want)
db_connection.isolation_level = None

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

class Question():
    def init(self, title: str):
        self.title = title
    
def ToJson(obj: object) -> str:
    return json.dump(obj)

def ToObject(json_str: str) -> object:
    return json.loads(json_str)
    
def ToSQL(obj: object, objName: str) -> str:
    query: str = f"INSERT INTO {objName} VALUES ("
    for field in obj:
        if is_primitive(obj[field]): continue
        query += str(obj[field]) + ", "
    query = query[:-2] + ")"
    return query

def AddQuestion(question):
    query: str = ToSQL(question, "Question")
    cur = db_connection.cursor()
    cur.execute()
    

