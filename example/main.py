import flask_restful
from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb://test_user_admin:123456@localhost:27017/admin"
}
MongoEngine(app)
api = flask_restful.Api(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
