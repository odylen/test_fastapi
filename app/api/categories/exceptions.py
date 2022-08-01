from fastapi import HTTPException, status

category_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Category with given id does not exist",
)
