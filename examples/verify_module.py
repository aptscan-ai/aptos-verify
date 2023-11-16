from aptos_verify.main import start_verify
from aptos_verify.schemas import CliArgs, Params
import asyncio


async def main():
    print('Start verify module: 0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::admin')
    rs = await start_verify(
        CliArgs(
            module_id='0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::admin',
            # You can pass rpc node, log level...
            params=Params(
                aptos_node_url='https://fullnode.mainnet.aptoslabs.com',
                move_build_path='/'
            )
        )
    )
    print('Result:')
    print(rs)

if __name__ == "__main__":
    asyncio.run(main())
