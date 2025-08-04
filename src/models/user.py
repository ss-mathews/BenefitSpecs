from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # Import this
from bcrypt import hashpw, gensalt, checkpw

db = SQLAlchemy()

# Make your User model inherit from UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        # Hash the password with a salt and store it
        self.password_hash = hashpw(password.encode('utf-8'), gensalt())

    def check_password(self, password):
        # Check a given password against the stored hash
        return checkpw(password.encode('utf-8'), self.password_hash)
