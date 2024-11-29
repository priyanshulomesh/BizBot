from app.databases.user_profile import UserProfile
from app.databases.db_init import db



class UserInput(db.Model):
    __tablename__ = 'user_input'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    user_name = db.Column(db.String, nullable=False)  # User's name
    gender = db.Column(db.String)  # Gender (optional)
    user_Address = db.Column(db.String)  # User's address (optional)
    # pincode = db.Column(db.Integer)  # Pincode (optional)
    # city = db.Column(db.String)  # City (optional)
    # state = db.Column(db.String)  # State (optional)

    def to_dict(self):
        return {
            'id': self.id,
            'user_profile_id': self.user_profile_id,
            'user_name': self.user_name,
            'gender': self.gender,
            'user_Address': self.user_Address
        }
    
# Utility function to save user input data
def save_user_input(user_id, input_data):
    # user_input = UserInput(user_name=input_data.get("user_name"), 
    #                     #    gender=input_data.get("gender"), 
    #                        user_Address=input_data.get("address"), 
    #                        pincode=input_data.get("pincode"), 
    #                        city=input_data.get("city"), 
    #                        state=input_data.get("state"))
    #user_id is wa_id i.e. phone number
    user =  UserProfile.query.filter_by(user_phone_number=user_id).first()
    user_input = UserInput(user_name=input_data.get("user_name"),user_profile_id=user.id,user_Address=input_data.get("address"))
    db.session.add(user_input)
    db.session.commit()