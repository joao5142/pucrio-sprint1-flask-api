from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """ Error response schema for API endpoints
    """
    message: str
