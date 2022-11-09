import flask_restful
from flask import Flask
from flask_mongoengine import MongoEngine

from views import DemoUserAPI

# init app
app = Flask(__name__)

# init db
app.config["MONGODB_SETTINGS"] = {
    # "host": "mongodb://test_user_admin:123456@localhost:27017/admin"
    "host": "mongodb+srv://test_admin_user:nOiPyfHBJDwxYX5K@cluster0.3an3klk.mongodb.net/?retryWrites=true&w=majority"
}
MongoEngine(app)

# load api
api = flask_restful.Api(app)
api.add_resource(DemoUserAPI, "/user/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
