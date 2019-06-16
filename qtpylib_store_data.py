import logging
from os import listdir
from os.path import isfile, join

import pandas as pd
from qtpylib import workflow as wf

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')


def get_data_from_csv(file_path):
    csv_df = pd.read_csv(file_path, index_col='Date')
    csv_df.index = pd.to_datetime(csv_df.index, format="%Y%m%d")
    csv_df = csv_df.drop(['RIC', 'Adj Close'], axis=1)
    csv_df.columns = ['open', 'high', 'low', 'close', 'volume']
    return csv_df


if __name__ == "__main__":
    my_path = "/home/laikasin93/python/HKDailyStocksQuotes/"
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

    for file in only_files:
        file_path = my_path + file
        logging.info("Sourcing " + file_path)
        stock_code = file.replace('.csv', '')
        df = get_data_from_csv(file_path)

        ibtuple = (stock_code, "STK", "SEHK", "HKD")
        qtpylib_df = wf.prepare_data(ibtuple, data=df, resample="1D")

        # # store data
        wf.store_data(qtpylib_df, kind="BAR")
