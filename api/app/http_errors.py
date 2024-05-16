from fastapi import HTTPException, status

def _exception(parent_exception: Exception, status_code: int, message: str):
    raise HTTPException(status_code=status_code, detail={"message": message}) from parent_exception

def forbidden(e: Exception = None, message: str = "Forbidden"):
    e = e or Exception()
    _exception(e, status.HTTP_403_FORBIDDEN, message)

def unauthorized(message: str = "Unauthorized"):
    e = e or Exception()
    _exception(e, status.HTTP_401_UNAUTHORIZED, message)

def not_found(message: str = "Not Found"):
    e = e or Exception()
    _exception(e, status.HTTP_404_NOT_FOUND, message)
