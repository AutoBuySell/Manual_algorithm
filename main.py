from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body

import json

from apps.error import CustomError, DataReqError

from scripts.core_algos.assets import Equity_Manual_v1, get_default_settings
from scripts.log import get_order_log, update_order_log
from scripts.execute import judge_and_order

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
    summary="자동 알고리즘 매매 프로그램",
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

OBJ_ASSETS = {}

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

@app.get('/logs')
def get_logs():
    logs = get_order_log()

    return JSONResponse(
        content={
            "message": "success",
            "data": logs,
        },
        status_code=200,
    )

@app.put('/logs')
def update_logs():
    update_order_log()
    logs = get_order_log()

    return JSONResponse(
        content={
            "message": "success",
            "data": logs,
        },
        status_code=200,
    )

@app.get('/settings')
def get_setting_lists():
    settings = get_default_settings()

    return JSONResponse(
        content={
            "message": "success",
            "data": settings,
        },
        status_code=200,
    )

@app.get('/settings/{symbol}')
def get_setting_values(symbol: str):
    if symbol not in OBJ_ASSETS:
        OBJ_ASSETS[symbol] = Equity_Manual_v1(symbol)
    asset = OBJ_ASSETS[symbol]

    return JSONResponse(
        content={
            "message": "success",
            "data": asset.settings,
        },
        status_code=200,
    )

@app.put('/settings/{symbol}')
def set_setting_values(symbol: str, args: object = Body(embed=True)):
    if len(args.keys()) == 0:
        raise DataReqError('args')

    if symbol not in OBJ_ASSETS:
        OBJ_ASSETS[symbol] = Equity_Manual_v1(symbol)
    asset = OBJ_ASSETS[symbol]

    asset.set(**args)

    return JSONResponse(
        content={
            "message": "success",
            "data": asset.settings,
        },
        status_code=200,
    )
