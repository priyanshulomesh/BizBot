from app.databases.db_init import db
from datetime import datetime

class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_phone_number = db.Column(db.String(15), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # Relationship to UserInput
    user_inputs = db.relationship('UserInput', backref='user_profile', lazy=True)

def check_user_exists(phone_number):
    user = UserProfile.query.filter_by(user_phone_number=phone_number).first()
    return user

def create_user_profile(phone_number):
    new_user = UserProfile(user_phone_number=phone_number, created_at=datetime.now())
    db.session.add(new_user)
    db.session.commit()
    print('User profile created')
    return new_user