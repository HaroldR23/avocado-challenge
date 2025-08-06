class EmptyCommentError(Exception):
    def __init__(self, message: str = "Comment content cannot be empty."):
        self.message = message
        super().__init__(self.message)
