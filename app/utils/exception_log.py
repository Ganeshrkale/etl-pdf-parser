
from app.logger.log import logger
from flask import jsonify
from .const import HttpStatus
import traceback

class ExceptionLog:
    def ExceptionResponse(e,userName,apiName,fileName):
        construct=dict()
        construct['success'] = False
        construct['error'] = str(e)
        response = jsonify(construct)
        response.status_code = HttpStatus.BAD_REQUEST
        logger.error("Error log", extra={'Type':"Api Controller",'ErrorMessage':traceback.format_exc(),'API': apiName, 'User': userName,'FileName':fileName})
        return response