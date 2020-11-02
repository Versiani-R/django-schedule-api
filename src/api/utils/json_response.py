def get_json_response(success, data, error):
    return {
        "success": success,
        "data": data,
        "error": error
    }
