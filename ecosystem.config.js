module.exports = {
    apps: [
        {
            'name': 'aptoscan-verify-api',
            'script': './server.py',
            'error_file': './log/webservice_err.log',
            'out_file': './log/webservice_err.log',
            'interpreter': './aptos-verify-venv/bin/python3'
        }
    ]
}