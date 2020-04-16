from pathlib import Path
from typing import Dict, List


class DataLab:
    def __init__(self):
        docs_from_txt: Dict[str, str] = self.create_docs_from_txt()
        keys = list(docs_from_txt.keys())
        values = list(docs_from_txt.values())

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

        self.__reg_param_list: List[RegParam] = [
            RegParam("REMOTEPEER", r"SOFTWARE\Wincor Nixdorf\ProTopas\CurrentVersion\CCOPEN\COMMUNICATION\TCPIP\PROJECT"),
            RegParam("PORTNUMBER", r"SOFTWARE\Wincor Nixdorf\ProTopas\CurrentVersion\CCOPEN\COMMUNICATION\TCPIP\PROJECT"),
            RegParam("Header", r"SOFTWARE\Wincor Nixdorf\ProTopas\CurrentVersion\LYNXPAR\Renome\CassCounters"),
            RegParam("PAGE_HEADER", r"SOFTWARE\Wincor Nixdorf\ProTopas\CurrentVersion\LYNXPAR\PRINTER\RECEIPT"),
            RegParam("NUM_LOG_CASS", r"SOFTWARE\Wincor Nixdorf\ProTopas\CurrentVersion\LYNXPAR\CASH_DISPENSER"),
            RegParam("DOUBLE_LENGTH_KEYS", r"SOFTWARE\Wincor Nixdorf\ProTopas\CurrentVersion\LYNXPAR\APPLICATION"),
            RegParam("NoteIDs", r"SOFTWARE\XFS\PHYSICAL_SERVICES\SNA30"),
            RegParam("Counters", r"SOFTWARE\XFS\PHYSICAL_SERVICES\SNA30"),
            RegParam("Notes", r"SOFTWARE\Renome-Smart\TPCA\Config"),
            RegParam("TerminalID", r"SOFTWARE\Renome-Smart\TPCA\Config")
        ]

        self.__chosen_dir = None
        self.__MACHINE_DATA_DIR = None
        self.__CHOSEN_machine_docs = []
        self.__TPCA_dir = None
        self.__REG_dir = None

    @staticmethod
    def create_docs_from_txt():
        docs_from_txt: Dict[str, str] = {}
        with open("paths_of_docs.txt") as file_object:
            for line in file_object:
                lst = line.rstrip().split("#")
                docs_from_txt[lst[0]] = lst[1]
        return docs_from_txt

    def get_all_machines_docs(self):
        return self.__all_machines_docs

    def get_CHOSEN_machine_docs(self):
        return self.__CHOSEN_machine_docs

    def set_CHOSEN_machine_docs(self, chosen_list):
        self.__CHOSEN_machine_docs = chosen_list

    def get_machine_data_dir(self):
        return self.__MACHINE_DATA_DIR

    def set_machine_data_dir(self, param: Path):
        self.__MACHINE_DATA_DIR = param

    def get_chosen_dir(self):
        return self.__chosen_dir

    def set_chosen_dir(self, chosen_dir: Path):
        self.__chosen_dir = chosen_dir

    def get_REG_dir(self):
        return self.__REG_dir

    def set_REG_dir(self, param):
        self.__REG_dir = param

    def get_reg_param_list(self):
        return self.__reg_param_list

    def get_TPCA_dir(self):
        return self.__TPCA_dir

    def set_TPCA_dir(self, param):
        self.__TPCA_dir = param


class RegParam:
    def __init__(self, reg_name: str, reg_path: str):
        self.param_name = reg_name
        self.param_path = reg_path
        self.param_value = None
