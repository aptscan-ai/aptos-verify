import os
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from aptos_verify.config import get_config
import typing
import uvicorn
from aptos_verify.schemas import VerifyArgs
import time
from fastapi.responses import JSONResponse
from aptos_verify.rules.compare_bytecode import logger
import traceback
from aptos_verify.const import VerifyMode

app = FastAPI()
try:
    from dotenv import load_dotenv
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
async def api_verify(request: Request,
                     module: str,
                     rpc: typing.Optional[str] = '',
                     complie_ver: typing.Optional[str] = '',
                     github_repo: typing.Optional[str] = '',
                     local_path: typing.Optional[str] = '',
                     keep: typing.Optional[str] = ''
                     ):
    from aptos_verify.main import start_verify
    kwargs = {
        'module_id': module,

    }
    kwargs['verify_mode'] = VerifyMode.ONCHAIN.value
    if rpc:
        kwargs['aptos_node_url'] = rpc
    if complie_ver:
        kwargs['compile_bytecode_version'] = complie_ver
    if github_repo:
        kwargs['github_repo'] = github_repo
        kwargs['verify_mode'] = VerifyMode.GITHUB.value
    elif local_path:
        kwargs['local_path'] = local_path
        kwargs['verify_mode'] = VerifyMode.LOCAL_PATH.value
    if keep:
        kwargs['keep_build_data'] = True if keep == 'true' else False
        
    logger.debug(f"Params for verify: {kwargs}")

    try:
        params = VerifyArgs(**kwargs)
        rs = await start_verify(params)
        return JSONResponse(content={
            "message": "success" if rs.result else "fail",
            "data": rs.dict()
        }, status_code=200)
    except BaseException as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
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
