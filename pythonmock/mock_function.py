from typing import List, Optional

from pythonmock.mock_function_parameters import MockFunctionParameters


class MockFunction(object):
    id: int
    name: str
    parameter_matcher: MockFunctionParameters
    object_to_return: object
    calls: List[MockFunctionParameters]

    __id_counter = 0

    def __init__(self):
        MockFunction.__id_counter += 1

        self.id = MockFunction.__id_counter
        self.calls = list()
        self.name = None
        self.parameter_matcher = None
        self.object_to_return = None

    def __eq__(self, other):
        return isinstance(other, MockFunction) and other.id == self.id

    def __hash__(self):
        return hash(self.id)

    def add_call(self, args: Optional[tuple], kwargs: Optional[dict]):
        self.calls.append(MockFunctionParameters(args, kwargs))
