import numpy as np
import pandas as pd

from argparse import ArgumentParser

DRK_AMT_LABEL = [
    f'DRK_CURR_{i}_{j}' for i in 'ABC' 
                        for j in ['FREQ', 'TIMES', 'DOSAGE', 'UNIT']
]
SMK_2ND_PLACES_HR = [
    'SMK_2ND_PLACE1_HR',
    'SMK_2ND_PLACE2_HR',
    'SMK_2ND_PLACE3_HR',
    'SMK_2ND_PLACE4_HR'
]
SPO_HABIT_LABEL = [
    f'SPO_HABBIT_{i}_{j}' for i in 'ABC' 
                       for j in ['FREQ', 'HR', 'MIN']
]
SPO_ANY_LABEL = [
    f'SPO_ANY_{i}_{j}' for i in 'ABC' 
                       for j in ['FREQ', 'HR', 'MIN']
]
INCENSE_HR_LABEL = [f'INCENSE_{i}_HR' for i in 'ABC']
DIS_LIST = [
    'OSTEOPOROSIS',
    'ARTHRITIS',
    'GOUT',
    'ASTHMA',
    'EMPHYSEMA_BRONCHITIS',
    'VALVE_HEART_DIS',
    'CORONARY_ARTERY_DIS',
    'ARRHYTHMIA',
    'CARDIOMYOPATHY',
    'CONGENITAL_HEART_DIS',
    'OTHER_HEART_DIS',
    'HYPERLIPIDEMIA',
    'HYPERTENSION',
    'APOPLEXIA',
    'DIABETES',
    'PEPTIC_ULCER',
    'GASTROESOPHAGEA_REFLUX',
    'IRRITABLE_BOWEL_SND',
    'DEPRESSION',
    'MANIC_DEPRESSION',
    'OBSESSIVE_COMPULSIVE_DIS',
    'ALCOHOLISM_DRUG_ABUSE',
    'SCHIZOPHRENIA',
    'EPILEPSY',
    'HEMICRANIA',
    'MULTIPLE_SCLEROSIS',
    'PARKISON',
    'DEMENTIA',
    'LIVER_GALL_STONE',
    'KIDNEY_STONE',
    'RENAL_FAILURE',
    'VERTIGO',
    'LIVER_CA',
    'LUNG_CA',
    'BREAST_CA',
    'GASTRIC_CA',
    'COLORECTAL_CA',
    'NASOPHARYNGEAL_CA',
    'OTHER_CA',
]

def merge_drk_curr_time(df: pd.Series):
    yr = df['DRK_CURR_YR']
    mn = df['DRK_CURR_MN']
    
    if pd.isna(yr) and pd.isna(mn):
        return np.nan
    
    rtn = 0
    if not pd.isna(yr):
        rtn += yr * 12
    
    if not pd.isna(mn):
        rtn += mn
    
    return rtn

def merge_drk_amt(
    df: pd.Series,
    freq_map: dict = {
        1: 30,
        2: 4,
        3: 1,
    },
    unit_map: dict = {
        1: 50,
        2: 150,
        3: 250,
        4: 600,
    }
    ):
    
    if all(map(pd.isna, df)):
        return np.nan
    
    rtn = 0
    for drk_type in ['DRK_CURR_A', 'DRK_CURR_B', 'DRK_CURR_C']:
        freq = df[f'{drk_type}_FREQ']
        times = df[f'{drk_type}_TIMES']
        dosage = df[f'{drk_type}_DOSAGE']
        unit = df[f'{drk_type}_UNIT']
        
        
        if any(map(pd.isna, [freq, times, dosage, unit])):
            continue
        
        freq = freq_map[freq]
        unit = unit_map[unit]
        
        rtn += freq * times * dosage * unit

    return rtn

def merge_smk_amt(
    df: pd.Series,
    freq_map: dict = {
        1: 30,
        2: 4,
        3: 1
    }
):

    freq = df['SMK_CURR_FREQ']
    pkg = df['SMK_CURR_PKG']
    
    if pd.isna(freq) or pd.isna(pkg):
        return np.nan
    
    return freq_map[freq] * pkg

def merge_smk_2nd_hr(df: pd.Series):
    if all(map(pd.isna, df)):
        return np.nan
    
    hrs = [hr for hr in df if not pd.isna(hr)]
    return sum(hrs)

def merge_nut_last_time(df: pd.Series):
    
    if all(map(pd.isna, df)):
        return np.nan
    
    yr = df['NUT_LAST_YR']
    mn = df['NUT_LAST_MN']
    if pd.isna(yr): yr = 0
    if pd.isna(mn): mn = 0
    
    return yr + mn

def merge_spo_habit_time(df: pd.Series):
    if all(map(pd.isna, df)):
        return np.nan
    
    rtn = 0
    for spo_type in ['SPO_HABIT_A', 'SPO_HABIT_B', 'SPO_HABIT_C']:
        freq = df[f'{spo_type}_FREQ']
        hr = df[f'{spo_type}_HR']
        mini = df[f'{spo_type}_MIN']
        
        if any(map(pd.isna, [freq, hr, mini])):
            continue
        
        rtn += freq * (hr * 60 + mini)

def merge_spo_any_time(df: pd.Series):
    
    if all(map(pd.isna, df)):
        return np.nan
    
    rtn = 0
    for spo_type in ['SPO_ANY_A', 'SPO_ANY_B', 'SPO_ANY_C']:
        freq = df[f'{spo_type}_FREQ']
        hr = df[f'{spo_type}_HR']
        mini = df[f'{spo_type}_MIN']
        
        if any(map(pd.isna, [freq, hr, mini])):
            continue
        
        rtn += freq * (hr * 60 + mini)
    
    return rtn

def merge_incense_hr(df: pd.Series):
    if all(map(pd.isna, df)):
        return np.nan
    rtn = 0
    for hr in df:
        if not pd.isna(hr): rtn += hr
        
    return rtn

def merge_dis_fam(df: pd.Series):
    if all(map(pd.isna, df)):
        return np.nan
    else:
        return 1

def main(args):
    df = pd.read_csv(args.csv_file)
    
    df['DRK_CURR_TIME'] = df[['DRK_CURR_YR', 'DRK_CURR_MN']].apply(merge_drk_curr_time, axis=1)
    df['DRK_CURR_AMT'] = df[DRK_AMT_LABEL].apply(merge_drk_amt, axis=1)
    df['SMK_CURR_AMT'] = df[['SMK_CURR_FREQ', 'SMK_CURR_PKG']].apply(merge_smk_amt, axis=1)
    df['SMK_2ND_HR'] = df[SMK_2ND_PLACES_HR].apply(merge_smk_2nd_hr, axis=1)
    df['NUT_LAST_TIME'] = df[['NUT_LAST_YR', 'NUT_LAST_MN']].apply(merge_nut_last_time, axis=1)
    df['SPO_HABIT_TIME'] = df[SPO_HABIT_LABEL].apply(merge_spo_habit_time, axis=1)
    df['SPO_ANY_TIME'] = df[SPO_ANY_LABEL].apply(merge_spo_any_time, axis=1)
    df['INCENSE_HR'] = df[INCENSE_HR_LABEL].apply(merge_incense_hr, axis=1)
    for dis in DIS_LIST:
        dis_column = [dis + suffix for suffix in ['_FA', '_MOM', '_BRO', '_SIS']]
        df[f'{dis}_FAM'] = df[dis_column].apply(merge_dis_fam, axis=1)

    df.to_csv(args.output_file)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--csv_file',
        type=str,
        default='./release_list_survey.csv'
    )
    parser.add_argument(
        '--output_file',
        type=str,
        default='./output.csv'
    )
    args = parser.parse_args()
    main(args)
