from fastapi import HTTPException, status


def _exception(parent_exception: Exception, status_code: int, message: str):
    raise HTTPException(
        status_code=status_code, detail={"message": message}
    ) from parent_exception


def auth_expired(
    e: Exception = None,
    message: str = "Authorization token has expired, please log in again",
):
    e = e or Exception()
    _exception(e, status.HTTP_401_UNAUTHORIZED, message)


def forbidden(e: Exception = None, message: str = "Forbidden"):
    e = e or Exception()
    _exception(e, status.HTTP_403_FORBIDDEN, message)


def unauthorized(e: Exception = None, message: str = "Unauthorized"):
    e = e or Exception()
    _exception(e, status.HTTP_401_UNAUTHORIZED, message)


def not_found(e: Exception = None, message: str = "Not Found"):
    e = e or Exception()
    _exception(e, status.HTTP_404_NOT_FOUND, message)


def bad_request(e: Exception = None, message: str = "Bad Request"):
    e = e or Exception()
    _exception(e, status.HTTP_400_BAD_REQUEST, message)
