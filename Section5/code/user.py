import sqlite3
from sqlite3.dbapi2 import Cursor
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))

        row = result.fetchone()

        if row is None:
            user = None
        else:
            user = cls(*row) # same as => cls(_id = row[0], username = row[1], password= row[2])
        
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,))

        row = result.fetchone()

        if row is None:
            user = None
        else:
            user = cls(*row) # same as => cls(_id = row[0], username = row[1], password= row[2])
        
        connection.close()
        return user

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type = str,
            required = True,
            help = "This field cannot be left empty!"
    )
    parser.add_argument('password',
            type = str,
            required = True,
            help = "This field cannot be left empty!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message' : 'A user with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query, (data['username'], data['password']))
        
        connection.commit()
        connection.close()

        return {'message' : 'User created successfully.'}, 201