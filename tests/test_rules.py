import pytest

import aptos_verify.utils as utils
from aptos_verify.schemas import VerifyArgs


@pytest.mark.asyncio
async def test_compare_bytecode():
    from aptos_verify.rules.compare_bytecode import process_compare_bycode
    params = VerifyArgs(
        module_id='0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::admin',
    )
    rs = await process_compare_bycode(
        args=params
    )

    from pprint import pprint
    import json
    pprint(json.loads(rs.json()))

    assert rs == True
