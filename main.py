from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import os
import json
from dotenv import load_dotenv

from apps.error import CustomError, DataReqError
from apps.setting import setting

from scripts.execute import judge_and_order

from configs.objAssets import OBJ_ASSETS

tags_metadata = [
    {
        "name": "Backend Server with Model Embedding",
        "description": "백엔드 모델 임베딩 서버",
    }
]

load_dotenv(verbose=True)

frontServerUrl = os.getenv('FRONT_SERVER_URL')

origins = [
    frontServerUrl,
]

app = FastAPI(
    title="AutoTrading",
    summary="자동 알고리즘 매매 프로그램",
    version="0.0.2",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(CustomError)
def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(
        content={"message": f"{exc.message} in {exc.detail}"},
        status_code=exc.status_code
    )

@app.exception_handler(DataReqError)
def data_requirement_error_handler(request: Request, exc: DataReqError):
    return JSONResponse(
        content={"message": exc.message},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

@app.get('/')
def hello_code():
    return JSONResponse(
        content={"message": "Hello World!"},
        status_code=200,
    )

@app.get('/alarm')
def check_update_and_decide(symbols: str):
    target_symbols = json.loads(symbols)
    if not target_symbols or len(target_symbols) == 0:
        raise DataReqError('symbols')

    judge_and_order(OBJ_ASSETS=OBJ_ASSETS, symbols=target_symbols)

    return JSONResponse(
        content={"message": "success"},
        status_code=200,
    )

app.include_router(setting, prefix='/settings')
