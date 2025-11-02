import os
import errno
import logging
import configparser

from pathlib                               import Path

from gpblib.parsing.models                 import GPBModule
from gpblib.utils.colors                   import bcolors

logger = logging.getLogger(__name__)


def validate_modules(modules_files: str) -> list:
    if len(modules_files) == 0:
        return []

    parsed_modules_files = []
    for module_file in modules_files:
        if not Path(module_file).is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), module_file)
        module_parser = configparser.ConfigParser(interpolation=None)
        module_parser.read(module_file)
        parsed_modules_files.append((module_file, module_parser))

    modules = []
    for parsed_module_file in parsed_modules_files:
        logger.info(f"[INFO] Validating module {parsed_module_file[0]}")
        try:
            module_data = {section: dict(parsed_module_file[1].items(section)) for section in parsed_module_file[1].sections()}
            validated_module = GPBModule(**module_data)
            modules.append(validated_module)
        except Exception as e:
            logger.error(f"{bcolors.FAIL}[!] Error encountered during validation of module '{parsed_module_file[0]}'{bcolors.ENDC}")
            logger.error(str(e))
            raise e

    return modules