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
