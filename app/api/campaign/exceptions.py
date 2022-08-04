from fastapi import HTTPException, status

order_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Order with given id does not exist",
)


order_forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not enough rights",
)
