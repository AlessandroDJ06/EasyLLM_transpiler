def build_dataset(module_name, settings):
    dataset_code = ""
    source = ""
    name = ""
    batch_size = "32"
    split = "0.2"
    seperator = ","
    target_column = ""
    random_state = ""
    task_type = "regression"

    for setting in settings:
        s_name = setting['setting'].strip()
        s_val = setting['value'].strip().replace('"', '').replace("'", "")

        if s_name == 'name':
            name = s_val
        elif s_name == 'source':
            source = s_val
        elif s_name == 'test_split':
            try:
                s_val_clean = s_val.replace(',', '.')
                split_float = float(s_val_clean)
                if 0.0 < split_float < 1.0:
                    split = s_val_clean
                else:
                    raise ValueError
            except ValueError:
                raise ValueError(f"Error in {module_name}: split must be a float between 0 and 1 (e.g. 0.1 or 0,1)")
        elif s_name == 'target':
            target_column = s_val
        elif s_name == 'seperator':
            seperator = s_val
        elif s_name == 'random_state':
            if s_val.isdigit():
                random_state = s_val
            else:
                raise ValueError(f"Error in {module_name}: random_state must be an integer")
        elif s_name in ['type', 'task']:
            if s_val in ['regression', 'classification']:
                task_type = s_val
            else:
                raise ValueError(f"Error in {module_name}: task must be either regression or classification")

    if task_type == 'regression':
        target_processing = f"    {name}_y = {name}_df['{target_column}'].values.astype(np.float32)\n"
    else:
        target_processing = f"    {name}_y = pd.factorize({name}_df['{target_column}'])[0].astype(np.float32)\n"

    feature_processing = f"""
    features_df = {name}_df.drop(columns=['{target_column}'])
    features_df = pd.get_dummies(features_df, drop_first=True)
    {name}_X = features_df.values.astype(np.float32)
"""

    if random_state != "":
        random_statecode = f"""
    {name}_X_train, {name}_X_test, {name}_Y_train, {name}_Y_test = train_test_split({name}_X, {name}_y, test_size={split}, random_state={random_state})
"""
    else:
        random_statecode = f"""
    {name}_X_train, {name}_X_test, {name}_Y_train, {name}_Y_test = train_test_split({name}_X, {name}_y, test_size={split})
"""

    code_blok = f"""
# Settings for dataset: {name}
import numpy as np 
import pandas as pd
import os
from sklearn.model_selection import train_test_split

{name}_path = "{source}"
{name}_batch_size = {batch_size}
{name}_split = {split}

if not os.path.exists({name}_path):
    print(f"\\n[COMPILER ERROR] Het bestand '{{{name}_path}}' kan niet worden gevonden!")
    print(f"Huidige werkmap waar gezocht wordt: {{os.getcwd()}}\\n")
else:
    print(f"Dataset {name} loaded from : {{{name}_path}}")
    {name}_df = pd.read_csv({name}_path, sep='{seperator}', on_bad_lines='skip')
    {name}_df.columns = {name}_df.columns.str.strip()
    print(f"rows before cleanup: {{len({name}_df)}}")
    {name}_df = {name}_df.replace([np.inf, -np.inf], np.nan)
    {name}_df = {name}_df.dropna()
    print(f"rows after cleanup: {{len({name}_df)}}")
"""

    code_blok += target_processing + feature_processing + random_statecode

    dataset_code += code_blok

    return dataset_code