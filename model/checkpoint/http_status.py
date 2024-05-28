from enum import Enum


class HttpStatus(Enum):
    ok = 200
    created = 201
    redirect_ok = 301
    wrong_payload = 400
    without_auth = 401
    refuse_handle = 403
    not_found = 404
    timeout = 408
    exception = 500
    overload = 503