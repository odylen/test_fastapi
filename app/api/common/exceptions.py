from fastapi import HTTPException, status

token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token Expired",
    headers={"WWW-Authenticate": "Bearer"},
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User does not exist",
)

not_admin_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Admin only",
)

user_already_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already exists",
)
