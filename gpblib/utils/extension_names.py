import re

from gpblib.modules_configs import MODULES_CONFIG

def generate_extension_names(module_name, current_extension_names):
    module = MODULES_CONFIG[module_name]
    guid_pairs = re.findall(r'\[([^\]]+)\]', current_extension_names)
    extension_names = [re.findall(r'\{([0-9A-Fa-f\-]{36})\}', pair) for pair in guid_pairs]

    if module["setting_type"] == "Preferences":
        if "00000000-0000-0000-0000-000000000000" not in [guid_pair[0] for guid_pair in extension_names]:
            extension_names.insert(0, ["00000000-0000-0000-0000-000000000000", module["admin_guid"]])
        else:
            for item in extension_names:
                if item[0] == "00000000-0000-0000-0000-000000000000":
                    if module["admin_guid"] not in item:
                        item.append(module["admin_guid"])
                    break

    if [module["cse_guid"], module["admin_guid"]] not in extension_names:
        extension_names.append([module["cse_guid"], module["admin_guid"]])
    
    # For whatever reason, extension names actually need to be sorted to be processed correctly (not the case for the GPO core Preferences guids)
    extension_names.sort(key=lambda guid_pair: guid_pair[0])

    if extension_names is not None:
        extension_names = [''.join(f"{{{guid}}}" for guid in guid_pair) for guid_pair in extension_names]
        extension_names = ''.join(f"[{item}]" for item in extension_names)
    return extension_names
