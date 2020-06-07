# https://janakiev.com/blog/python-shell-commands/
from pathlib import Path
from model import DataLab
from utils.collect_utils import CollectUtils
from utils.controller_utils import ControllerUtils
import sys
import timeit
from utils import analyse_utils as au
from typing import Dict, Callable, Tuple


class AppController:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'single_object_of_appcontroller'):
            cls.single_object_of_appcontroller = super(AppController, cls).__new__(cls)
        return cls.single_object_of_appcontroller

    def __init__(self, console_view):
        self.MAIN_FOLDER_NAME: str = "MachineData"
        self.cv = console_view
        self.data_lab: DataLab = DataLab()
        self.method_dic: Dict[str, Callable] = {
            "exit": AppController.__machine_data_exit,
            "collect_atm": self.__atm_job,
            "collect_terminal": self.__terminal_job,
            "analyse": self.__analyse_job
        }

    def action(self, user_choice):
        result_code: Tuple[int, str] = (0, '')

        if user_choice == 0:
            self.method_dic['exit']()
        elif user_choice == 1:
            result_code = self.method_dic["collect_atm"]()
        elif user_choice == 2:
            result_code = self.method_dic["collect_terminal"]()
        elif user_choice == 3:
            result_code = self.method_dic["analyse"]()

        if result_code[0] == 0:
            self.cv.close_menu("\n>>>>>>> PROGRAM FINISHED <<<<<<<\n")
        elif result_code[0] == 1:
            self.cv.close_menu(result_code[1])

    @staticmethod
    def __machine_data_exit():
        sys.exit()

    def first_of_all(self):
        ControllerUtils.create_MAIN_dir(self)
        ControllerUtils.create_REG_dir(self.data_lab)
        ControllerUtils.create_list_copying_folders(self.data_lab)

    def general_job_for_all_machines(self):
        start_point = timeit.default_timer()

        # 1) Collect journals.
        if len(self.data_lab.get_CHOSEN_machine_docs()) > 0:
            CollectUtils.collection_journals(self.data_lab)
        else:
            print("No journals to copy!")

        # 2) Collect ip.
        CollectUtils.get_ip_data(self.data_lab)

        # 3) Collect reg branches.
        CollectUtils.save_REG_branches(self.data_lab)

        # 4) Collect reg values.
        CollectUtils.get_reg_values(self.data_lab)

        end_point = timeit.default_timer()
        print(f"WASTED TIME -> {(end_point - start_point):.2f} seconds\nPath to data >>> {self.data_lab.get_machine_data_dir()}")

    def __atm_job(self):
        result_code: Tuple[int, str] = (0, '')
        if not Path("C:/TPCA/Log").is_dir():
            self.first_of_all()
            self.general_job_for_all_machines()
        else:
            result_code = (1, 'It is not an ATM.')
        return result_code

    def __terminal_job(self):
        result_code: Tuple[int, str] = (0, '')
        if Path("C:/TPCA/Log").is_dir():
            self.first_of_all()
            ControllerUtils.create_TPCA_dir(self.data_lab)
            self.general_job_for_all_machines()
        else:
            result_code = (1, 'It is not a Terminal.')
        return result_code

    def __analyse_job(self):
        result_code: Tuple[int, str] = (0, '')
        if not Path("C:/TPCA/Log").is_dir():
            au.AnalyseUtils.cdm_scod_analyser(self)
        else:
            result_code = (1, 'Available only for ATMs.')
        return result_code
