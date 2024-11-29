from app.databases.db_init import db
from datetime import datetime

class Orders(db.Model):
    __tablename__='orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordered_by=db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    completed = db.Column(db.String(3), default="no", nullable=False) 

    grand_total=db.Column(db.Float)

def save_order(ordered_by,grand_total):
    new_order = Orders(ordered_by=ordered_by,grand_total=grand_total)

    # Add the new order to the database session
    db.session.add(new_order)

    # Commit the transaction to save the order
    db.session.commit()

    return new_order   
    