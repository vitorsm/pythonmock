from pythonmock.any_parameter import AnyParameter


class MockFunctionParameters(object):
    args: tuple
    kwargs: dict

    def __init__(self, args: tuple, kwargs: dict):
        self.args = args
        self.kwargs = kwargs

    def is_match(self, args, kwargs) -> bool:
        return self.__check_args(args) and self.__check_kwargs(kwargs)

    def __check_args(self, args: tuple) -> bool:
        if not isinstance(args, type(self.args)):
            return False

        if args is not None:
            if len(args) != len(self.args):
                return False

            for index, arg in enumerate(args):
                if isinstance(self.args[index], AnyParameter):
                    continue

                if arg != self.args[index]:
                    return False

        return True

    def __check_kwargs(self, kwargs: dict) -> bool:
        if not isinstance(kwargs, type(self.kwargs)):
            return False

        if kwargs is not None:
            kwargs_keys = set(kwargs.keys())
            original_keys = set(self.kwargs.keys())

            if kwargs_keys != original_keys:
                return False

            for parameter_name, parameter_value in kwargs:
                if isinstance(self.kwargs.get(parameter_name), AnyParameter):
                    continue

                if parameter_value != self.kwargs.get(parameter_name):
                    return False

        return True
