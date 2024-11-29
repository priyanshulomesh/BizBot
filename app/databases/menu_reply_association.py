from app.databases.db_init import db

class MenuReplyAssociation(db.Model):
    __tablename__ = 'menu_reply_association'

    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), primary_key=True)
    reply_list_id = db.Column(db.Integer, db.ForeignKey('reply_list.list_id'), primary_key=True)

    # Define relationships to both Menu and ReplyList
    # menu = db.relationship('Menu', backref='menu', lazy=True)
    # reply_list = db.relationship('ReplyList', backref='reply_list',lazy=True)