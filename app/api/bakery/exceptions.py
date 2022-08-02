from fastapi import HTTPException, status

bakery_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Bakery with given id does not exist",
)
