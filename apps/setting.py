from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from apps.error import DataReqError

from scripts.core_algos.assets import Equity_Manual_v2, get_default_settings

from configs.objAssets import OBJ_ASSETS

setting = FastAPI()

@setting.get('/')
def get_setting_lists():
    settings = get_default_settings()

    return JSONResponse(
        content={
            "message": "success",
            "data": settings,
        },
        status_code=200,
    )

@setting.get('/{symbol}')
def get_setting_values(symbol: str):
    if symbol not in OBJ_ASSETS:
        OBJ_ASSETS[symbol] = Equity_Manual_v2(symbol)
    asset = OBJ_ASSETS[symbol]

    return JSONResponse(
        content={
            "message": "success",
            "data": asset.settings,
        },
        status_code=200,
    )

@setting.put('/{symbol}')
def set_setting_values(symbol: str, args: dict = Body(embed=True)):
    if len(args.keys()) == 0:
        raise DataReqError('args')

    if symbol not in OBJ_ASSETS:
        OBJ_ASSETS[symbol] = Equity_Manual_v2(symbol)
    asset = OBJ_ASSETS[symbol]

    asset.set(**args)

    return JSONResponse(
        content={
            "message": "success",
            "data": asset.settings,
        },
        status_code=200,
    )
