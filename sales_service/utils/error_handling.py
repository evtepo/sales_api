from fastapi import status
from fastapi.responses import JSONResponse


def error_response(msg: str, status_code: int = status.HTTP_404_NOT_FOUND):
    return JSONResponse({"msg": msg}, status_code=status_code)
