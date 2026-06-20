data_import{
    name:dataset1;
    source:student_study_habits_exam_dataset.csv;
    test_split:0,1;
    target:Exam_Score;
    task:regression;
}

neural_network{
    dataset_name:dataset1;
    name:model1;
    hidden_layers:[64'relu,32'relu];
    type:regression;
    optimizer:adam;
    batchsize:32;
    shuffle_data:true;
    epochs:200;
}

data_import {
    name: student_habits;
    source: "student_study_habits_exam_dataset.csv";
    task: association_rules;
}
"""
test of we nog compilereennnn
"""
association_rules {
    dataset_name: student_habits;
    transaction_id: "Student_ID";
    item_id: "Preferred_Study_Method";
    min_support: 0.05;
    min_lift: 1.0;
    min_confidence: 0.4;
    output_rules: "output/study_method_rules.json";
    output_freq: "output/study_method_frequencies.json";
}