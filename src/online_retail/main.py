
import os
import pandas as pd
from online_retail.utils.base_funcs import load_data


# if __name__ == "__main__":
path = os.path.dirname(__file__)
file_path = os.path.abspath(
    os.path.join(path, '..','..','data/online_retail_II.xlsx'))
data = load_data(file_path=file_path)
data.head()
data.info()


