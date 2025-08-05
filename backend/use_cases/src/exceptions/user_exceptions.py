class UserNotFoundError(Exception):
	def __init__(self, user_id: int):
		super().__init__(f"User with ID {user_id} not found.")
		self.user_id = user_id
