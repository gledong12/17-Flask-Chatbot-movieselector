from sqlalchemy import text

class MessageDao:
    def __init__(self, db):
        self.db = db

    def get_state(self, sender_id):
        sender = self.db.execute(text("""
            SELECT id
            FROM users
            WHERE sender_id = sender_id
            """), {'sender_id' : sender_id}).fetchone()
        
        message = self.db.execute(text("""
            SELECT *
            FROM messages
            WHERE user_id=user_id
            ORDER BY created_at DESC
            LIMIT 1
            """),{ 'user_id' : sender[0]}).fetchone()   # sender[0] sender_id의 id 값
        
        if not message:
            return 'START'
        return message[-1]

    def get_previous_state(self, sender_id):
        sender = self.db.execute(text("""
            SELECT id
            FROM users
            WHERE sender_id = sender_id
            """),{'sender_id' : sender_id}).fetchone()
        
        message = self.db.execute(text("""
            SELECT * 
            FROM messages
            WHERE user_id = user_id
            ORDER BY created_at DESC
            LIMIT 1
            """), {'user_id' : sender[0]}).fetchone()
        
        return message[-2]

    def create_message(self, sender_id, message, state, next_state):
        sender = self.db.execute(text("""
            SELECT id
            FROM users
            WHERE sender_id = sender_id
        """), {'sender_id' : sender_id}).fetchone()
        print('sender3', sender[0])
        
        data = {'text' : message, 'user_id' : sender[0], 'state' : state, 'next_state' : next_state}
        
        print('message', data)
        message = self.db.execute(text("""
            INSERT INTO messages (
                text,
                user_id,
                state,
                next_state
            ) VALUES(
                :text,
                :user_id,
                :state,
                :next_state
            )
        """), data)
        print('message2', message)
        message_id = self.db.execute(text("""
                SELECT id
                FROM messages
                WHERE user_id = user_id
                ORDER BY created_at DESC
                LIMIT 1
            """), {'user_id': sender[0]}).fetchone()[0]
        return message_id

    
        
