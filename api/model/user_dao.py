from sqlalchemy  import text

class UserDao:
    def __init__(self, db):
        self.db = db

    def get_or_create_sender_id(self, sender_id):
        sender = self.db.execute(text("""
            SELECT
                id,
                sender_id
            FROM users
            where sender_id = sender_id
        """), {'sender_id' : sender_id}).fetchone()

        if not sender:
            sender = self.db.execute("INSERT INTO users (sender_id) VALUES(%s)", sender_id).lastrowid

        return sender
