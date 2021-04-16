import pandas as pd
from pandas import ExcelWriter
from platforms import DefaultValues
import traceback


def merge(source_excel_path, results_json_path, field):
    try:
        json_data = pd.read_json(results_json_path, lines=True)
        source_excel = pd.read_excel(source_excel_path, index_col=0)

        results = source_excel.merge(json_data, left_on=field, right_on='url', how='left')

        with ExcelWriter(DefaultValues.merge_path) as writer:
            results.to_excel(writer)
    except:
        traceback.print_exc()