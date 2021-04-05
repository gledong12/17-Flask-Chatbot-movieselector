class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao


    def get_or_create_sender_id(self, sender_id):
        return self.user_dao.get_or_create_sender_id(sender_id)
