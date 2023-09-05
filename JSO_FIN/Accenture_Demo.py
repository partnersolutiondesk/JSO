from flask import Flask, render_template, send_from_directory
from flask_restx import Api, Resource

app = Flask(__name__)

# Initialize Flask-RESTPlus API
api = Api(app, version='1.0', title='Sample API', description='A sample API with Swagger documentation')

# Namespace creation
ns = api.namespace('sample', description='Sample endpoints')

@ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        """
        Say hello!
        """
        return {'message': 'Hello, Flask-RESTPlus!'}

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
    app.run(debug=True)
