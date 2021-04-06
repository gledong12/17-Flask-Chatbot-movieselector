from sqlalchemy  import text

class UserDao:
    def __init__(self, db):
        self.db = db

    def get_user(self, sender_id):
        return self.db.execute(text("""
            SELECT
                id,
                sender_id
            FROM users
            WHERE sender_id = sender_id
            """),{'sender_id' : sender_id}).fetchone()
    
    def create_user(self, sender_id):
        return self.db.execute(text("""
            INSERT INTO users (
                sender_id
            ) VALUES (
                :sender_id
            )
            """), {'sender_id' : sender_id}).lastrowid

    def get_or_create_sender_id(self, sender_id):
        user = self.get_user(sender_id)

        if not user:
            return self.create_user(sender_id)
        
        return user.id
