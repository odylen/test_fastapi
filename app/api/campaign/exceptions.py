from fastapi import HTTPException, status

campaign_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Campaign with given id does not exist",
)
