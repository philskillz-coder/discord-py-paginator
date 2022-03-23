class BetterException(Exception):
    def __init__(self, message: str):
        self.message = message

class ButtonException(BetterException):
    pass

class ButtonFailed(ButtonException):
    pass

class NotAuthor(ButtonException):
    pass
