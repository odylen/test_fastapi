from fastapi import HTTPException, status

promocode_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Promocode does not exist",
)


invalid_promocode_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid promocode",
)
