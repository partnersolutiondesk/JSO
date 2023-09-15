#import AppInit

# Define user model
role_model = AppInit.api.model('role', {'role': AppInit.fields.String()})
user_model = AppInit.api.model('User', {
    'username': AppInit.fields.String(required=True, description='Username'),
    'password': AppInit.fields.String(required=True, description='Password'),
    'roles': AppInit.fields.List(AppInit.fields.Nested(role_model))
})

login_user_model = AppInit.api.model('login_user_model', {
    'username': AppInit.fields.String(required=True, description='Username'),
    'password': AppInit.fields.String(required=True, description='Password')
})

# Define JWT token model
token_model = AppInit.api.model('Token', {
    'access_token': AppInit.fields.String(description='Access Token')
})

