from flask import Flask, render_template, send_from_directory,request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace the placeholder with your Atlas connection string
uri = "mongodb://localhost:27017/test"
# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))


# Send a ping to confirm a successful connection
try:
    #client.admin.command('ping')
    #print("Pinged your deployment. You successfully connected to MongoDB!")
    # Create a database
    db = client["DB_UnSecuredLoans1"]  # Replace "mydatabase" with your desired database name
    # Create a collection within the database
    collection = db["mycollection"]  # Replace "mycollection" with your desired collection name

    User_Collection =db["users"]  # Replace with the collection name

    # User data to insert (replace with your user data)
    user_data ={
            "username": "admin",
            "password": "password",
            "roles": [{"role":"ADMIN"}]
        }


# Connect to MongoDB
    # Insert user data into the collection
    user = User_Collection.find_one({
            "username": "admin"
        })

    if user:
        print("Admin user existing")
    else:
        print("Admin user NOT existing")
        test=User_Collection.insert_one(user_data)

except Exception as e:
    print(e)

app = Flask(__name__)

# Initialize Flask-RESTPlus API
api = Api(app, version='1.0', title='Banking API', description='Banking API with Swagger documentation')

# Namespace creation
ns = api.namespace('jso', description='Banking endpoints')


# Configure JWT settings
app.config['JWT_SECRET_KEY'] = 'A#B#C@5%8'  # Secret key to sign the JWT tokens
jwt = JWTManager(app)

# Configure Flask-PyMongo
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/UnSecuredLoans'  # Change this to your MongoDB URI
#mongo = PyMongo(app)

# Define user model
role_model = api.model('role', {'role': fields.String()})
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'roles': fields.List(fields.Nested(role_model))
})

login_user_model = api.model('login_user_model', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

# Define JWT token model
token_model = api.model('Token', {
    'access_token': fields.String(description='Access Token')
})

# Define a custom user claims loader callback
# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     # Replace this with your logic to fetch user roles from your user data
#     return {"roles": user_data.get("roles", [])}

#-------------------------

# Login endpoint to obtain a JWT token
@ns.route('/login')
class UserLogin(Resource):
    @api.expect(login_user_model, validate=True)
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Replace this with your user authentication logic
        user_data = User_Collection.find_one({'username': username, 'password': password})

        if user:
            #access_token = create_access_token(identity=username)
            #access_token = create_access_token(identity=username, user_claims={'roles': user_data.get('roles', [])})
            #additional_claims=user_data.get('roles', [])
            additional_claims = {"roles": user_data.get('roles', [])}
            #print()
            access_token = create_access_token(identity=user_data["username"], additional_claims=additional_claims)
            return {'access_token': access_token}
        else:
            return {'message': 'Invalid credentials'}, 401
#------------------------------------------------------------------

# Login endpoint to obtain a JWT token
@ns.route('/createUser')
class CreateUser(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        roles = data['roles']

        # Create User Obj
        user = User_Collection.insert_one({'username': username, 'password': password, 'roles': roles})

        if user:
            return {'status': 'User Created'}
        else:
            return {'status': 'User Creation Failed'}, 401
#------------------------------------------------------------------
# Protected resource that requires a valid JWT token
@ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        #user_roles = get_jwt_claims().get('roles', [])
        jwt_dict=get_jwt()
        user_roles = jwt_dict["roles"]
        for roleObj in user_roles:
            if roleObj["role"] == "USER" or roleObj["role"] == "ANALYST" :
                return {'message': f'Access granted to {current_user}'}
            else:
                return {'message': f'Access denied to {current_user}'}


#------------------------------------------------------------------

@ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        collection.insert_one({"key": "value"})
        return "Connected to MongoDB, created database, and collection!"
        #return {'message': 'Hello, Flask-RESTPlus!'}

# Route to serve a static HTML page
@app.route('/static_page')
def static_page():
    return render_template('index.html')

# Serve the static HTML file
@app.route('/')
def serve_vue_app():
    return send_from_directory('static', 'index.html')

# API endpoint to provide data
@app.route('/api/data')
def api_data():
    # Replace this with your actual data
    data = {'message': 'Hello from Flask API'}
    return data

if __name__ == '__main__':
    #app.run(debug=True)
