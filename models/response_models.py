from pydantic import BaseModel


class captcha_response(BaseModel):
    status: str
    res: str



