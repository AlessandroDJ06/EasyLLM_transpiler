import re

"""
this function is responsible for finding tokens for each individual module, by doing this we can easily translate the
user settings into real python code and handle syntax errors in detail for each module
"""
def find_modules(source_code):
    modules = {}

    module_pattern = r'(\w+)\{([^}]+)\}'

    setting_pattern = r'(\w+):([^;]+);'

    for module_match in re.finditer(module_pattern, source_code):
        module_name = module_match.group(1)
        module_content = module_match.group(2)

        modules[module_name] = []

        for setting_match in re.finditer(setting_pattern, module_content):
            setting_name = setting_match.group(1)
            setting_value = setting_match.group(2)

            modules[module_name].append({
                "setting": setting_name,
                "value": setting_value
            })

    return modules