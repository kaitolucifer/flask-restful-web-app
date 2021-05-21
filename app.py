from werkzeug.utils import import_string
from flask import Flask, jsonify
from flask_restful import Api

from db import db
from resources.user import User, Signup, Close


app = Flask(__name__)
api = Api(app)
cfg = import_string('app_config.DevelopmentConfig')()
app.config.from_object(cfg)

db.init_app(app)

api.add_resource(User, '/users/<string:user_id>')
api.add_resource(Signup, '/signup')
api.add_resource(Close, '/close')


@app.before_first_request
def create_table():
    db.create_all()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
