from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

# define or import your error response model
class HttpValidationErrorResponse(BaseModel):
    message: str = Field(..., example="message to the developer")
    error: str = Field(..., example="Validation Error")
    detail: dict = Field(..., example=[
        {'loc': 'quantity', 
         'msg': 'value is not a valid integer',
         'type':'type_error.integer'}])


def init_http_exception_handler(app):
    # override openapi 422 error, swagger UI 的 response model 顯示文字
    import fastapi.openapi.utils as fu
    fu.validation_error_response_definition = HttpValidationErrorResponse.schema()

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, err: RequestValidationError):
        print(err.errors())
        print(err.body)
        return PlainTextResponse(str(err), status_code=422)