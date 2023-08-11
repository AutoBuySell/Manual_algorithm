from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Embedding Model",
        "description": "모델 관련 API",
    }
]

origins = [
    "*",
]

app = FastAPI(
    title="AutoTrading",
    summary="자동화 알고리즘입니다.",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def hello_code():
    return JSONResponse(
        content={"message": "Hello World!"},
        status_code=200,
    )
