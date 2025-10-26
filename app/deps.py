from fastapi import Depends, Request
from typing import Annotated, cast

def token_secret(request: Request) -> str:
    return cast(str, request.app.state.token_secret)

Token = Annotated[str, Depends(token_secret)]
