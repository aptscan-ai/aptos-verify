# Aptos Verify

Aptos Verify is a Python library for verifying a module on Aptos Blockchain

## Installation

Before install package, you need to setup Rust, Cargo and Aptos Cli
 

install Rust and Cargo: https://learning-rust.github.io/docs/installation/

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
install Aptos Cli: https://aptos.dev/tools/aptos-cli/install-cli/

```bash
curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install aptos_verify.

```bash
pip install aptos-verify
```
Run with docker by load image from folder docker
```
Option 1 Build docker: 
docker build -t aptos-verify-dk . 

Option 2 Load docker by image: 
docker load -i aptos-verify-dk.tar   

Start container: 
docker run -d -p 9998:9998 aptos-verify-dk
```
## Usage

Use with CLI
``` cli
aptos-verify -m 0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::admin

Result:
**************** Rule: Compare bytecode between published bytecode and published source code onchain *****************
                    Result: True
                    Error Code: 0
                    Message: Verify success
                    Exception Class: 
```
Use with sdk
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
Use with docker and API
```api
http://localhost:9998/verify/<module_address>

Example: 
http://localhost:9998/verify/0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::admin

Result:
{"message":"success","data":[{"title":"Compare bytecode between published bytecode and published source code onchain","message":"Verify success","is_skip":false,"error_code":0,"exeption_name":"","result":true,"traceback":"","error_message":""}]}
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

  <table>
    <thead>
      <tr>
        <th>Error Code</th>
        <th>Message</th>
      </tr>
    </thead>
    <tbody>
        <tr>
            <td>0</td>
            <td>No Errors</td>
        </tr>
        <tr>
            <td>1</td>
            <td>Package Not Found</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Module Not Found</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Module Has No Source Code</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Validation Error</td>
        </tr>
    </tbody>
  </table>
