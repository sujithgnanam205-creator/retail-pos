from flask import Flask
from flask_cors import CORS
from routes import pos_routes

app = Flask(__name__)
CORS(app)

# Register all the routes from routes.py
app.register_blueprint(pos_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False)