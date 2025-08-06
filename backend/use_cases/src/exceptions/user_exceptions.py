class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.message = f"User with ID {user_id} not found."
        super().__init__(self.message)
        self.user_id = user_id
