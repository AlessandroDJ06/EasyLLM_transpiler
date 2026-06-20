import re

"""
this function is responsible for finding tokens for each individual module, by doing this we can easily translate the
user settings into real python code and handle syntax errors in detail for each module
"""
def find_modules(source_code):
    modules = []

    comment_pattern = r'"""[\s\S]*?"""'
    source_code = re.sub(comment_pattern, '', source_code)

    module_pattern = r'(\w+)\s*\{([^}]+)\}'
    setting_pattern = r'(\w+):([^;]+);'

    for module_match in re.finditer(module_pattern, source_code):
        module_name = module_match.group(1)
        module_content = module_match.group(2)

        settings = []
        for setting_match in re.finditer(setting_pattern, module_content):
            settings.append({
                "setting": setting_match.group(1),
                "value": setting_match.group(2)
            })

        modules.append((module_name, settings))

    return modules