class _InvalidException():
    """
    Invalid Exception is the mother class of all exceptions related to this api.
    """
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def display_invalid_exception(self):
        return {
            "success": "false",
            "data": {},
            "error": {
                "code": self.code,
                "message": self.message
            }
        }


class InvalidPost(Exception, _InvalidException):
    def __init__(self, message, code):
        self.message = message
        self.code = code


class InvalidTokenId(Exception, _InvalidException):
    def __init__(self):
        self.message = "Invalid Token Id."
        self.code = 3


class InvalidDay(Exception, _InvalidException):
    def __init__(self):
        self.message = "Cannot Schedule a meeting to a saturday or sunday."
        self.code = 4


class InvalidDate(Exception, _InvalidException):
    def __init__(self):
        self.message = "Cannot Schedule a meeting to the past."
        self.code = 5


class InvalidTime(Exception, _InvalidException):
    def __init__(self):
        self.message = "Number of meetings scheduled to the date and hour is over the allowed number."
        self.code = 6


class InvalidApiCall(Exception, _InvalidException):
    def __init__(self):
        self.message = "Number of api calls is equal to 0. In order to keep using the api, you must buy more api calls."
        self.code = 7


class InvalidError(Exception, _InvalidException):
    def __init__(self):
        self.message = "Unknown error."
        self.code = 0


class InvalidObject(Exception):
    pass