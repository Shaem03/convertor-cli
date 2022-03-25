import argparse
import pandas as pd
import requests

URL = "http://127.0.0.1:5001/get_convert_rate"


def find_rates(df, rates):
    df["currency_rate"] = df["currency"].map(rates)
    df["converted"] = df["value"] * df["currency_rate"]
    df.reset_index(inplace=True, drop=True)
    return df


def read_json(file_path, target_currency, chunk_size):
    rates = get_convert_rates(target_currency)
    result = []
    if rates:
        try:
            for chunk in pd.read_json(file_path, chunksize=chunk_size, lines=True):
                result.append(find_rates(chunk, rates))
        except:
            print("JSON is malformed")
    else:
        return None

    result_df = pd.concat(result)
    output_df = pd.DataFrame()
    output_df["value"] = result_df["converted"]
    output_df["currency"] = target_currency
    output_json = output_df.to_json(orient='records', lines=True)
    print(output_json)


def get_convert_rates(target_currency):
    data = {
        'convertTo': str(target_currency)
    }

    # sending post request and saving response as response object
    r = requests.post(url=URL, json=data)
    if r.ok:
        return r.json()
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Currency Convertor')
    parser.add_argument('-f', '--file', help='Input file path', required=True)
    parser.add_argument('-t', '--target-currency', help='Convertor Target', required=True)
    parser.add_argument('-c', '--chunk-size', help='Chunk Size', type=int, required=False, default=1)
    args = vars(parser.parse_args())
    read_json(args["file"], args["target_currency"], args["chunk_size"])
