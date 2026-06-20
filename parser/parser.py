from parser_modules.neuralNetwork import build_neural_network
from parser_modules.dataImport import build_dataset
from parser_modules.associationRules import build_association_rules

def parse_modules(modules):
    translated_code = ""
    all_import_lines = []

    for module_name, settings in modules:
        if module_name == "neural_network":
            imports, code = build_neural_network(module_name, settings)
        elif module_name == "data_import":
            imports, code = build_dataset(module_name, settings)
        elif module_name == "association_rules":
            imports, code = build_association_rules(module_name, settings)
        else:
            raise ValueError("Unknown module name")

        all_import_lines.extend(line for line in imports.splitlines() if line.strip())
        translated_code += code

    unique_imports = list(dict.fromkeys(all_import_lines))
    import_block = "\n".join(unique_imports)

    return import_block + "\n" + translated_code