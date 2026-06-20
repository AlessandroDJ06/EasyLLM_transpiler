def build_association_rules(module_name, settings):
    dataset_name = ""
    transaction_id = ""
    item_id = ""
    ignore_item = ""

    min_support = "0.1"
    min_lift = "1.2"
    min_confidence = "0.5"
    output_rules = "final_association_rules.json"
    output_freq = "page_frequenties.json"

    for setting in settings:
        s_name = setting['setting'].strip()
        s_val = setting['value'].strip().replace('"', '').replace("'", "")

        if s_name == 'dataset_name':
            dataset_name = s_val
        elif s_name == 'transaction_id':
            transaction_id = s_val
        elif s_name == 'item_id':
            item_id = s_val
        elif s_name == 'ignore_item':
            ignore_item = s_val
        elif s_name == 'min_support':
            min_support = s_val
        elif s_name == 'min_lift':
            min_lift = s_val
        elif s_name == 'min_confidence':
            min_confidence = s_val
        elif s_name == 'output_rules':
            output_rules = s_val
        elif s_name == 'output_freq':
            output_freq = s_val

    if ignore_item != "":
        filter_code = f"df_flat = df_flat[df_flat['{item_id}'] != '{ignore_item}']"
    else:
        filter_code = "# Geen ignore_item opgegeven"

    imports = f"""
from mlxtend.frequent_patterns import apriori, association_rules
import os
import json
"""

    code = f"""
df_flat = {dataset_name}_df[['{transaction_id}', '{item_id}']].dropna()

{filter_code}

item_counts = df_flat['{item_id}'].value_counts()
df_frequenties = [{{'item': key, 'frequentie': int(val)}} for key, val in item_counts.items()]

dataset = pd.crosstab(df_flat['{transaction_id}'], df_flat['{item_id}']) > 0

frequent_itemsets = apriori(dataset, min_support={min_support}, use_colnames=True)

if not frequent_itemsets.empty:
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold={min_lift})
    rules = rules[rules['confidence'] >= {min_confidence}]
    rules = rules.sort_values('lift', ascending=False)
else:
    rules = pd.DataFrame()

if "{output_rules}" != "":
    dir_rules = os.path.dirname("{output_rules}")
    if dir_rules:
        os.makedirs(dir_rules, exist_ok=True)

    if not rules.empty:
        rules_json = rules.copy()
        rules_json['antecedents'] = rules_json['antecedents'].apply(list)
        rules_json['consequents'] = rules_json['consequents'].apply(list)
        rules_json.to_json("{output_rules}", orient='records', indent=4)
    else:
        with open("{output_rules}", "w") as f:
            json.dump([], f)
            
if "{output_freq}" != "":
    dir_freq = os.path.dirname("{output_freq}")
    if dir_freq:
        os.makedirs(dir_freq, exist_ok=True)

    with open("{output_freq}", "w") as f:
        json.dump(df_frequenties, f, indent=4)
"""
    return [imports,code]