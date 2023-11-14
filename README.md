# Aptos Verify

Aptos Verify is a Python library for verifying a module on Aptos Blockchain

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install aptos_verify.

```bash
pip install aptos_verify
```

## Usage

```python
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
                aptos_node_url='https://fullnode.devnet.aptoslabs.com'
            )
        )
    )
    print('Result:')
    print(rs)
if __name__ == "__main__":
    asyncio.run(main())
```
You can use cli to verify module
``` cli
aptos-verify -m 0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::admin
```

Run tests
``` cli
pytest -s
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Error Code
List error codes  that returned from tool
```
1: Package Not Found
2: Module Not Found
3: Module Has No Source Code
```

