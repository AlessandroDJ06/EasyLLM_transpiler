from parser_modules.neuralNetwork import build_neural_network
from parser_modules.dataImport import build_dataset
from parser_modules.associationRules import build_association_rules

translated_code = ""

"""
this function is responsible for constructing the modules based on the module the user wants
"""
def parse_modules(modules):
    global translated_code

    for module_name,settings in modules.items():
        if module_name == "neural_network":
            translated_code += build_neural_network(module_name, settings)
        elif module_name == "data_import":
            translated_code += build_dataset(module_name,settings)
        elif module_name == "association_rules":
            translated_code += build_association_rules(module_name,settings)

        else:
            raise ValueError("Unknown module name")

    return translated_code