import json
import numpy as np
import pandas as pd

from argparse import ArgumentParser
from collections import Counter

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def count_nums(df: pd.Series, to_numeric=False):
    if to_numeric:
        df = pd.to_numeric(df, errors='coerce')
    num_nan = df.isna().sum()
    return {
        'nums': {
            'total': len(df),
            'valid_data': len(df) - num_nan,
            'nan': num_nan
        }
    }
   
def number_analysis(df: pd.Series):
    rtn = count_nums(df, to_numeric=True)
    
    df = pd.to_numeric(df, errors='coerce').dropna()
    info = dict()
    info['mean'] = np.mean(df)
    info['std'] = np.std(df)
    info['1st_quartile'], info['2nd_quartile'], info['3rd_quartile'] = \
        np.quantile(df, [0.25, 0.5, 0.75])
    
    rtn['info'] = info
    
    return rtn

def choice_analysis(df: pd.Series):
    rtn = count_nums(df)
    rtn['info'] = dict(Counter(df.dropna()))

    return rtn

def analysis_pipe(df, label, dtype):
    if dtype == 'number':
        return number_analysis(df[label])
    elif dtype == 'choice':
        return choice_analysis(df[label])
    else:
        return count_nums(df[label])

def main(args):
    df = pd.read_csv(args.csv_file)
    meta_data = pd.read_csv(args.filter_info, encoding='big5')
    field2type = {field: typ for field, typ in meta_data[['field', 'type']].itertuples(index=False)}

    valid_column = set(df.columns) & field2type.keys()
    info = {label: analysis_pipe(df, label, field2type[label]) for label in valid_column}
    with open(args.output_json, 'w') as f:
        json.dump(info, f, cls=NpEncoder, indent=4)
    
if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--filter_info',
        type=str,
        default='clean_filter.csv'
    )
    parser.add_argument(
        '--csv_file',
        type=str,
        default='release_list_survey.csv'
    )
    parser.add_argument(
        '--output_json',
        type=str,
        default='output.json'
    )
    args = parser.parse_args()
    main(args)
