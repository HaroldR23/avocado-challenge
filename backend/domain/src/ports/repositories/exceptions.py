class RepositoryException(Exception):
    def __init__(self, message="An error occurred in the repository."):
        self.message = message
        super().__init__(self.message)
