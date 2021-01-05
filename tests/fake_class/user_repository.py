import abc


class UserRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_user_by_id(self, _id: int) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def create_user(self, user: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def update_user(self, user: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def instantiate_new_user(self) -> dict:
        raise NotImplementedError
