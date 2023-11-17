from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from aptos_verify.config import get_config
import typing
import uvicorn
from aptos_verify.schemas import CliArgs, Params
import time
from fastapi.responses import JSONResponse
from aptos_verify.rules.compare_bytecode import logger
app = FastAPI()
try:
    load_dotenv(dotenv_path='.env')
except BaseException as e:
    pass


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_middleware_here(request: Request, call_next):
    try:
        response = await call_next(request)
        if (response.status_code == 404):
            return JSONResponse(content={
                "message": "fail",
                "error": '404 Not Found',
            }, status_code=404)
        return response
    except BaseException as e:
        return JSONResponse(content={
            "message": "fail",
            "error": str(e),
        }, status_code=400)


@app.get('/verify/{module}')
async def api_verify(request: Request, module: str, rpc: typing.Optional[str] = '', complie_ver: typing.Optional[str] = ''):
    from aptos_verify.main import start_verify
    kwargs = {}
    params = Params(**kwargs)
    if rpc:
        kwargs['aptos_node_url'] = rpc
    if complie_ver:
        kwargs['compile_bytecode_version'] = complie_ver
    try:
        params = Params(**kwargs)
        rs = await start_verify(CliArgs(
            module_id=module,
            params=params
        ))
        return JSONResponse(content={
            "message": "success",
            "data": [dict(k)for k in rs]
        }, status_code=200)
    except BaseException as e:
        return JSONResponse(content={
            "message": "fail",
            "error": str(e)
        }, status_code=400)


def create_server():
    config = get_config()
    port = int(os.getenv('HTTP_PORT') or 0) or config.default_http_port
    host = (os.getenv('HTTP_HOST') or '0.0.0.0') or config.default_http_host

    uvicorn.run(app, host=host,
                port=port)


if __name__ == '__main__':
    create_server()
