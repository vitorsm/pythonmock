

class MockFunctionNotFoundException(Exception):
    def __init__(self, function_name: str, args: tuple, kwargs: dict):
        super().__init__(f"parameters not match with a declared function. function_name: {function_name} "
                         f"args: {str(args)} - kwargs: {str(kwargs)}")
