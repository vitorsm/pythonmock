from typing import List, Optional, Generic, TypeVar

from pythonmock.mock_function import MockFunction
from pythonmock.mock_function_not_found_exception import MockFunctionParameterNotFound
from pythonmock.mock_function_parameters import MockFunctionParameters


class WhenMock(object):
    parameter: MockFunction

    def __init__(self, function_name: str):
        self.parameter = MockFunction()
        self.parameter.name = function_name

    def with_arguments(self, *args, **kwargs):
        self.parameter.parameter_matcher = MockFunctionParameters(args, kwargs)
        return self

    def then_return(self, object_to_return):
        self.parameter.object_to_return = object_to_return


T = TypeVar('T')


class Mock(Generic[T]):

    functions: List[MockFunction]

    def __init__(self):
        self.functions = list()

    def get_instance(self) -> T:
        instance = T()
        instance.generated_mock = self

        for function in self.functions:
            setattr(instance, function.name,
                    lambda *args, **kwargs: self.__handle_function_call(function.name, args, kwargs))

        return instance

    def when(self, function_name: str):
        when_mock = WhenMock(function_name)
        self.functions.append(when_mock.parameter)
        setattr(self, function_name, lambda *args, **kwargs: self.__handle_function_call(function_name, args, kwargs))
        return when_mock

    def __handle_function_call(self, function_name: str, args: Optional[tuple], kwargs: Optional[dict]):
        function = next((f for f in self.functions
                         if f.name == function_name and f.parameter_matcher.is_match(args, kwargs)), None)

        if not function:
            raise MockFunctionParameterNotFound(function_name, args, kwargs)

        function.add_call(args, kwargs)

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
                         if f.name == function_name and f.parameter_matcher.is_match(args, kwargs)), None)
        result = list()

        if function:
            result = function.calls

        return result
