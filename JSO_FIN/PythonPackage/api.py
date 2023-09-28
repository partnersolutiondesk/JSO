import os

import requests
import re
import socket
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from .AppInit import app, api, fields, Resource, ns, request, client, User_Collection, db, render_template
from .Models import login_user_model, user_model, customer_model, auditrails_model
from .Libs.DataSimulation import generate_fake_customer, generate_OTP
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime

from bson.int64 import Int64

# -------------------------


# Configure JWT settings
app.config['JWT_SECRET_KEY'] = 'A#B#C@5%8'  # Secret key to sign the JWT tokens
jwt = JWTManager(app)


# db = client["DB_UnSecuredLoans1"]  # Replace "mydatabase" with your desired database name
#     # Create a collection within the database
# collection = db["mycollection"]  # Replace "mycollection" with your desired collection name
#
# User_Collection =db["users"]  # Replace with the collection name


def get_host_port():
    # Get the hostname of the local machine
    hostname = socket.gethostname()

    # Get the port number associated with a service (e.g., HTTP)
    service = "http"
    port = socket.getservbyname(service)

    return hostname, port


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
            # access_token = create_access_token(identity=username)
            # access_token = create_access_token(identity=username, user_claims={'roles': user_data.get('roles', [])})
            # additional_claims=user_data.get('roles', [])
            additional_claims = {"roles": user_data.get('roles', [])}
            # print()
            access_token = create_access_token(identity=user_data["username"], additional_claims=additional_claims)
            return {'access_token': access_token}
        else:
            return {'message': 'Invalid credentials'}, 401


# ------------------------------------------------------------------

# Login endpoint to obtain a JWT token
@ns.route('/OTPlogin')
class OTPLogin(Resource):
    # @api.expect(login_user_model, validate=True)
    def post(self):
        serverConfig = read_config(
            r'C:\Users\Sikha.P\OneDrive - Automation Anywhere Software Private Limited\AA_SIKHA\AA_SIKHA\PROJECTS\JSO\BackEnd\Git\JSO\JSO_FIN\serverConfig.json')
        print(serverConfig)
        data = request.get_json()
        print("sasadasdasd")
        print(data)
        otp = data['otp']
        offerID = data['offerID']
        offer_collection = db["offers"]
        offer_data = offer_collection.find_one({'_id': ObjectId(offerID)})
        # offer_data = offer_collection.find_one({'_id': ObjectId(offerID), 'OTP': otp})
        print(offer_data)
        customer_data = db["customers"].find_one({'Account_ID': offer_data['Account_ID']})
        print(customer_data)
        customerObjID = str(customer_data["_id"])
        print(customerObjID)
        if offer_data:
            additional_claims = {"roles": ["customer"]}
            access_token = create_access_token(identity=offerID, additional_claims=additional_claims)
            print(data)
            # Trigger the loan process at this point using deployment API
            baseUrl = serverConfig['scheme'] + "://" + serverConfig['host'] + ":" + serverConfig['port']
            deployTriggerLoanProcessBot(offerID, customerObjID, baseUrl + "/jso/getCustomerDetailsv2",
                                        baseUrl + "/jso/acceptOffer/" + offerID,
                                        baseUrl + "/jso/rejectOffer/" + offerID)
            return {'status': 'PASS', 'access_token': access_token}, 200
        else:
            return {'status': 'FAIL', 'message': 'Invalid credentials'}, 200


# --------------------------------------------------------------------

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


# ------------------------------------------------------------------
# Protected resource that requires a valid JWT token
@ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        # user_roles = get_jwt_claims().get('roles', [])
        jwt_dict = get_jwt()
        user_roles = jwt_dict["roles"]
        for roleObj in user_roles:
            if roleObj["role"] == "USER" or roleObj["role"] == "ANALYST":
                return {'message': f'Access granted to {current_user}'}
            else:
                return {'message': f'Access denied to {current_user}'}


# ------------------------------------------------------------------


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
        data = request.get_json()

        customer = customer_collection.insert_one(data)
        if customer:
            return {'status': 'Customer Created'}
        else:
            return {'status': 'Customer Creation Failed'}, 401


@ns.route('/fake-customers')
class FakeCustomersResource(Resource):
    # @api.expect(user_model, validate=True)
    def get(self):
        num_customers = 3
        fake_customers = [generate_fake_customer() for _ in range(num_customers)]
        inserted = customer_collection.insert_many(fake_customers)
        if inserted:
            return {'status': 'Fake Customers Created'}, 200
        else:
            return {'status': 'Customer Fake Creation Failed'}, 401


@ns.route('/sendOTP')
class sendOTP(Resource):
    # @api.expect(user_model, validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        custID = data['data']['_id']['$oid']
        otp = generate_OTP()
        print(str(otp), custID)
        setval = {"OTP": otp}
        offer_collection = db["offers"]
        result = offer_collection.update_one({'_id': ObjectId(custID)}, {"$set": setval})
        print(result)
        if result.matched_count > 0:
            return {'status': 'OTP Generated', "otp": otp}, 200
        else:
            return {'status': 'Customer Fake Creation Failed'}, 401


def updateOfferStatus(status, offer_data, offerID):
    offer_data['Status'] = status
    offer_data['LastModified'] = datetime.utcnow()
    offer_collection = db["offers"]
    result = offer_collection.update_one({'_id': ObjectId(offerID)}, {"$set": offer_data})
    return result


def insertAuditTrailEntry(audittrailEntry, masterEntry, customer_data):
    audittrails_collection = db["audittrails"]
    master_DescriptionPattern = masterEntry['Key_Description']
    # Define a regular expression pattern to match values inside <>
    pattern = r'<(.*?)>'
    # Use re.findall to find all matches of the pattern in the sentence
    matches = re.findall(pattern, master_DescriptionPattern)
    # Convert the matches to an array
    variables_in_description = list(matches)
    print(variables_in_description)
    audittrail_description = master_DescriptionPattern
    for value in variables_in_description:
        splitted = value.split('.')
        collectionName = splitted[0]
        attributeName = splitted[1]
        if collectionName == 'audittrails':
            if attributeName == "Actor_ID":
                if audittrailEntry[attributeName] == "Admin":
                    attributeValue = "Admin"
                else:
                    attributeValue = str(customer_data["First_Name"]) + " " + str(
                        customer_data["Last_Name"]) + "( " + \
                                     str(audittrailEntry[attributeName]) + ")"
            else:
                attributeValue = audittrailEntry[attributeName]
        if collectionName == 'master':
            attributeValue = masterEntry[attributeName]
        audittrail_description = audittrail_description.replace("<" + value + ">", str(attributeValue))
    print(audittrail_description)
    keyToRemove = "OfferID"
    if keyToRemove in audittrailEntry:
        del audittrailEntry[keyToRemove]
    audittrailEntry['Description'] = audittrail_description
    audittrails_collection.insert_one(audittrailEntry)
    return audittrails_collection


@ns.route('/ProceedWithOffer')
class ProceedWithOffer(Resource):
    # @api.expect(user_model, validate=True)
    def post(self):
        print("inside")
        data = request.get_json()
        print(data)

        offer_collection = db["offers"]
        offer_data = offer_collection.find_one({'_id': ObjectId(data['offerID'])})
        print(offer_data)
        otp = offer_data['OTP']
        print("before deploy")
        customer_data = db["customers"].find_one({'Account_ID': offer_data['Account_ID']})

        # deploySendOTPBot(offer_data['customerDetails'][', otp, "psdaa48@gmail.com")
        # deploySendOTPBot("+918157897518", otp, "psdaa48@gmail.com")
        deploySendOTPBot(customer_data['Phone_Number'], otp, customer_data['Email'])

        # Update offer status as "INTERESTED" "30"
        # offer_data['Status'] = "30"
        # result = offer_collection.update_one({'_id': ObjectId(data['offerID'])}, {"$set": offer_data})
        result = updateOfferStatus("30", offer_data, data['offerID'])
        # Update audit trail
        customer_data = db["customers"].find_one({'Account_ID': offer_data['Account_ID']})
        audittrails_collection = db["audittrails"]
        master_collection = db["master"]
        masterEntry = master_collection.find_one(({"Key_Name": "OfferStatus", "Key_Value": offer_data['Status']}))
        audittrailEntry = {
            "Date": datetime.utcnow(), "Status": "30", "Actor_ID": customer_data['_id'],
            "Role": "Customer", "Type": "Offer", "Description": "", "OfferID": str(offer_data['_id'])
        }
        master_DescriptionPattern = masterEntry['Key_Description']
        # Define a regular expression pattern to match values inside <>
        pattern = r'<(.*?)>'
        # Use re.findall to find all matches of the pattern in the sentence
        matches = re.findall(pattern, master_DescriptionPattern)
        # Convert the matches to an array
        variables_in_description = list(matches)
        print(variables_in_description)
        audittrail_description = master_DescriptionPattern
        for value in variables_in_description:
            splitted = value.split('.')
            collectionName = splitted[0]
            attributeName = splitted[1]
            if collectionName == 'audittrails':
                if attributeName == "Actor_ID":
                    attributeValue = str(customer_data["First_Name"]) + " " + str(
                        customer_data["Last_Name"]) + "( " + \
                                     str(audittrailEntry[attributeName]) + ")"
                else:
                    attributeValue = audittrailEntry[attributeName]
            if collectionName == 'master':
                attributeValue = masterEntry[attributeName]
            audittrail_description = audittrail_description.replace("<" + value + ">", str(attributeValue))
        print(audittrail_description)
        audittrailEntry['Description'] = audittrail_description
        audittrails_collection.insert_one(audittrailEntry)

        print(result)
        #
        return {'status': 'Thanks for choosing the offer. You will get a notification soon'}, 200


@ns.route('/NotInterested')
class NotInterested(Resource):
    # @api.expect(user_model, validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        offer_collection = db["offers"]
        offer_data = offer_collection.find_one({'_id': ObjectId(data['offerID'])})
        print(offer_data)

        # Update offer status as "NOT_INTERESTED" "40"
        offer_data['Status'] = "40"
        result = offer_collection.update_one({'_id': ObjectId(data['offerID'])}, {"$set": offer_data})
        # Update audit trail
        customer_data = db["customers"].find_one({'Account_ID': offer_data['Account_ID']})
        audittrails_collection = db["audittrails"]
        master_collection = db["master"]
        masterEntry = master_collection.find_one(({"Key_Name": "OfferStatus", "Key_Value": offer_data['Status']}))
        audittrailEntry = {
            "Date": datetime.utcnow(), "Status": "40", "Actor_ID": customer_data['_id'],
            "Role": "Customer", "Type": "Offer", "Description": "", "OfferID": str(offer_data['_id'])
        }
        master_DescriptionPattern = masterEntry['Key_Description']
        # Define a regular expression pattern to match values inside <>
        pattern = r'<(.*?)>'
        # Use re.findall to find all matches of the pattern in the sentence
        matches = re.findall(pattern, master_DescriptionPattern)
        # Convert the matches to an array
        variables_in_description = list(matches)
        print(variables_in_description)
        audittrail_description = master_DescriptionPattern
        for value in variables_in_description:
            splitted = value.split('.')
            collectionName = splitted[0]
            attributeName = splitted[1]
            if collectionName == 'audittrails':
                if attributeName == "Actor_ID":
                    attributeValue = str(customer_data["First_Name"]) + " " + str(
                        customer_data["Last_Name"]) + "( " + \
                                     str(audittrailEntry[attributeName]) + ")"
                else:
                    attributeValue = audittrailEntry[attributeName]
            if collectionName == 'master':
                attributeValue = masterEntry[attributeName]
            audittrail_description = audittrail_description.replace("<" + value + ">", str(attributeValue))
        print(audittrail_description)
        audittrailEntry['Description'] = audittrail_description
        audittrails_collection.insert_one(audittrailEntry)

        print(result)
        #
        return {'status': 'Thanks for your update'}, 200


def DeployCAMReportBot(CAMReport_json_string, OfferID):
    # function body
    api_url = config_data['ControlRoomUrl'] + "/v4/automations/deploy"
    input_data = {
        "botId": config_data['CAMReportBotID'],
        "botInput": {
            "UnderWriterName": {
                "type": "STRING",
                "string": "UnderWriter"
            },
            "UnderWriterEmail": {
                "type": "STRING",
                "string": "sikha.p@automationanywhere.com"
            },
            "CAMReportJson": {
                "type": "STRING",
                "string": CAMReport_json_string
            },
            "OfferID": {
                "type": "STRING",
                "string": OfferID
            }
        },
        "automationPriority": "PRIORITY_MEDIUM",
        "unattendedRequest": {
            "runAsUserIds": config_data['runAsUserIds'],
            "poolIds": config_data['poolIds'],
            "numOfRunAsUsersToUse": 0,
            "deviceUsageType": config_data['deviceUsageType']
        }
    }
    token = Authentication()
    print("token  ....................")
    print(token)
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*",
        "X-Authorization": token
    }
    print(api_url)
    print(input_data)
    print(headers)
    # Send a POST request to the API with input data and headers
    response = requests.post(api_url, json=input_data, headers=headers)
    print("sent bot deployment api")
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and use the response data (assuming it's in JSON format)
        data = response.json()
        print("API Response:")
        # print(data)
        return data
    else:
        print(f"API request failed with status code {response.status_code}")
        return "API request failed with status code "
    # print(f"API request failed: {e}")


@ns.route('/DeployNoActionOrMidwayMail')
class DeployNoActionOrMidwayMail(Resource):
    # @api.expect(user_model, validate=True)
    def post(self):
        data = request.get_json()
        type_ = data['type']
        inputs = data['inputs']
        DeployNoActionOrMidwayMailBot(type_, inputs)


def DeployNoActionOrMidwayMailBot(type_, inputs):
    # function body
    api_url = config_data['ControlRoomUrl'] + "/v4/automations/deploy"
    input_data = {
        "botId": config_data['MidwayOrNoactionMailBot'],
        "botInput": {
            "Type": {
                "type": "STRING",
                "string": type_
            },
            "inputs": {
                "type": "STRING",
                "string": inputs
            }
        },
        "automationPriority": "PRIORITY_MEDIUM",
        "unattendedRequest": {
            "runAsUserIds": config_data['runAsUserIds'],
            "poolIds": config_data['poolIds'],
            "numOfRunAsUsersToUse": 0,
            "deviceUsageType": config_data['deviceUsageType']
        }
    }
    token = Authentication()
    print("token  ....................")
    print(token)
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*",
        "X-Authorization": token
    }
    print(api_url)
    print(input_data)
    print(headers)
    # Send a POST request to the API with input data and headers
    response = requests.post(api_url, json=input_data, headers=headers)
    print("sent bot deployment api")
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and use the response data (assuming it's in JSON format)
        data = response.json()
        print("API Response:")
        # print(data)
        return data
    else:
        print(f"API request failed with status code {response.status_code}")
        return "API request failed with status code "
    # print(f"API request failed: {e}")


def generateCAMReport(offer_data, customer_data):
    print("cammmmmmmmmmmmmmmm")
    salariedStatus = 'Salaried' if customer_data['Profession'] != "self" else "Non-Salaried"
    master_collection = db["master"]
    masterEntry = master_collection.find_one(
        ({"Key_Name": "CAMReport", "Key_Text": salariedStatus + "_ExecutiveSummary"}))
    ExecutiveSummary = masterEntry['Key_Description']
    camReportData = {
        "ReportedDate": str(datetime.utcnow()),
        "ReportPreparedBy": "System",
        "CustomerName": customer_data['First_Name'] + " " + customer_data['Last_Name'],
        "ExecutiveSummary": ExecutiveSummary,
        "CustomerID": customer_data['Account_ID'],
        "DateOfBirth": str(customer_data['DOB']),
        "ContactNumber": customer_data['Phone_Number'],
        "EmailAddress": customer_data['Email'],
        "PermanentAddress": customer_data['Address'],
        "EmploymentStatus": salariedStatus,
        "EmployerName": customer_data['EmployerName'],
        "MonthlySalary": customer_data['MonthlySalary'],
        "CurrentOutstandingBalance": customer_data['CurrentBalance'],
        "LoanOrEMIDetails": offer_data['EMIDetails'],
        "LoanType": offer_data['LoanType'],
        "LoanAmount": offer_data['Amount'],
        "InterestRate": offer_data['InterestRate'],
        "EMIAmount": offer_data['EMIAmount'],
        "LoanTenure": offer_data['TenureInMonths'],
        "CreditScore": customer_data['credit_score']
    }

    # Convert the dictionary to a JSON string
    CAMReport_json_string = json.dumps(camReportData, indent=4)  # Using indent for pretty formatting

    # Specify the path to the text file
    file_path = "files/CAMReport_" + str(offer_data['_id']) + ".txt"

    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the JSON string to the file
        file.write(CAMReport_json_string)
    absolute_path = os.path.abspath(file_path)
    print(f"JSON data has been written to '{file_path}'" + absolute_path)
    # Add an entry to camreports table
    camreports_collection = db["camreports"]
    camreports_collection.insert_one({
        "reportedDate": camReportData['ReportedDate'],
        "reportPreparedBy": camReportData['ReportPreparedBy'],
        "reportJSON": str(camReportData),
        "executiveSummary": camReportData['ExecutiveSummary'],
        "OfferID": str(offer_data['_id'])
    })
    # Add an entry to audittrails table
    master_collection = db["master"]
    masterEntry = master_collection.find_one(({"Key_Name": "CAMReport", "Key_Value": "AuditTrail"}))
    audittrailEntry = {
        "Date": datetime.utcnow(), "Status": "Generated & shared", "Actor_ID": "Admin",
        "Role": "SystemUser", "Type": "Offer", "Description": "", "OfferID": str(offer_data['_id'])
    }
    insertAuditTrailEntry(audittrailEntry, masterEntry, customer_data)
    # Send CAMReport to UnderWriter . call bot deployment API pass the json
    DeployCAMReportBot(CAMReport_json_string, str(offer_data['_id']))
    return "done"


@ns.route('/reviewOfferStatus/<string:id>/<string:status>')
class ReviewOfferStatus(Resource):
    def get(self, id, status):
        print(id)
        offerID = id
        print(status)
        statusID = ""
        if status == "accepted":
            statusID = "70"
        if status == "rejected":
            statusID = "80"

        offer_collection = db["offers"]
        offer_data = offer_collection.find_one({'_id': ObjectId(offerID)})

        result = updateOfferStatus(statusID, offer_data, offerID)

        master_collection = db["master"]
        masterEntry = master_collection.find_one(({"Key_Name": "OfferStatus", "Key_Value": statusID}))
        audittrailEntry = {
            "Date": datetime.utcnow(), "Status": statusID, "Actor_ID": "Admin",
            "Role": "Employee", "Type": "Offer", "Description": "", "OfferID": str(offer_data['_id'])
        }
        insertAuditTrailEntry(audittrailEntry, masterEntry, "")
        return {'status': 'Status updated'}, 200


@ns.route('/acceptOffer/<string:id>')
class AcceptOffer(Resource):
    # @api.expect(offer_model, validate=True)
    def get(self, id):
        print(id)
        status = "50"
        offerID = id
        offer_collection = db["offers"]
        offer_data = offer_collection.find_one({'_id': ObjectId(offerID)})
        customer_data = db["customers"].find_one({'Account_ID': offer_data['Account_ID']})
        updateOfferStatus(status, offer_data, offerID)
        master_collection = db["master"]
        masterEntry = master_collection.find_one(({"Key_Name": "OfferStatus", "Key_Value": status}))
        audittrailEntry = {
            "Date": datetime.utcnow(), "Status": status, "Actor_ID": customer_data['_id'],
            "Role": "Customer", "Type": "Offer", "Description": "", "OfferID": str(offer_data['_id'])
        }
        insertAuditTrailEntry(audittrailEntry, masterEntry, customer_data)
        # start amount disbursement - Update offer entry & insert new audit entry
        disbursementStatus = "100"
        updateOfferStatus(disbursementStatus, offer_data, offerID)
        masterEntry_disbursement = master_collection.find_one(
            ({"Key_Name": "OfferStatus", "Key_Value": disbursementStatus}))
        audittrailEntry_disbursement = {
            "Date": datetime.utcnow(), "Status": disbursementStatus, "Actor_ID": "Admin",
            "Role": "SystemUser", "Type": "Offer", "Description": "", "OfferID": str(offer_data['_id'])
        }
        insertAuditTrailEntry(audittrailEntry_disbursement, masterEntry_disbursement, customer_data)

        generateCAMReport(offer_data, customer_data)
        return {'status': 'Thanks for accepting the offer. We started the loan process for you. You will be notified '
                          'shortly.'}, 200


@ns.route('/rejectOffer/<string:id>')
class RejectOffer(Resource):
    # @api.expect(offer_model, validate=True)
    def get(self, id):
        print(id)
        status = "60"
        offerID = id
        offer_collection = db["offers"]
        offer_data = offer_collection.find_one({'_id': ObjectId(offerID)})
        customer_data = db["customers"].find_one({'Account_ID': offer_data['Account_ID']})
        updateOfferStatus(status, offer_data, offerID)
        master_collection = db["master"]
        masterEntry = master_collection.find_one(({"Key_Name": "OfferStatus", "Key_Value": status}))
        audittrailEntry = {
            "Date": datetime.utcnow(), "Status": status, "Actor_ID": customer_data['_id'],
            "Role": "Customer", "Type": "Offer", "Description": "", "OfferID": str(offer_data['_id'])
        }
        insertAuditTrailEntry(audittrailEntry, masterEntry, customer_data)

        return {'status': 'Thanks for accepting the offer'}, 200


@ns.route('/getCustomers')
class getCustomers(Resource):
    # @api.expect(customer_model, validate=True)
    def get(self):
        customer_collection = db["customers"]

        if customer_collection is not None:
            cur = customer_collection.find()
            list_cur = list(cur)
            res = dumps(list_cur, indent=2)
            return {'customers': res}, 200
        else:
            return {'status': 'Customer Fetch Failed'}, 401


@ns.route('/getCustomerDetails')
class getCustomerDetails(Resource):
    # @api.expect(customer_model, validate=True)
    def post(self):
        data = request.get_json()
        custID = data['id']
        print(custID)
        customer_collection = db["customers"]
        customer_data = customer_collection.find_one({'_id': ObjectId(custID)})
        if customer_data is not None:
            # list_cur = list(customer_data)
            res = dumps(customer_data, indent=2)
            return {'CustomerDetails': res}, 200
        else:
            return {'status': 'Customer Details Fetch Failed'}, 401


@ns.route('/getCustomerDetailsv2')
class getCustomerDetailsv2(Resource):
    # @api.expect(customer_model, validate=True)
    def post(self):
        data = request.get_json()
        custID = data['id']
        print(custID)
        customer_collection = db["customers"]
        customer_data = customer_collection.find_one({'_id': ObjectId(custID)})
        if customer_data is not None:
            # list_cur = list(customer_data)
            res = dumps(customer_data, indent=4)
            print("res['DOB']")
            print(customer_data['DOB'])
            return {'CustomerDetails': res}, 200
        else:
            return {'status': 'Customer Details Fetch Failed'}, 401


# used in updating customer records
@ns.route('/saveCustomerDetails')
class postCustomerDetails(Resource):
    # @api.expect(customer_model, validate=True)
    def post(self):
        reqdata = request.get_json()
        print(reqdata)
        custID = reqdata['data']['_id']['$oid']
        print(custID)
        customer_collection = db["customers"]
        del reqdata['data']['_id']
        result = customer_collection.update_one({'_id': ObjectId(custID)}, {"$set": reqdata['data']})
        # print(customer_data)
        if result.matched_count > 0:
            # list_cur = list(customer_data)
            # res= dumps(customer_data, indent=2)
            return {'status': "updated"}, 200  # mongo collection updated
        else:
            return {'status': 'Customer Details update Failed'}, 401


# ------------------------------------------------------------------------------------
# Route to serve a offers View
@app.route('/offers')
def offer_view():
    return render_template('./Offers.html')


# Route to serve individual offer details or add new offer
@app.route('/offerDetails')
def offer_details():
    return render_template('./OfferDetails.html')


@app.route('/audittrails')
def audittrail_view():
    return render_template('./AuditTrails.html')


@ns.route('/getOffers')
class getOffers(Resource):
    # @api.expect(customer_model, validate=True)
    def get(self):
        offer_collection = db["offers"]

        if offer_collection is not None:
            cur = offer_collection.find()
            list_cur = list(cur)
            res = dumps(list_cur, indent=2)
            return {'offers': res}, 200
        else:
            return {'status': 'Offer Fetch Failed'}, 401


@ns.route('/getAudittrails')
class getAudittrails(Resource):
    # @api.expect(customer_model, validate=True)
    def get(self):
        audittrail_collection = db["audittrails"]

        if audittrail_collection is not None:
            cur = audittrail_collection.find()
            list_cur = list(cur)
            res = dumps(list_cur, indent=2)
            return {'audittrails': res}, 200
        else:
            return {'status': 'Audittrails Fetch Failed'}, 401

@app.route('/camreports')
def camreports_view():
    return render_template('./CAMReports.html')


@ns.route('/getCAMReports')
class getCAMReports(Resource):
    # @api.expect(customer_model, validate=True)
    def get(self):
        camreport_collection = db["camreports"]

        if camreport_collection is not None:
            cur = camreport_collection.find()
            list_cur = list(cur)
            res = dumps(list_cur, indent=2)
            return {'camreports': res}, 200
        else:
            return {'status': 'camreports Fetch Failed'}, 401




@ns.route('/getOfferDetails')
class getOfferDetails(Resource):
    # @api.expect(customer_model, validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        offerID = data['id']
        # print(custID)
        offer_collection = db["offers"]
        offer_data = offer_collection.find_one({'_id': ObjectId(offerID)})
        print(offer_data)
        print(offer_data['Account_ID'])
        customer_data = db["customers"].find_one({'Account_ID': offer_data['Account_ID']})
        print(customer_data)
        offer_data["customerDetails"] = customer_data
        if offer_data is not None:
            # list_cur = list(customer_data)
            res = dumps(offer_data, indent=2)
            return {'OfferDetails': res, 'Role': 'CUSTOMER'}, 200
        else:
            return {'status': 'Offer Details Fetch Failed'}, 401


# used in updating customer records
@ns.route('/saveOfferDetails')
class postOfferDetails(Resource):
    # @api.expect(customer_model, validate=True)
    def post(self):
        reqdata = request.get_json()
        print(reqdata)
        offer_collection = db["offers"]
        update = 1
        # if reqdata['data']['_id'] is not None and reqdata['data']['_id']['$oid'] is not None:
        if "_id" in reqdata['data'] and "$oid" in reqdata['data']['_id']:

            offerID = reqdata['data']['_id']['$oid']
            # print(custID)

            del reqdata['data']['_id']
            result = offer_collection.update_one({'_id': ObjectId(offerID)}, {"$set": reqdata['data']})
        else:
            update = 0
            result = offer_collection.insert_one(reqdata['data'])
        if update == 0 and result is not None:
            return {'status': "created"}, 200  # mongo collection updated
        elif result.matched_count > 0:
            # list_cur = list(customer_data)
            # res= dumps(customer_data, indent=2)
            return {'status': "updated"}, 200  # mongo collection updated
        else:
            return {'status': 'Offer Details update Failed'}, 401


@ns.route('/getOfferStatus')
class getOfferStatus(Resource):
    # @api.expect(customer_model, validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        offerID = data['id']
        offer_collection = db["offers"]
        master_collection = db["master"]

        if offer_collection is not None:
            cur = offer_collection.find_one({'_id': ObjectId(offerID)})
            masterEntry = master_collection.find_one({'Key_Value': cur['Status'], "Key_Name": "OfferStatus"})
            print("asdddddddddddddddddddddd")
            print(masterEntry)
            cur['StatusText'] = masterEntry['Key_Text']
            res = dumps(cur, indent=2)

            return {'offerDetails': res}, 200
        else:
            return {'status': 'offerdetails Fetch Failed'}, 401


# RPA Related functions

config_file_path = "config.json"


def read_config(file_path):
    try:
        with open(file_path, "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print(f"Config file '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


config_data = read_config("config.json")

print(config_data)
#config_data = read_config(
 #   r"C:\Users\Sikha.P\OneDrive - Automation Anywhere Software Private Limited\AA_SIKHA\AA_SIKHA\PROJECTS\JSO\BackEnd\Git\JSO\JSO_FIN\PythonPackage\config.json")


def Authentication():
    # function body
    print(config_data)
    print(config_data['ControlRoomUrl'])
    api_url = config_data['ControlRoomUrl'] + "/v1/authentication"
    input_data = {
        "username": config_data['username'],
        "password": config_data['password']
    }
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    # Send a POST request to the API with input data and headers
    response = requests.post(api_url, json=input_data, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and use the response data (assuming it's in JSON format)
        data = response.json()
        print("API Response:")
        print(data['token'])
        return data['token']
    else:
        # print(f"API request failed with status code {response.status_code}")
        return "API request failed with status code "
    # print(f"API request failed: {e}")


def deploySendOTPBot(mobileNumber, otp, toAddress):
    # function body
    print(config_data['ControlRoomUrl'])
    api_url = config_data['ControlRoomUrl'] + "/v4/automations/deploy"
    input_data = {
        "botId": config_data['SendOTPBot'],
        "botInput": {
            "mobileNumber": {
                "type": "STRING",
                "string": mobileNumber
            },
            "logFilePath": {
                "type": "STRING",
                "string": config_data['logFilePath']
            },
            "otp": {
                "type": "STRING",
                "string": otp
            },
            "ToAddress": {
                "type": "STRING",
                "string": toAddress
            }
        },
        "automationPriority": "PRIORITY_MEDIUM",
        "unattendedRequest": {
            "runAsUserIds": config_data['runAsUserIds'],
            "poolIds": config_data['poolIds'],
            "numOfRunAsUsersToUse": 0,
            "deviceUsageType": config_data['deviceUsageType']
        }
    }
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*",
        "X-Authorization": Authentication()
    }

    # Send a POST request to the API with input data and headers
    response = requests.post(api_url, json=input_data, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and use the response data (assuming it's in JSON format)
        data = response.json()
        print("API Response:")
        print(data)
        return data
    else:
        print(f"API request failed with status code {response.status_code}")
        return "API request failed with status code "
    # print(f"API request failed: {e}")


def deployTriggerLoanProcessBot(offerID, customerObjID, getCustomerDetailsAPIUrl, acceptOfferAPIUrl,
                                rejectOfferAPIUrl):
    # function body
    print(config_data['ControlRoomUrl'])
    api_url = config_data['ControlRoomUrl'] + "/v4/automations/deploy"
    input_data = {
        "botId": config_data['TriggerLoanProcessBot'],
        "botInput": {
            "offerID": {
                "type": "STRING",
                "string": offerID
            },
            "customerObjID": {
                "type": "STRING",
                "string": customerObjID
            },
            "getCustomerDetailsAPIUrl": {
                "type": "STRING",
                "string": getCustomerDetailsAPIUrl
            },
            "acceptOfferAPIUrl": {
                "type": "STRING",
                "string": acceptOfferAPIUrl
            },
            "rejectOfferAPIUrl": {
                "type": "STRING",
                "string": rejectOfferAPIUrl
            }
        },
        "automationPriority": "PRIORITY_MEDIUM",
        "unattendedRequest": {
            "runAsUserIds": config_data['runAsUserIds'],
            "poolIds": config_data['poolIds'],
            "numOfRunAsUsersToUse": 0,
            "deviceUsageType": config_data['deviceUsageType']
        }
    }
    token = Authentication()
    print("token  ....................")
    print(token)
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*",
        "X-Authorization": token
    }
    print(api_url)
    print(input_data)
    print(headers)
    # Send a POST request to the API with input data and headers
    response = requests.post(api_url, json=input_data, headers=headers)
    print("sent bot deployment api")
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and use the response data (assuming it's in JSON format)
        data = response.json()
        print("API Response:")
        # print(data)
        return data
    else:
        print(f"API request failed with status code {response.status_code}")
        return "API request failed with status code "
    # print(f"API request failed: {e}")
