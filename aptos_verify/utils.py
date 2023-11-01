from aptos_verify.config import Config
from pydantic import validate_call, Field
from typing import Annotated
from aptos_sdk.async_client import RestClient
import httpx


async def aptos_rest_client(**options):
    """
    Init rest client instance that will be used to work with RPC API
    Docs: https://pypi.org/project/aptos-sdk/
    """
    return RestClient(
        base_url=Config.APTOS_NODE_URL.value,
        **options
    )
