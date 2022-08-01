from fastapi import HTTPException, status

product_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Product with given id does not exist",
)
