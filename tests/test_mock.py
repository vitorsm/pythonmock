import unittest

from pythonmock.any_parameter import AnyParameter
from pythonmock.mock import Mock
from pythonmock.mock_function_not_found_exception import MockFunctionNotFoundException
from tests.fake_class.user_not_found_exception import UserNotFoundException
from tests.fake_class.user_repository import UserRepository
from tests.fake_class.user_service import UserService


class MockTest(unittest.TestCase):

    def setUp(self):
        user1 = {
            "id": 1,
            "name": "User 1",
            "permissions": [1, 2, 3, 4]
        }

        self.mock_user_repository = Mock()
        self.mock_user_repository.when('find_user_by_id').with_arguments(1).then_return(user1)
        self.mock_user_repository.when('find_user_by_id').with_arguments(2).then_return(None)

        self.mock_user_repository.when('update_user').with_arguments(None)
        self.mock_user_repository.when('update_user')
        self.mock_user_repository.when('update_user').with_arguments(AnyParameter())

        self.mock_user_repository.when('instantiate_new_user').then_return(dict())

        self.user_service = UserService(self.mock_user_repository.get_instance())

    def test_mock_find_user(self):
        permissions = self.user_service.find_user_permissions_by_user_id(1)
        self.assertEqual([1, 2, 3, 4], permissions)

    def test_mock_undeclared_function(self):
        permissions = self.user_service.find_user_permissions_by_user_id(1)

        self.assertEqual([1, 2, 3, 4], permissions)
        self.assertEqual(0, self.mock_user_repository.get_call_quantity('update_user_test'))
        self.assertEqual(0, self.mock_user_repository.get_call_quantity_by_parameters('update_user_test'))

    def test_mock_find_user_exception(self):
        with self.assertRaises(UserNotFoundException):
            self.user_service.find_user_permissions_by_user_id(2)

    def test_mock_find_user_argument_match(self):
        with self.assertRaises(MockFunctionNotFoundException):
            self.user_service.find_user_permissions_by_user_id(10)

    def test_call_quantity(self):
        self.user_service.set_user_name(1, "new_name")

        self.assertEqual(2, self.mock_user_repository.get_call_quantity('update_user'))

    def test_call_quantity_with_different_parameters(self):

        user3 = {
            "id": 3,
            "name": "User 3",
            "permissions": [1, 2]
        }

        self.mock_user_repository.when('update_user').with_arguments(user3)
        self.mock_user_repository.when('find_user_by_id').with_arguments(3).then_return(user3)

        self.user_service.set_user_name(3, "new_name")

        self.mock_user_repository.get_call_quantity_by_parameters('update_user', user3)
        self.assertEqual(1, self.mock_user_repository.get_call_quantity_by_parameters('update_user', user3))
        self.assertEqual(2, self.mock_user_repository.get_call_quantity('update_user'))

    def test_then_callback_function(self):

        user4 = {
            "id": 4,
            "name": "User 4",
            "permissions": [1]
        }

        def find_user(user_id: int):
            self.assertEqual(4, user_id)
            return user4

        self.mock_user_repository.when('find_user_by_id').with_arguments(4).then(find_user)

        self.user_service.set_user_name(4, "new name")

        self.assertEqual(1, self.mock_user_repository.get_call_quantity('find_user_by_id'))

    def test_function_without_parameters(self):

        users_to_save = []

        def save_callback(user: dict):
            users_to_save.append(user)

        self.mock_user_repository.when('create_user').with_arguments(AnyParameter()).set_callback(save_callback)

        self.user_service.create_new_user("Test")

        self.assertEqual(1, self.mock_user_repository.get_call_quantity('instantiate_new_user'))
        self.assertEqual(1, len(users_to_save))
        self.assertEqual("Test", users_to_save[0].get("name"))
