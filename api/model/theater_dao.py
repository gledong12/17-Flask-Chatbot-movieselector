from sqlalchemy  import text

class TheaterDao:
    def __init__(self, db):
        self.db = db

    def get_cgv_list(self, message):
        print('cgvmessage', message)
        cgvs = self.db.execute(text("""
            SELECT *
            FROM cgv
            WHERE name = name
        """), {'name' : message}).fetchone()[0]

        return cgvs
       
    def get_cgv_code(self, message):
        cgv =self.db.execute(text("""
            SELECT *
            FROM cgv
            WHERE name = name
            """), {'name' : message}).fetchall()

        return cgv



