def build_neural_network(module_name, settings):
    name = ""
    dataset_name = ""
    batch_size = 64
    output_layer_activation = ''
    optimizer = 'adam'
    shuffle_dataset = True
    type = "regression"
    epochs = 50

    hidden_layers = ""
    for setting in settings:
        s_name = setting['setting']
        s_val = setting['value'].strip().replace('"', '')

        if s_name == 'dataset_name':
            dataset_name = s_val
        elif s_name == 'name':
            name = s_val
        elif s_name == 'batch_size':
            if s_val.isdigit():
                batch_size = s_val
            else:
                raise ValueError(f"Error in {module_name}: batch_size must be an integer")
        elif s_name == 'output_layer_activation':
            output_layer_activation = s_val.lower().replace("'", "")
            if output_layer_activation not in ['relu', 'sigmoid', 'softmax', 'tanh', 'linear', 'leaky_relu', 'elu',
                                               'selu', 'gelu', 'swish', 'exponential', 'softplus', 'softsign']:
                raise ValueError(f"{s_val} is not a valid value for output_layer_activation")
        elif s_name == 'optimizer':
            optimizer = s_val.lower().replace("'", "")
            if optimizer not in ['adam', 'adamw', 'sgd', 'rmsprop', 'adagrad', 'adamax', 'nadam', 'adadelta', 'ftrl',
                                 'lion', 'loss_scale_optimizer']:
                raise ValueError(f"{s_val} is not a valid value for optimizer")
        elif s_name == 'shuffle_dataset' or s_name == 'shuffle_data':
            val_clean = s_val.lower().replace("'", "")
            if val_clean in ['true', 'false']:
                shuffle_dataset = (val_clean == 'true')
            else:
                raise ValueError(f"{s_val} is not a valid value for shuffle_dataset")
        elif s_name == 'hidden_layers':

            clean_list = s_val.strip("[]").split(",")
            for hidden_layer in clean_list:
                values = hidden_layer.split("'")
                hidden_layers += f"    layers.Dense({values[0].strip()}, activation='{values[1].strip()}'),\n"
        elif s_name == 'type':
            type = s_val.replace("'", "")
            if type not in ['regression', 'binary_classification', 'multi_classification']:
                raise ValueError(f"{s_val} is not a valid value for type")
        elif s_name == 'epochs':
            if s_val.isdigit():
                epochs = s_val


    if type == 'regression':
        loss = "'mse'"
        metric = "'mae'"
    elif type == 'binary_classification':
        loss = "'binary_crossentropy'"
        metric = "'accuracy'"
    else:
        loss = "'sparse_categorical_crossentropy'"
        metric = "'accuracy'"

    imports = f"""
from tensorflow.keras import layers, models
"""

    input_layer = f"""
{name} = models.Sequential([
    layers.Input(shape=({dataset_name}_X_train.shape[1],)),
"""

    if type == 'regression' or type == 'binary_classification':
        if output_layer_activation == '':
            output_layer = f"""    
        layers.Dense(1)
])
        """
        else:
            output_layer = f"""    
        layers.Dense(1, activation='{output_layer_activation}')
])
        """
    else:
        if output_layer_activation == '':
            output_layer = f"""    
        layers.Dense(len(np.unique({dataset_name}_Y_train))')
])
"""
        else:
            output_layer = f"""    
        layers.Dense(len(np.unique({dataset_name}_Y_train)), activation='{output_layer_activation}')
])
"""

    model_code = input_layer + hidden_layers + output_layer

    model_compile_and_train = f"""
{name}.compile(optimizer='{optimizer}', loss={loss}, metrics=[{metric}])
{name}.fit(
    {dataset_name}_X_train, 
    {dataset_name}_Y_train, 
    epochs={epochs}, 
    batch_size={batch_size}, 
    shuffle={shuffle_dataset}, 
    validation_data=({dataset_name}_X_test, {dataset_name}_Y_test)
)
"""

    model_code += model_compile_and_train
    return [imports,model_code]