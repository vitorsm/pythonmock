import inspect

from typing import List, Optional, Generic, TypeVar

from pythonmock.instance import Instance
from pythonmock.mock_function import MockFunction
from pythonmock.mock_function_not_found_exception import MockFunctionNotFoundException
from pythonmock.mock_function_parameters import MockFunctionParameters


class WhenMock(object):
    parameter: MockFunction

    def __init__(self, function_name: str):
        self.parameter = MockFunction(function_name)

    def with_arguments(self, *args, **kwargs):
        self.parameter.parameter_matcher = MockFunctionParameters(args, kwargs)
        return self

    def then_return(self, object_to_return):
        self.parameter.object_to_return = object_to_return
        return self

    def then(self, function_to_return: callable):
        self.parameter.function_to_return = function_to_return
        return self

    def set_callback(self, function_callback: callable):
        self.parameter.callback_to_execute = function_callback
        return self

# T = TypeVar('T')


class Mock(object):

    functions: List[MockFunction]
    instance: Optional[Instance]

    def __init__(self):
        self.functions = list()
        self.instance = None

    def get_instance(self):
        self.instance = Instance()

        self.__set_function_to_instance(self.instance)

        return self.instance

    def __set_function_to_instance(self, instance: Instance, index: int = 0):
        if len(self.functions) <= index:
            return

        function = self.functions[index]

        setattr(instance, function.name,
                lambda *args, **kwargs: self.__handle_function_call(function.name, args, kwargs))

        self.__set_function_to_instance(instance, index + 1)

    def when(self, function_name: str):
        when_mock = WhenMock(function_name)
        self.functions.append(when_mock.parameter)
        self.functions = sorted(self.functions, key=lambda function: function.number_of_any_parameters())

        if self.instance:
            setattr(self.instance, function_name,
                    lambda *args, **kwargs: self.__handle_function_call(function_name, args, kwargs))

        return when_mock

    def __handle_function_call(self, function_name: str, args: Optional[tuple], kwargs: Optional[dict]):
        function = next((f for f in self.functions
                         if f.name == function_name and f.is_match(args, kwargs)), None)

        if not function:
            raise MockFunctionNotFoundException(function_name, args, kwargs)

        function.add_call(args, kwargs)

        if function.callback_to_execute:
            function.callback_to_execute(*args, **kwargs)

        if function.function_to_return:
            return function.function_to_return(*args, **kwargs)
        else:
            return function.object_to_return

    def get_call_quantity_by_parameters(self, function_name: str, *args, **kwargs) -> int:
        return len(self.get_calls_by_parameters(function_name, *args, **kwargs))

    def get_call_quantity(self, function_name: str) -> int:
        return len(self.get_calls(function_name))

    def get_calls(self, function_name: str) -> List[MockFunctionParameters]:
        functions = [f for f in self.functions if f.name == function_name]
        result = list()

        for function in functions:
            result.extend(function.calls)

        return result

    def get_calls_by_parameters(self, function_name: str, *args, **kwargs) -> List[MockFunctionParameters]:
        function = next((f for f in self.functions
                         if f.name == function_name and f.is_match(args, kwargs)), None)
        result = list()

        if function:
            result = function.calls

        return result
