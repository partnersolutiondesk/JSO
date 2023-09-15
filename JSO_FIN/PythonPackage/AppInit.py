from flask import Flask, render_template, send_from_directory,request
from flask_restx import Api, Resource, fields

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb://localhost:27017/test"

client = MongoClient(uri, server_api=ServerApi('1'))
try:
    # Create a database
    db = client["DB_UnSecuredLoans1"]
    # Create a collection within the database
    collection = db["mycollection"]
    User_Collection =db["users"]
    user_data ={
            "username": "admin",
            "password": "password",
            "roles": [{"role":"ADMIN"}]
        }
    user = User_Collection.find_one({"username": "admin"})
    if user:
        print("Admin user existing")
    else:
        print("Admin user NOT existing")
        test=User_Collection.insert_one(user_data)

except Exception as e:
    print(e)

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

# Define your custom Flask class (if necessary)
class CustomFlask1(Flask):
    pass

#app = CustomFlask(__name__)  # This replaces your existing "app = Flask(__name__)"

app = Flask(__name__)
# Initialize Flask-RESTPlus API
api = Api(app, version='1.0', title='Banking API', description='Banking API with Swagger documentation')

# Namespace creation
ns = api.namespace('jso', description='Banking endpoints')



