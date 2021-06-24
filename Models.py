from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model): 
    __tablename__ = 'user_table'

    userid = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(8), nullable=False)

    def __init__(self, userid, email, password):
        self.userid = userid
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)

