from app.databases.db_init import db
from app.databases.reply_list import ReplyList
from app.databases.menu_reply_association import MenuReplyAssociation

class Menu(db.Model):
    __tablename__ = 'menu'

    menu_id = db.Column(db.Integer, primary_key=True, nullable=False)
    menu_name = db.Column(db.String, nullable=False)
    menu_desc = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=False, nullable=False)

    reply_lists = db.relationship('MenuReplyAssociation', backref='menu', lazy='dynamic')

    @staticmethod
    def set_active(menu_id):
        """Set only one menu row as active, and the rest as inactive."""
        
        # Deactivate all rows
        Menu.query.update({Menu.active: False})
        
        # Activate the specified row
        menu = Menu.query.get(menu_id)
        if menu:
            menu.active = True
            db.session.commit()
    
    @staticmethod
    def add_menu(name, desc, active=False):
        """Add a new menu entry. If active=True, deactivate all other menus first."""
        
        # If setting the new menu as active, deactivate others
        if active:
            Menu.query.update({Menu.active: False})
        
        # Create the new menu
        new_menu = Menu(menu_name=name, menu_desc=desc, active=active)
        db.session.add(new_menu)
        db.session.commit()
        
        return new_menu

    @staticmethod
    def add_item_to_menu(reply_list_id, menu_id):
        """Associate a ReplyList item with a Menu item by their IDs."""
        
        menu = Menu.query.get(menu_id)
        reply_list = ReplyList.query.get(reply_list_id)
        
        if menu and reply_list:
            # Only add the association if it doesn't already exist
            if reply_list not in menu.reply_lists:
                menu.reply_lists.append(reply_list)
                db.session.commit()
                return {"message": "Reply list successfully added to menu"}
            else:
                return {"message": "Reply list is already associated with the menu"}
        else:
            return {"message": "Menu or ReplyList not found"}

def fetch_active_menu_id():
    return Menu.query.filter(Menu.active.is_(True)).first().menu_id()
