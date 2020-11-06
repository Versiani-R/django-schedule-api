class InvalidPost(Exception):
    def __init__(self, message, code):
        self.code = code
        self.message = message

    def format_invalid_post(self):
        return {
            "success": "false",
            "data": {},
            "error": {
                "code": self.code,
                "message": self.message
            }
        }


class InvalidTokenId(Exception):
    def format_invalid_token_id(self):
        return {
            "success": "false",
            "data": {},
            "error": {
                "code": 3,
                "message": "Invalid Token Id."
            }
        }
    

class InvalidApiCall(Exception):
    def format_invalid_api_call(self):
        return {
                "success": "false",
                "data": {},
                "error": {
                    "code": 7,
                    "message": "Number of api calls made in 15 minutes is greater than 15."
                }
            }


class InvalidDay(Exception):
    def format_invalid_day(self):
        return {
            "success": "false",
            "data": {},
            "error": {
                "code": 4,
                "message": "Cannot Schedule a meeting to a saturday or sunday."
            }
        }


class InvalidDate(Exception):
    def format_invalid_date(self):
        return {
            "success": "false",
            "data": {},
            "error": {
                "code": 5,
                "message": "Cannot Schedule a meeting to the past."
            }
        }


class InvalidTime(Exception):
    def format_invalid_time(self):
        return {
            "success": "false",
            "data": {},
            "error": {
                "code": 6,
                "message": "Number of meetings scheduled to the date and hour is over the allowed number."
            }
        }


class InvalidObject(Exception):
    def format_invalid_object(self):
        return {
            "success": "false",
            "data": {},
            "error": {
                "code": 6,
                "message": "Number of meetings scheduled to the date and hour is over the allowed number."
            }
        }
