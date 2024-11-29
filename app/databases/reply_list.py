from app.databases.db_init import db


class ReplyList(db.Model):
    __tablename__ = 'reply_list'

    list_id = db.Column(db.Integer, primary_key=True, nullable=False)
    list_name = db.Column(db.String, nullable=False)
    list_desc = db.Column(db.String, nullable=False)
    available_quantity=db.Column(db.Integer)

    menus = db.relationship('MenuReplyAssociation', backref='reply_list', lazy='joined')

# Function to send a list prompt
def create_list_items(list_ids):
    lists = ReplyList.query.filter(ReplyList.list_id.in_(list_ids.split(',')),ReplyList.available_quantity>0).all()
    return [{"id": l.list_id, "name": l.list_name, "desc": f"₹ {l.list_desc}"} for l in lists] 

def get_list_name_by_id(list_id):
    list_item = ReplyList.query.filter_by(list_id=list_id).first()
    if list_item:
        return list_item.list_name
    else:
        return None  # or handle it as you prefer
def get_list_desc_by_id(list_id):
    list_item = ReplyList.query.filter_by(list_id=list_id).first()
    if list_item:
        return list_item.list_desc
    else:
        return None

def get_id_by_name(name):
    list_item = ReplyList.query.filter_by(list_name=name).first()
    if list_item:
        return list_item.list_id
    else:
        return None  # or handle it as you prefer
    
def get_available_quantity(item_name):
    list_item = ReplyList.query.filter_by(list_name=item_name).first()
    if list_item:
        return list_item.available_quantity
    else:
        return None  # or handle it as you prefer

def edit_avalable_quantity(item_name,new_quantity):
    list_item = ReplyList.query.filter_by(list_name=item_name).first()
    if list_item:
        # Update the available quantity
        list_item.available_quantity = new_quantity

        # Commit the change to the database
        db.session.commit()
    else:
        return None