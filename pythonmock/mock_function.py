from typing import List, Optional

from pythonmock.mock_function_parameters import MockFunctionParameters


class MockFunction(object):
    id: int
    name: str
    parameter_matcher: Optional[MockFunctionParameters]
    object_to_return: object
    calls: List[MockFunctionParameters]
    function_to_return: Optional[callable]
    callback_to_execute: Optional[callable]

    __id_counter = 0

    def __init__(self, name: str):
        MockFunction.__id_counter += 1

        self.id = MockFunction.__id_counter
        self.calls = list()
        self.name = name
        self.parameter_matcher = None
        self.object_to_return = None
        self.function_to_return = None
        self.callback_to_execute = None

    def add_call(self, args: Optional[tuple], kwargs: Optional[dict]):
        self.calls.append(MockFunctionParameters(args, kwargs))

    def number_of_any_parameters(self) -> int:
        return self.parameter_matcher.number_of_any_parameters() if self.parameter_matcher else 0

    def is_match(self, args: tuple, kwargs: dict) -> bool:
        if not args and not kwargs and not self.parameter_matcher:
            return True

        if not self.parameter_matcher:
            return False

        return self.parameter_matcher.is_match(args, kwargs)
