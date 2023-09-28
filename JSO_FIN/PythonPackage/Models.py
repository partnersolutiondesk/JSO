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
    'Age': fields.String(description='Age'),
    'Email': fields.String(description='Email'),
    'Phone_Number': fields.String(description='Phone Number'),
    'DOB': fields.String(description='DOB'),

    'Pincode': fields.String(description='Pincode'),

    'Profession': fields.String(description='Profession'),

    'credit_score': fields.Integer(description='credit score'),

    'Income_source': fields.String(description='Income source'),

    'Industry_Sector': fields.String(description='Industry Sector'),

    'Income_range': fields.Integer(description='Income range'),

    'Payslip': fields.String(description='Payslip'),

    'IT_return': fields.String(description='IT return'),

    'AML': fields.String(description='AML')

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
    'OTP':fields.Integer(description='OTP'),
    'Date':fields.Integer(description='Date'),
    'ExpiryDate':fields.Integer(description='ExpiryDate')
})

#offerStatuses
offerstatuses_model = api.model('OfferStatuses', {
    'Value': fields.Integer(description='Value'),
    'DisplayText': fields.String(description='Display Text')
})


#master
master_model = api.model('master', {
    'Key_Name': fields.Integer(description='Key Name'),
    'Key_Value': fields.String(description='Key Value'),
    'Key_Text': fields.String(description='Key Text'),
    'Key_Description': fields.String(description='Key Description')
})


#audit trail
auditrails_model = api.model('auditrails', {
    'DateTime': fields.Date(description='Date and Time'),
    'Status': fields.String(description='Status'),
    'Actor_ID': fields.String(description='Actor ID'),
    'Role': fields.String(description='Role'),
    'Type': fields.String(description='Type'),
    'Description': fields.String(description='Description')
})


#camreports
camreports_model = api.model('camreports', {
    'reportdate': fields.Date(description='Report Date'),
    'reportPreparedBy': fields.String(description='Report Prepared By'),
    'reportdocument': fields.String(description='Report Document')
})