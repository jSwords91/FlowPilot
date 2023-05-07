
import os
import re
from typing import Callable, Dict, List, Optional, Union, Any



class ImportExtractor:

    @staticmethod
    def extract_all_imports(file_content: str, ignore_nesting: bool = False) -> List[str]:
        base_regexes = [
            r'import [\w.]+ as [\w.]+',
            r'import [\w.]+',
            r'from [\w.]+ import [\w.]+ as [\w.]+',
            r'from [\w.]+ import [\w.]+',
        ]
        regexes = []

        if ignore_nesting:
            for regex in base_regexes:
                regexes.append(f'^{regex}')
                regexes.append(f'\n{regex}')
        else:
            regexes += base_regexes

        regex = re.compile(f'({"|".join(regexes)})')
        return [s.strip() for s in re.findall(regex, file_content)]

    @staticmethod
    def files_in_path(path: str) -> List[str]:
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))
        return files

    @staticmethod
    def filter_file_list(file_list: List[str]) -> List[str]:
        return [item for item in file_list if ".git" not in item and "env" not in item]

    def get_import_list(self, file_list: List[str]) -> List[List[str]]:
        import_list = []
        for file_name in file_list:
            try:
                with open(file_name, mode='r') as f:
                    file_content = f.read()
                    import_list.append(self.extract_all_imports(file_content))
            except:
                pass

        return import_list

    @staticmethod
    def make_unique_list(import_list: List[List[str]]) -> List[str]:
        flat_list = [item for sublist in import_list for item in sublist]
        return list(set(flat_list))

    @staticmethod
    def clean_list(import_list: List[str]) -> List[str]:
        return [item for item in import_list if item != 'import .']

    def get_unique_imports(self, path: str) -> List[str]:
        files = self.filter_file_list(self.files_in_path(path))
        import_list = self.get_import_list(files)
        unique_imports = self.make_unique_list(import_list)
        return self.clean_list(unique_imports)
