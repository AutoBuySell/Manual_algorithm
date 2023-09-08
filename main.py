from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from apps.subapp import sub

from scripts.assets import Equity_Manual_v1
from scripts.judge import getNewPosition_Manual_v1, makeOrders_Manual_v1

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

obj_assets = {}

app.mount('/sub', sub)

@app.get('/')
def hello_code():
    return JSONResponse(
        content={"message": "Hello World!"},
        status_code=200,
    )

@app.get('/check')
def check_update_and_decide(equities: list):
    symbols = []
    orders = []

    for eq in equities:
        if eq not in obj_assets:
            obj_assets[eq] = Equity_Manual_v1(eq)
        if obj_assets[eq].check_data():
            result = getNewPosition_Manual_v1(obj_assets[eq])
            if result[0]:
                symbols.append(eq)
                orders.append('buy')
            elif result[1]:
                symbols.append(eq)
                orders.append('sell')

    makeOrders_Manual_v1(assets=symbols, orders=orders)

    