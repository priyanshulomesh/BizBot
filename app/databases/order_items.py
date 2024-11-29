from app.databases.db_init import db

class OrderItems(db.Model):
    __tablename__ = 'order_items'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('reply_list.list_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    bill_amount = db.Column(db.Float, nullable=False)
    

def save_order_item(order_id, item_id, quantity,bill_amount):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    if bill_amount <= 0:
        raise ValueError("Bill amount must be greater than 0")

    # Create a new order item instance with the bill amount
    order_item = OrderItems(order_id=order_id, item_id=item_id, quantity=quantity, bill_amount=bill_amount)
    # order_item = OrderItems(order_id=order_id, item_id=item_id, quantity=quantity)

    # Add the order item to the session
    db.session.add(order_item)

    # Commit the transaction to save the order item
    db.session.commit()

    return order_item
