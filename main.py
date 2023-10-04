from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import json

from scripts.requests import req_data_realtime
from scripts.assets import Equity_Manual_v1
from scripts.judge import getNewPosition_Manual_v1, makeOrders_Manual_v1
from scripts.log import get_order_log, update_order_log

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

@app.get('/')
def hello_code():
    return JSONResponse(
        content={"message": "Hello World!"},
        status_code=200,
    )

@app.get('/alarm')
def check_update_and_decide(symbols: str):
    target_symbols = json.loads(symbols)

    req_data_realtime(target_symbols)

    orders = ([], [])

    for symbol in target_symbols:
        if symbol not in OBJ_ASSETS:
            OBJ_ASSETS[symbol] = Equity_Manual_v1(symbol)

        obj_symbol = OBJ_ASSETS[symbol]
        if obj_symbol.check_data():
            result = getNewPosition_Manual_v1(obj_symbol)
            if result[0]:
                orders[0].append(symbol)
                orders[1].append('buy')
            elif result[1]:
                orders[0].append(symbol)
                orders[1].append('sell')

    makeOrders_Manual_v1(orders=orders, obj_assets=OBJ_ASSETS)

    return JSONResponse(
        content={"message": "success"},
        status_code=200,
    )

@app.get('/logs')
def get_logs():
    logs = get_logs()

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
    logs = get_logs()

    return JSONResponse(
        content={
            "message": "success",
            "data": logs,
        },
        status_code=200,
    )
