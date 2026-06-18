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