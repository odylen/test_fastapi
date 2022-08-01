from pydantic import BaseModel


class RequestStatus(BaseModel):
    success: bool = True
