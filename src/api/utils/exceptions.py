class InvalidException():
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


class InvalidPost(Exception, InvalidException):
    def __init__(self, message, code):
        self.message = message
        self.code = code


class InvalidTokenId(Exception, InvalidException):
    def __init__(self):
        self.message = "Invalid Token Id."
        self.code = 3


class InvalidDay(Exception, InvalidException):
    def __init__(self):
        self.message = "Cannot Schedule a meeting to a saturday or sunday."
        self.code = 4


class InvalidDate(Exception, InvalidException):
    def __init__(self):
        self.message = "Cannot Schedule a meeting to the past."
        self.code = 5


class InvalidTime(Exception, InvalidException):
    def __init__(self):
        self.message = "Number of meetings scheduled to the date and hour is over the allowed number."
        self.code = 6


class InvalidApiCall(Exception, InvalidException):
    def __init__(self):
        self.message = "Number of api calls made in 15 minutes is greater than 15."
        self.code = 7


class InvalidObject(Exception):
    pass