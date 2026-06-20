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
    allow_debug_prints=False

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
            if s_val in ['regression', 'classification', 'association_rules']:
                task_type = s_val
            else:
                raise ValueError(f"Error in {module_name}: task must be either regression, classification or association_rules")

    if task_type != 'association_rules' and not target_column:
        raise ValueError(f"Error in {module_name}: target column is required for {task_type}")

    if task_type == 'association_rules':
        processing_code = f"""
    {name}_df_cleaned = {name}_df.astype(str).apply(lambda x: x.str.strip())
    {name}_X = pd.get_dummies({name}_df_cleaned, dtype=bool)
"""
    else:
        if task_type == 'regression':
            target_processing = f"{name}_y = {name}_df['{target_column}'].values.astype(np.float32)\n"
        else:
            target_processing = f"{name}_y = pd.factorize({name}_df['{target_column}'])[0].astype(np.float32)\n"

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
        processing_code = target_processing + feature_processing + random_statecode

    imports = f"""
import numpy as np 
import pandas as pd
import os
from sklearn.model_selection import train_test_split
"""


    code_blok = f"""
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
"""
    debug_prints = [f"""
    print(f"rows before cleanup: {{len({name}_df)}}")
""",f"""
    print(f"rows after cleanup: {{len({name}_df)}}")
"""]
    cleanup_code = f"""
    {name}_df = {name}_df.replace([np.inf, -np.inf], np.nan)
    {name}_df = {name}_df.dropna()
    """
    if allow_debug_prints:
        code_blok += debug_prints[0] + cleanup_code + debug_prints[1] + processing_code
    else:
        code_blok += cleanup_code + processing_code

    dataset_code += code_blok
    return [imports,dataset_code]