class ViewException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class BetterException(ViewException):
    pass


class ButtonException(BetterException):
    pass


class ButtonFailed(ButtonException):
    pass


class NotAuthor(ButtonException):
    pass


class SelectException(ViewException):
    pass


class SelectFailed(SelectException):
    pass
