from copy import deepcopy
from typing import List, Optional

from tests.fake_class.user_not_found_exception import UserNotFoundException
from tests.fake_class.user_repository import UserRepository


class UserService(object):

    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_new_user(self, name: str):
        user = self.user_repository.instantiate_new_user()
        user.update({"name": name})

        self.user_repository.create_user(user)

    def find_user_permissions_by_user_id(self, user_id: int) -> Optional[List[str]]:
        user = self.user_repository.find_user_by_id(user_id)

        if not user:
            raise UserNotFoundException(user_id)

        return user.get("permissions")

    def set_user_name(self, user_id: int, user_name: str):
        user = self.user_repository.find_user_by_id(user_id)

        if not user:
            raise UserNotFoundException(user_id)

        user.update({"status": "processing"})
        self.user_repository.update_user(user)

        user = deepcopy(user)
        user.update({"name": user_name, "status": "processed"})
        self.user_repository.update_user(user)
