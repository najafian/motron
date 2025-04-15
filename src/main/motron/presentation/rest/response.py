from flask import jsonify, make_response

class ResponseEntity:
    @staticmethod
    def ok(body=None, headers=None):
        return make_response(jsonify(body), 200, headers or {})

    @staticmethod
    def created(body=None, headers=None):
        return make_response(jsonify(body), 201, headers or {})

    @staticmethod
    def bad_request(body=None):
        return make_response(jsonify(body), 400)

    @staticmethod
    def error(message, code=500):
        return make_response(jsonify({"error": message}), code)
