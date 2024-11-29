from app.databases.db_init import db



class PromptData(db.Model):
    __tablename__ = 'prompt_data'

    prompt_data_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    header_id = db.Column(db.Integer, db.ForeignKey('heading_desc.header_id'))
    attachment_type = db.Column(db.String, nullable=False)
    option_id = db.Column(db.String)
    list_id = db.Column(db.String)
    is_end = db.Column(db.Integer)

    # Relationship with HeadingDesc
    heading_desc = db.relationship('HeadingDesc', backref='prompt_data')


class PromptFlow(db.Model):
    __tablename__ = 'prompt_flow'

    flow_id = db.Column(db.Integer, primary_key=True, nullable=False)
    current_prompt_id = db.Column(db.Integer, db.ForeignKey('prompt_data.prompt_data_id'))
    next_prompt_id = db.Column(db.Integer, db.ForeignKey('prompt_data.prompt_data_id'))
    option_id = db.Column(db.Integer, db.ForeignKey('reply_option.option_id'))
    is_end = db.Column(db.Boolean, default=False)

    # Relationships with Prompt
    current_prompt = db.relationship('PromptData', foreign_keys=[current_prompt_id], backref='current_prompts')
    next_prompt = db.relationship('PromptData', foreign_keys=[next_prompt_id], backref='next_prompts')
    reply_option = db.relationship('ReplyOption', backref='prompt_flows')