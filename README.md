* 資料處理
```
python run.py \
    --csv_file [原始 survey 資料] \
    --output_file [輸出檔名] 
```
* 資料分佈分析
```
python analyze.py \
    --filter_info [filter.csv] \
    --csv_file [要調查的檔案] \
    --output_json [以 .json 的形式輸出]
```
* json file
```
{
    'LABEL_1': {
        'nums': {
            'total': xxxxx,
            'valid_data': xxxxx,
            'nan': xxxxx
        },
        'info': {
            ...
        }
    },
    ...
}
```

    * 'number' data:
    ```
    'info': {
        'mean': xxxxx,
        'std': xxxxx,
        "1st_quartile": xxxxx,
        "2nd_quartile": xxxxx,
        "3rd_quartile": xxxxx
    }
    ```
    * 'choice' data:
    ```
    'info': {
        'cls1': xxxxx,
        'cls2': xxxxx,
        ...
    }
    ```
