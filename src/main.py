import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
# --- IMPORTS FOR AUTHENTICATION ---
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# --- IMPORT YOUR MODELS AND BLUEPRINTS ---
# Make sure your User model is imported correctly from your models file
from src.models.user import db, User
from src.routes.user import user_bp
from src.routes.benefitspecs import benefitspecs_bp

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# --- APP CONFIGURATION ---
# Use an environment variable for the secret key in production for security
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-default-secret-key-for-dev')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# This line will be replaced by the environment variable on Railway.
# For local development, it falls back to a local SQLite database.
# On Railway, set DATABASE_URL in your service's environment variables.
database_url = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for all routes to allow frontend interaction
CORS(app, supports_credentials=True)

# Initialize database with the app
db.init_app(app)

# --- FLASK-LOGIN CONFIGURATION ---
login_manager = LoginManager()
login_manager.init_app(app)

# This function tells Flask-Login how to load a user from the database given their ID.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# If a user tries to access a protected page without being logged in,
# we will return a 401 Unauthorized error. This is ideal for APIs.
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Authentication required. Please log in."}), 401

# --- REGISTER EXISTING BLUEPRINTS ---
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(benefitspecs_bp, url_prefix='/api')

# --- NEW AUTHENTICATION API ROUTES ---

@app.route('/api/register', methods=['POST'])
def register():
    """Registers a new user."""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(username=username)
    new_user.set_password(password)  # Use the method from your User model
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User '{username}' registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Logs in a user and creates a session."""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    # Use the check_password method from your User model
    if user and user.check_password(password):
        login_user(user)  # This function from Flask-Login creates the session cookie
        return jsonify({"message": f"Welcome, {user.username}!", "user": {"id": user.id, "username": user.username}}), 200
    
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/api/logout', methods=['POST'])
@login_required  # Ensures only logged-in users can access this
def logout():
    """Logs out the current user by clearing the session."""
    logout_user()  # This function from Flask-Login clears the session
    return jsonify({"message": "Successfully logged out"}), 200

@app.route('/api/profile')
@login_required  # This is an example of a protected route
def profile():
    """Returns the profile of the currently logged-in user."""
    # `current_user` is a proxy from Flask-Login to the logged-in user object
    return jsonify({
        "id": current_user.id,
        "username": current_user.username
    })

# --- CREATE DATABASE TABLES ---
# This block ensures that the database tables are created based on your models.
with app.app_context():
    # Create a directory for the SQLite database if it doesn't exist
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        db_dir = os.path.join(os.path.dirname(__file__), 'database')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
    db.create_all()

# --- SERVE STATIC FRONTEND ---
# This route serves your frontend application (e.g., a React or Vue build).
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found in static folder", 404

# --- RUN THE APP ---
# This block is for local development and will not be used by Gunicorn on Railway.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    # Use debug=False in a production-like local test
    app.run(host='0.0.0.0', port=port, debug=True)