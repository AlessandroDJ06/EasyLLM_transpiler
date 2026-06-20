import numpy as np 
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models
from mlxtend.frequent_patterns import apriori, association_rules
import json

dataset1_path = "student_study_habits_exam_dataset.csv"
dataset1_batch_size = 32
dataset1_split = 0.1

if not os.path.exists(dataset1_path):
    print(f"\n[COMPILER ERROR] Het bestand '{dataset1_path}' kan niet worden gevonden!")
    print(f"Huidige werkmap waar gezocht wordt: {os.getcwd()}\n")
else:
    print(f"Dataset dataset1 loaded from : {dataset1_path}")
    dataset1_df = pd.read_csv(dataset1_path, sep=',', on_bad_lines='skip')
    dataset1_df.columns = dataset1_df.columns.str.strip()

    dataset1_df = dataset1_df.replace([np.inf, -np.inf], np.nan)
    dataset1_df = dataset1_df.dropna()
    dataset1_y = dataset1_df['Exam_Score'].values.astype(np.float32)

    features_df = dataset1_df.drop(columns=['Exam_Score'])
    features_df = pd.get_dummies(features_df, drop_first=True)
    dataset1_X = features_df.values.astype(np.float32)

    dataset1_X_train, dataset1_X_test, dataset1_Y_train, dataset1_Y_test = train_test_split(dataset1_X, dataset1_y, test_size=0.1)

model1 = models.Sequential([
    layers.Input(shape=(dataset1_X_train.shape[1],)),
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    
        layers.Dense(1)
])
        
model1.compile(optimizer='adam', loss='mse', metrics=['mae'])
model1.fit(
    dataset1_X_train, 
    dataset1_Y_train, 
    epochs=200, 
    batch_size=64, 
    shuffle=True, 
    validation_data=(dataset1_X_test, dataset1_Y_test)
)

student_habits_path = "student_study_habits_exam_dataset.csv"
student_habits_batch_size = 32
student_habits_split = 0.2

if not os.path.exists(student_habits_path):
    print(f"\n[COMPILER ERROR] Het bestand '{student_habits_path}' kan niet worden gevonden!")
    print(f"Huidige werkmap waar gezocht wordt: {os.getcwd()}\n")
else:
    print(f"Dataset student_habits loaded from : {student_habits_path}")
    student_habits_df = pd.read_csv(student_habits_path, sep=',', on_bad_lines='skip')
    student_habits_df.columns = student_habits_df.columns.str.strip()

    student_habits_df = student_habits_df.replace([np.inf, -np.inf], np.nan)
    student_habits_df = student_habits_df.dropna()
    
    student_habits_df_cleaned = student_habits_df.astype(str).apply(lambda x: x.str.strip())
    student_habits_X = pd.get_dummies(student_habits_df_cleaned, dtype=bool)

df_flat = student_habits_df[['Student_ID', 'Preferred_Study_Method']].dropna()

# Geen ignore_item opgegeven

item_counts = df_flat['Preferred_Study_Method'].value_counts()
df_frequenties = [{'item': key, 'frequentie': int(val)} for key, val in item_counts.items()]

dataset = pd.crosstab(df_flat['Student_ID'], df_flat['Preferred_Study_Method']) > 0

frequent_itemsets = apriori(dataset, min_support=0.05, use_colnames=True)

if not frequent_itemsets.empty:
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
    rules = rules[rules['confidence'] >= 0.4]
    rules = rules.sort_values('lift', ascending=False)
else:
    rules = pd.DataFrame()

if "output/study_method_rules.json" != "":
    dir_rules = os.path.dirname("output/study_method_rules.json")
    if dir_rules:
        os.makedirs(dir_rules, exist_ok=True)

    if not rules.empty:
        rules_json = rules.copy()
        rules_json['antecedents'] = rules_json['antecedents'].apply(list)
        rules_json['consequents'] = rules_json['consequents'].apply(list)
        rules_json.to_json("output/study_method_rules.json", orient='records', indent=4)
    else:
        with open("output/study_method_rules.json", "w") as f:
            json.dump([], f)
            
if "output/study_method_frequencies.json" != "":
    dir_freq = os.path.dirname("output/study_method_frequencies.json")
    if dir_freq:
        os.makedirs(dir_freq, exist_ok=True)

    with open("output/study_method_frequencies.json", "w") as f:
        json.dump(df_frequenties, f, indent=4)
