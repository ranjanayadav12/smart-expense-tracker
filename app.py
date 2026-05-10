from flask import Flask
from flask_socketio import SocketIO

# Config
from config import Config

# Database
from database.db import db

# Models
from model.user_model import User
from model.expense_model import Expense

# Routes
from routes.auth_routes import register_routes
from routes.expense_route import expense_routes

# Flask App
app = Flask(__name__)

# Load Config
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Initialize SocketIO
socketio = SocketIO(app)

# Register Routes
register_routes(app)

expense_routes(app, socketio)

# Create Database Tables
with app.app_context():
    db.create_all()

# Home Route
@app.route("/")
def home():
    return """
    <h2>Smart Expense Tracker Running Successfully 🚀</h2>
    <a href='/login'>Login</a>
    """

# Run App
if __name__ == "__main__":
    socketio.run(app, debug=True)