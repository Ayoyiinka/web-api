from flask import jsonify, abort, make_response
from art_alb import app

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(500)
def internal_Server_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)