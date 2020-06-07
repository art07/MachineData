from pathlib import Path
from typing import Dict, List

import docs


class DataLab:
    def __init__(self):
        atm_docs: Dict[str, str] = docs.get_atm_docs()
        keys = list(atm_docs.keys())
        values = list(atm_docs.values())

        self.__all_machines_docs: Dict[str, Path] = {
            keys[0]: Path(values[0]) if Path(values[0]).is_dir() else None,
            keys[1]: Path(values[1]) if Path(values[1]).is_dir() else None,
            keys[2]: Path(values[2]) if Path(values[2]).is_dir() else None,
            keys[3]: Path(values[3]) if Path(values[3]).is_file() else None,
            keys[4]: Path(values[4]) if Path(values[4]).is_file() else None,
            keys[5]: Path(values[5]) if Path(values[5]).is_dir() else None,
            keys[6]: Path(values[6]) if Path(values[6]).is_file() else None,
            keys[7]: Path(values[7]) if Path(values[7]).is_dir() else None,
            keys[8]: Path(values[8]) if Path(values[8]).is_dir() else None,
            keys[9]: Path(values[9]) if Path(values[9]).is_dir() else Path(r"C:\WOSASSP\LOG"),
            keys[10]: Path(values[10]) if Path(values[10]).is_dir() else None,
            keys[11]: Path(values[11]) if Path(values[11]).is_dir() else None,
            keys[12]: Path(values[12]) if Path(values[12]).is_file() else None,
            keys[13]: Path(values[13]) if Path(values[13]).is_file() else None,
            keys[14]: Path(values[14]) if Path(values[14]).is_file() else None,
            keys[15]: Path(values[15]) if Path(values[15]).is_file() else None
        }

        regedit_branches: Dict[str, str] = docs.get_regedit_branches()
        branches_keys: List[str] = list(regedit_branches.keys())
        branches_values: List[str] = list(regedit_branches.values())

        self.__reg_branch_list: List[RegBranch] = [
            RegBranch(branches_keys[0], branches_values[0]),
            RegBranch(branches_keys[1], branches_values[1]),
            RegBranch(branches_keys[2], branches_values[2]),
            RegBranch(branches_keys[3], branches_values[3])
        ]

        regedit_values: Dict[str, str] = docs.get_regedit_values()
        reg_param = list(regedit_values.keys())
        path_to_reg_param = list(regedit_values.values())

        self.__reg_param_list: List[RegParam] = [
            RegParam(reg_param[0], path_to_reg_param[0]),
            RegParam(reg_param[1], path_to_reg_param[1]),
            RegParam(reg_param[2], path_to_reg_param[2]),
            RegParam(reg_param[3], path_to_reg_param[3]),
            RegParam(reg_param[4], path_to_reg_param[4]),
            RegParam(reg_param[5], path_to_reg_param[5]),
            RegParam(reg_param[6], path_to_reg_param[6]),
            RegParam(reg_param[7], path_to_reg_param[7]),
            RegParam(reg_param[8], path_to_reg_param[8]),
            RegParam(reg_param[9], path_to_reg_param[9])
        ]

        self.__BASE_DIR: Path = Path('')
        self.__MACHINE_DATA_DIR: Path = Path('')
        self.__available_machine_docs: List[Path] = []
        self.__TPCA_dir: Path = Path('')
        self.__REG_dir: Path = Path('')

    def get_all_machines_docs(self):
        return self.__all_machines_docs

    def get_CHOSEN_machine_docs(self):
        return self.__available_machine_docs

    def set_available_machine_docs(self, available_machine_docs: List[Path]):
        self.__available_machine_docs = available_machine_docs

    def get_machine_data_dir(self):
        return self.__MACHINE_DATA_DIR

    def set_machine_data_dir(self, machinedata_dir: Path):
        self.__MACHINE_DATA_DIR = machinedata_dir

    def get_base_dir(self):
        return self.__BASE_DIR

    def set_base_dir(self, base_dir: Path):
        self.__BASE_DIR = base_dir

    def get_REG_dir(self):
        return self.__REG_dir

    def set_REG_dir(self, reg_dir: Path):
        self.__REG_dir = reg_dir

    def get_reg_param_list(self):
        return self.__reg_param_list

    def get_reg_branch_list(self):
        return self.__reg_branch_list

    def get_TPCA_dir(self):
        return self.__TPCA_dir

    def set_TPCA_dir(self, tpca_dir: Path):
        self.__TPCA_dir = tpca_dir


class RegParam:
    def __init__(self, reg_name: str, reg_path: str):
        self.param_name: str = reg_name
        self.param_path: str = reg_path
        self.param_value = None


class RegBranch:
    def __init__(self, branch_name: str, branch_path: str):
        self.branch_name: str = branch_name
        self.full_branch_name: str = f"{branch_name}.reg"
        self.branch_path: str = branch_path
