from fastapi import HTTPException, status

sending_sms_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Error while sending sms",
)

code_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Code with given id does not exist",
)

incorrect_code_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect sms code",
)


code_not_confirmed_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Code not confirmed",
)
code_expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Code Expired",
)
