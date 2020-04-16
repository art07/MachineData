# https://janakiev.com/blog/python-shell-commands/
from tkinter import filedialog
from pathlib import Path
from src.model import DataLab
from src.collect_utils import CollectUtils
import sys
from tkinter import Tk
import timeit
from src.cdm_analyser_utils import CdmAnalyserUtils
from typing import List


class AppController:
    def __init__(self, console_view):
        self.MAIN_folder_name: str = "MachineData"
        self.cv = console_view
        self.data_lab: DataLab = DataLab()
        self.collect_utils: CollectUtils = CollectUtils()
        self.method_dic = {
            "collect": self.Atm_Terminal_JOB,
            "analyse": self.CDM_SCOD_Analyser_JOB,
            "exit": AppController.machine_data_exit
        }

    def action(self):
        # ATM / T > collect
        if (self.cv.current_MACHINE == self.cv.machines_list[0] and self.cv.USER_CHOICE == 1) \
                or (self.cv.current_MACHINE == self.cv.machines_list[1] and self.cv.USER_CHOICE == 1):
            self.method_dic["collect"]()
        # ATM > analyse
        elif self.cv.current_MACHINE == self.cv.machines_list[0] and self.cv.USER_CHOICE == 2:
            self.method_dic["analyse"]()
        # ATM / T > exit
        elif (self.cv.current_MACHINE == self.cv.machines_list[0] and self.cv.USER_CHOICE == 3) \
                or (self.cv.current_MACHINE == self.cv.machines_list[1] and self.cv.USER_CHOICE == 2):
            self.method_dic["exit"]()

        self.cv.close_menu("\n>>>>>>> PROGRAM FINISHED <<<<<<<\n")

    def Atm_Terminal_JOB(self):
        self.create_MAIN_folder()
        start_point = timeit.default_timer()

        self.collect_utils.create_list_copying_folders(self.data_lab)
        if len(self.data_lab.get_CHOSEN_machine_docs()) > 0:
            if self.cv.current_MACHINE == self.cv.machines_list[1]:
                self.collect_utils.create_TPCA(self.data_lab)
            self.collect_utils.collection_journals(self.data_lab)
        else:
            print("No journals to copy!")
        self.collect_utils.get_ip_data(self.data_lab.get_machine_data_dir())
        self.collect_utils.create_REG(self.data_lab)
        self.collect_utils.save_REG_branches(self.data_lab)
        self.collect_utils.get_reg_values(self.cv, self.data_lab)

        end_point = timeit.default_timer()
        print(f"Wasted time > {(end_point - start_point):.2f} seconds\nPath to data >>> {self.data_lab.get_machine_data_dir()}")

    def CDM_SCOD_Analyser_JOB(self):
        str_chosen_path = self.window_helper("file")
        if str_chosen_path != '':
            path_obj = Path(str_chosen_path)
            is_command_started: bool = False
            is_command_finished: bool = False
            super_string: str = ""
            super_string_list: List[str] = []
            with open(path_obj, "r") as cmd_log_file:
                for string_line in cmd_log_file:
                    if string_line.find("<EVENT") != -1:
                        if string_line.find("SCOD=") != -1:  # Если SCOD есть
                            if string_line.find("SCOD=14") == -1 and string_line.find("SCOD=00") == -1:
                                super_string_list.append(string_line)
                                continue
                            else:
                                continue
                        else:
                            continue

                    if string_line.find("<COMMAND") != -1:
                        is_command_started = True
                    elif string_line.find("</COMMAND>") != -1:
                        is_command_started = False
                        is_command_finished = True

                    if is_command_started:
                        super_string += string_line
                    if is_command_finished:
                        super_string += "</COMMAND>\n"
                        if super_string.find("SCOD=") != -1:  # Если SCOD есть
                            if super_string.find("SCOD=14") == -1 and super_string.find("SCOD=00") == -1:
                                super_string_list.append(super_string)
                        super_string = ""
                        is_command_finished = False

            if len(super_string_list) == 0:
                print("_____________________________________________________\nSCOD NOT FOUND\n_____________________________________________________")
            else:
                if not CdmAnalyserUtils.is_scod_dic_made:
                    CdmAnalyserUtils.make_scod_dic()
                print("_____________________________________________________")

                for list_line in super_string_list:
                    param_list = list_line.split(',')
                    shut_str = mon_str = ts_str = scod_str = ""
                    for param in param_list:
                        if param.find("SHUT=") != -1:
                            shut_str = CdmAnalyserUtils.shut_analyse(param)
                        elif param.find("MON=") != -1:
                            mon_str = CdmAnalyserUtils.mon_analyse(param)
                        elif param.find("TS=") != -1:
                            ts_str = CdmAnalyserUtils.ts_analyse(param)
                        elif param.find("SCOD=") != -1:
                            scod_str = CdmAnalyserUtils.scod_analyse(param)
                    print(f"\n{list_line}* {shut_str}\n* {mon_str}\n* {ts_str}\n* {scod_str}")

                print("_____________________________________________________")
        else:
            self.cv.close_menu("The choice of the path is not made")

    @staticmethod
    def machine_data_exit():
        sys.exit()

    def create_MAIN_folder(self):
        print(
            f"Choose directory (in this directory will be created folder > {self.MAIN_folder_name} < for collecting {self.cv.current_MACHINE} data)")
        str_chosen_path = self.window_helper("dir")
        if str_chosen_path != '':
            self.data_lab.set_chosen_dir(Path(str_chosen_path))
            self.data_lab.set_machine_data_dir(Path().joinpath(self.data_lab.get_chosen_dir(), self.MAIN_folder_name))
            if not self.data_lab.get_machine_data_dir().is_dir():
                self.data_lab.get_machine_data_dir().mkdir()
                if self.data_lab.get_machine_data_dir().is_dir():
                    print(
                        f"{self.MAIN_folder_name} created successfully! Full path >>> {str(self.data_lab.get_machine_data_dir())}\n")
                else:
                    self.cv.close_menu("get_machine_data_dir().is_dir() FALSE!")
            else:
                self.cv.close_menu(
                    f"{self.MAIN_folder_name} already EXISTS. Delete old {self.MAIN_folder_name} before start new attempt")
        else:
            self.cv.close_menu("The choice of the path is NOT made")

    def window_helper(self, doc):
        window = Tk()
        str_chosen_path = ""
        if doc == "dir":
            str_chosen_path = filedialog.askdirectory(title="Choose directory", initialdir=Path.home())
        elif doc == "file":
            str_chosen_path = filedialog.askopenfilename(title="Choose TRC.XML file",
                                                         initialdir=self.data_lab.get_all_machines_docs().get(
                                                             "LOG"), filetypes=[("cdm log files", "*.TRC.XML")])
        window.destroy()
        return str_chosen_path
