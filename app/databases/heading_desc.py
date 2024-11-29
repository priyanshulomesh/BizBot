from app.databases.db_init import db



class HeadingDesc(db.Model):
    __tablename__ = 'heading_desc'

    header_id = db.Column(db.Integer, primary_key=True, nullable=False)
    desc = db.Column(db.String, nullable=False)