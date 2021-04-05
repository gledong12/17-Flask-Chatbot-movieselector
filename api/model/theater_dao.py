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
        print('cgvs',cgvs)
        
        if not cgvs:
            return 'RANK'
        return cgvs


    def get_cgv_code(self, message):
        cgv = self.db.execute(text("""
            SELECT *
            FROM cgv
            WHERE name = name
            """), {'name' : message}).fetchall()
        
        for i in cgv:
            if message == i[1]:
                return i[2]
                print('cgv3', i[2])

