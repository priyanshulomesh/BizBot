from app.databases.db_init import db


class ReplyOption(db.Model):
    __tablename__ = 'reply_option'

    option_id = db.Column(db.Integer, primary_key=True, nullable=False)
    option_desc = db.Column(db.String, nullable=False)

def create_reply_options(option_ids):
    options = ReplyOption.query.filter(ReplyOption.option_id.in_(option_ids.split(','))).all()
    return [{
        "type": "reply",  # Set type to "reply"
        "reply": {
            "id": option.option_id,  # ID for the button
            "title": option.option_desc  # Title for the button
        }
    } for option in options]