from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# define or import your error response model
class HttpValidationErrorResponse(BaseModel):
    message: str = Field(..., example="Occur a Validation Error. Please Checking Field Name or Field Type is correct.")
    error: str = Field(..., example="Validation Error")
    detail: list = Field(..., example=[
        {'loc': '(body, field name)', 
         'msg': 'value is not a valid integer',
         'type':'type_error.integer'}])


def init_http_exception_handler(app):
    # override openapi 422 error, swagger UI 的 response model 顯示文字
    import fastapi.openapi.utils as fu
    fu.validation_error_response_definition = HttpValidationErrorResponse.schema()

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, err: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content= HttpValidationErrorResponse(message= "Occur a Validation Error. Please Checking Field Name or Field Type is correct.", 
                                                 error= "Validation Error", 
                                                 detail= err.errors()).json()
        )