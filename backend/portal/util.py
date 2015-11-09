from flask import jsonify

def createErrorResponse(status, e, errorCode):
        response = jsonify({
            'errors': True,
            'status': status,
            'message': str(e)
        })
        response.status_code = errorCode
        return response