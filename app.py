from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from flask_heroku import Heroku
# from flask_cors import CORS
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,"app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)
# heroku = Heroku(app)
# CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)


class Workout(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    muscle_group = db.Column(db.String, nullable=False)
    equiptment = db.Column(db.String, nullable=False)
    
    def __init__(self, muscle_group, equiptment):
        self.muscle_group = muscle_group
        self.equiptment = equiptment

class WorkoutSchema(ma.Schema):
    class Meta:
        fields = ("id", "muscle_group", "equiptment")

workout_schema = WorkoutSchema()
multiple_workout_schema = WorkoutSchema(many=True)

# User Endpoints

@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON.")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

# possible duplication error code to go here

    record = User(username, password)
    db.session.add(record)
    db.session.commit()

    return jsonify("User Added")



if __name__ == "__main__":
    app.run(debug=True)