from fastapi import FastAPI
from fastapi.responses import JSONResponse

sub = FastAPI()

@sub.get('/')
def aaa():
    return JSONResponse(
        content={"message": "Hello World!"},
        status_code=200,
    )