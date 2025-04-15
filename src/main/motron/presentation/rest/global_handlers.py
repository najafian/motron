# motron/web/errors/global_handlers.py

from flask import jsonify
from werkzeug.exceptions import HTTPException

from motron.presentation.rest.exception_handler import ControllerAdvice, ExceptionHandler


@ControllerAdvice
class GlobalErrorHandler:

    @ExceptionHandler(ValueError)
    def handle_value_error(self):
        return jsonify({"error": str(self)}), 400

    @ExceptionHandler(HTTPException)
    def handle_http_error(self):
        return jsonify({"error": self.description}), self.code
