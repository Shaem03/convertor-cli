# Currency Convertor
This is a currency convertor which we are fetching with 'forex-python' package. 
our project act as two part one is to run an Endpoint and
Other is to run CLI commands

### Installation
    # Activate the environment

    pip install -r requirements.txt

### Run Endpoint

    python application.py

### Run CLI commands

    ./convert_cli.py --file input.json --target-currency EUR --chunk-size 100000

```Note: Chunk Size is optional```