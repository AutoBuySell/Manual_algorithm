**You should follow the [project instruction](https://github.com/AutoBuySell) first to have a fully working service**

## Installation
1. Make a Conda environment
    1. Conda installation docs: https://conda.io/docs/user-guide/install/
    2. Conda env creation docs: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands
        1. `conda create -n myenv python=3.10.12`
    3. Use python version 3.10.12 (recommendation)
2. Clone this repository
    1. `git clone https://github.com/AutoBuySell/Backend_server.git`
3. Move into the cloned folder
4. Install library requirements
    1. `pip install -r requirements.txt`
5. Set .env file
```shell
ALPACA_PAPER_BASEURL=https://paper-api.alpaca.markets/v2
ALPACA_PAPER_KEY=XXXXXXXXXXXXXX <= enter your key from Alpaca
ALPACA_PAPER_KEY_SECRET=XXXXXXXXXXXXXXXXXXXX <= enter your key secret

ALPACA_HISTORY_DATA_URL=https://data.alpaca.markets/v2

DATA_SERVER_URL=http://localhost:8000

PATH_MARKET_DATA=../data/market_data/
PATH_SETTING_DATA=../data/setting_data/
PATH_DEFAULT_SETTING=configs/default_settings.json
```
6. Start server with reload option and port number 8001
    1. `uvicorn main:app --reload --port 8001`
    2. You should change env values if you want to change the port numbers
