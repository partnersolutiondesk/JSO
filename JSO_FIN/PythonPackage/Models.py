from .AppInit import api, fields
# Define user model
role_model = api.model('role', {'role': fields.String()})
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'roles': fields.List(fields.Nested(role_model))
})

login_user_model = api.model('login_user', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

# Define JWT token model
token_model = api.model('Token', {
    'access_token': fields.String(description='Access Token')
})

# Customer
customer_model = api.model('Customer', {
    'First_Name': fields.String(description='First Name'),
    'Last_Name': fields.String(description='Last Name'),
    'Address': fields.String(description='Address'),
    'Account_ID': fields.String(description='Account ID'),
    'Age': fields.String(description='Age')
})

# master
master_model = api.model('Master', {
    'Loan Types': fields.String(description='Loan Type'),
    'Account Type': fields.String(description='Account Type')
})

#offer
offer_model = api.model('Offer', {
    'Type': fields.String(description='Offer Type'),
    'Status': fields.String(description='Status'),
    'Account_ID': fields.String(description='Account ID'),
    'Amount': fields.Integer(description='Amount'),
    'OTP':fields.Integer(description='OTP')
})

#audit trail
auditrail_model = api.model('auditrail', {
    'DateTime': fields.Date(description='Date and Time'),
    'Text': fields.String(description='Status'),
    'Offer_ID': fields.String(description='Offer ID')
})