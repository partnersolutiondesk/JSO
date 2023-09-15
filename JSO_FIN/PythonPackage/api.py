from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from .AppInit import app, api, fields, Resource, ns, request, client, User_Collection, db, render_template
from .Models import login_user_model, user_model, customer_model
from .Libs.DataSimulation import generate_fake_customer, generate_OTP
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from bson.int64 import Int64
#-------------------------


# Configure JWT settings
app.config['JWT_SECRET_KEY'] = 'A#B#C@5%8'  # Secret key to sign the JWT tokens
jwt = JWTManager(app)

# db = client["DB_UnSecuredLoans1"]  # Replace "mydatabase" with your desired database name
#     # Create a collection within the database
# collection = db["mycollection"]  # Replace "mycollection" with your desired collection name
#
# User_Collection =db["users"]  # Replace with the collection name


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

        if user_data:
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
@ns.route('/OTPlogin')
class OTPLogin(Resource):
    #@api.expect(login_user_model, validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        otp = data['otp']
        offerID = data['offerID']
        offer_collection = db["offers"]
        #offer_data = offer_collection.find_one({'_id': ObjectId(offerID)})
        offer_data = offer_collection.find_one({'_id': ObjectId(offerID), 'OTP': otp})
        print(offer_data)
        if offer_data:
            additional_claims = {"roles": ["customer"]}
            access_token = create_access_token(identity=offerID, additional_claims=additional_claims)
            return {'status':'PASS', 'access_token': access_token}, 200
        else:
            return {'status':'FAIL', 'message': 'Invalid credentials'}, 200

#--------------------------------------------------------------------

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


# Route to serve a static HTML page
@app.route('/static_page')
def static_page():
    return render_template('./index.html')

# Route to serve a customer View
@app.route('/customers')
def customer_view():
    return render_template('./Customers.html')

# Route to serve Customer Details
@app.route('/customerDetails')
def customerDetails_view():
    return render_template('./CustomerDetails.html')


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

db = client["DB_UnSecuredLoans1"]
customer_collection = db["customers"]

@ns.route('/Add customer')
class AddCustomers(Resource):
    @api.expect(customer_model, validate=True)
    def post(self):
        data=request.get_json()

        customer=customer_collection.insert_one(data)
        if customer:
            return {'status': 'Customer Created'}
        else:
            return {'status': 'Customer Creation Failed'}, 401

@ns.route('/fake-customers')
class FakeCustomersResource(Resource):
    #@api.expect(user_model, validate=True)
    def get(self):
        num_customers = 200
        fake_customers = [generate_fake_customer() for _ in range(num_customers)]
        inserted =customer_collection.insert_many(fake_customers)
        if inserted:
            return {'status': 'Fake Customers Created'},200
        else:
            return {'status': 'Customer Fake Creation Failed'}, 401


@ns.route('/sendOTP')
class sendOTP(Resource):
    #@api.expect(user_model, validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        custID = data['data']['_id']['$oid']
        otp = generate_OTP()
        print(str(otp), custID)
        setval={"OTP":otp}
        offer_collection = db["offers"]
        result = offer_collection.update_one({'_id': ObjectId(custID)}, {"$set": setval})
        print(result)
        if result.matched_count > 0 :
            return {'status': 'OTP Generated', "otp":otp},200
        else:
            return {'status': 'Customer Fake Creation Failed'}, 401



@ns.route('/getCustomers')
class getCustomers(Resource):
    #@api.expect(customer_model, validate=True)
    def get(self):
        customer_collection = db["customers"]

        if customer_collection is not None:
            cur = customer_collection.find()
            list_cur = list(cur)
            res= dumps(list_cur, indent=2)
            return {'customers': res},200
        else:
            return {'status': 'Customer Fetch Failed'}, 401


@ns.route('/getCustomerDetails')
class getCustomerDetails(Resource):
    #@api.expect(customer_model, validate=True)
    def post(self):
        data = request.get_json()
        custID = data['id']
        print(custID)
        customer_collection = db["customers"]
        customer_data = customer_collection.find_one({'_id': ObjectId(custID)})
        if customer_data is not None:
           # list_cur = list(customer_data)
            res= dumps(customer_data, indent=2)
            return {'CustomerDetails': res},200
        else:
            return {'status': 'Customer Details Fetch Failed'}, 401



#used in updating customer records
@ns.route('/saveCustomerDetails')
class postCustomerDetails(Resource):
    #@api.expect(customer_model, validate=True)
    def post(self):
        reqdata = request.get_json()
        print(reqdata)
        custID = reqdata['data']['_id']['$oid']
        print(custID)
        customer_collection = db["customers"]
        del reqdata['data']['_id']
        result = customer_collection.update_one({'_id': ObjectId(custID)}, {"$set":reqdata['data']})
        #print(customer_data)
        if result.matched_count > 0 :
           # list_cur = list(customer_data)
            #res= dumps(customer_data, indent=2)
            return {'status': "updated"},200 #mongo collection updated
        else:
            return {'status': 'Customer Details update Failed'}, 401

#------------------------------------------------------------------------------------
# Route to serve a offers View
@app.route('/offers')
def offer_view():
    return render_template('./Offers.html')

# Route to serve individual offer details or add new offer
@app.route('/offerDetails')
def offer_details():
    return render_template('./OfferDetails.html')



@ns.route('/getOffers')
class getOffers(Resource):
    #@api.expect(customer_model, validate=True)
    def get(self):
        offer_collection = db["offers"]

        if offer_collection is not None:
            cur = offer_collection.find()
            list_cur = list(cur)
            res= dumps(list_cur, indent=2)
            return {'offers': res},200
        else:
            return {'status': 'Offer Fetch Failed'}, 401


@ns.route('/getOfferDetails')
class getOfferDetails(Resource):
    #@api.expect(customer_model, validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        offerID = data['id']
        #print(custID)
        offer_collection = db["offers"]
        offer_data = offer_collection.find_one({'_id': ObjectId(offerID)})
        print(offer_data)
        print(offer_data['Account_ID'])
        customer_data=db["customers"].find_one({'Account_ID':offer_data['Account_ID']})
        print(customer_data)
        offer_data["customerDetails"] = customer_data
        if offer_data is not None:
           # list_cur = list(customer_data)
            res= dumps(offer_data, indent=2)
            return {'OfferDetails': res, 'Role':'CUSTOMER'},200
        else:
            return {'status': 'Offer Details Fetch Failed'}, 401



#used in updating customer records
@ns.route('/saveOfferDetails')
class postOfferDetails(Resource):
    #@api.expect(customer_model, validate=True)
    def post(self):
        reqdata = request.get_json()
        print(reqdata)
        offer_collection = db["offers"]
        update=1
       # if reqdata['data']['_id'] is not None and reqdata['data']['_id']['$oid'] is not None:
        if "_id" in reqdata['data'] and "$oid" in reqdata['data']['_id']:

             offerID = reqdata['data']['_id']['$oid']
             #print(custID)

             del reqdata['data']['_id']
             result = offer_collection.update_one({'_id': ObjectId(offerID)}, {"$set":reqdata['data']})
        else:
            update = 0
            result = offer_collection.insert_one(reqdata['data'])
        if update == 0 and result is not None:
            return {'status': "created"}, 200  # mongo collection updated
        elif result.matched_count > 0:
           # list_cur = list(customer_data)
            #res= dumps(customer_data, indent=2)
            return {'status': "updated"},200 #mongo collection updated
        else:
            return {'status': 'Offer Details update Failed'}, 401
