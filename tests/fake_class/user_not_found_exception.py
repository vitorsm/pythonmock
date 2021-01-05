

class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"The user #{user_id} not found")
