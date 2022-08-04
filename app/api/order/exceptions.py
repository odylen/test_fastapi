from fastapi import HTTPException, status

product_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Product with given id does not exist",
)
invalid_order_input_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Check request params",
)

invalid_order_cart_input_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Check cart",
)
