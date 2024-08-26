import pytz

class HttpStatus:
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    BAD_REQUEST = 400

class TimeZone:
    IST = pytz.timezone('Asia/Kolkata')