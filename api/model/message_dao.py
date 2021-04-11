from sqlalchemy import text
from .user_dao import UserDao

class MessageDao:
    def __init__(self, db, user_dao):
        self.db = db
        self.user_dao = user_dao


    def get_state(self, sender_id):
        return self.db.execute(text("""
            SELECT * 
            FROM messages m
            JOIN users u ON u.id = m.user_id
            WHERE u.sender_id = sender_id
            ORDER BY m.created_at DESC
            LIMIT 1
            """),{ 'user_id' : sender_id}).fetchone()   # sender[0] sender_id의 id 값
        
    def get_message(self, sender_id):
        return self.db.execute(text("""
            SELECT *
            FROM messages m
            JOIN users u ON u.id = m.user_id
            WHERE u.sender_id = sender_id
            """),{'sender_id' : sender_id}).fetchone()
    
    def create_message(self, sender_id, message, current_state, next_state):
        user = self.user_dao.get_user(sender_id)
        
        data = {'text' : message, 'user_id' : user[0], 'current_state' : current_state, 'next_state' : next_state}
        
        print('data', data)
        message = self.db.execute(text("""
            INSERT INTO messages (
                text,
                user_id,
                current_state,
                next_state
            ) VALUES(
                :text,
                :user_id,
                :current_state,
                :next_state
            )
        """), data)
        
        messages = self.get_message(sender_id)
        return messages.id
