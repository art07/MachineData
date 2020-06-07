from pathlib import Path
from typing import List

from utils.controller_utils import ControllerUtils
import controller as c
from utils import cdm_analyser_utils as cau


class AnalyseUtils:
    is_command_started: bool = False
    is_command_finished: bool = False

    @staticmethod
    def cdm_scod_analyser(controller: 'c.AppController'):
        chosen_path: str = ControllerUtils.window_helper(path_obj=controller.data_lab.get_all_machines_docs()['LOG'], doc="file")
        if chosen_path != '':
            path_obj = Path(chosen_path)

            super_string: str = ""
            super_string_list: List[str] = []

            with open(path_obj, "r") as file_object:
                for line_from_file in file_object:
                    if line_from_file.find("<EVENT") != -1:  # Если <EVENT есть.
                        if line_from_file.find("SCOD=") != -1:  # Если SCOD есть.
                            if line_from_file.find("SCOD=14") == -1 and line_from_file.find("SCOD=00") == -1:
                                super_string_list.append(line_from_file)
                                continue
                            else:
                                continue
                        else:
                            continue

                    if line_from_file.find("<COMMAND") != -1:
                        AnalyseUtils.is_command_started = True
                    elif line_from_file.find("</COMMAND>") != -1:
                        AnalyseUtils.is_command_started = False
                        AnalyseUtils.is_command_finished = True

                    if AnalyseUtils.is_command_started:
                        super_string += line_from_file
                    if AnalyseUtils.is_command_finished:
                        super_string += "</COMMAND>\n"
                        if super_string.find("SCOD=") != -1:  # Если SCOD есть
                            if super_string.find("SCOD=14") == -1 and super_string.find("SCOD=00") == -1:
                                super_string_list.append(super_string)
                        super_string = ""
                        AnalyseUtils.is_command_finished = False

            if len(super_string_list) == 0:
                print("_____________________________________________________\nSCOD NOT FOUND\n_____________________________________________________")
            else:
                if not cau.CdmAnalyserUtils.is_scod_dic_made:
                    cau.CdmAnalyserUtils.make_scod_dic()
                print("_____________________________________________________")

                for list_line in super_string_list:
                    param_list = list_line.split(',')
                    shut_str = mon_str = ts_str = scod_str = ""
                    for param in param_list:
                        if param.find("SHUT=") != -1:
                            shut_str = cau.CdmAnalyserUtils.shut_analyse(param)
                        elif param.find("MON=") != -1:
                            mon_str = cau.CdmAnalyserUtils.mon_analyse(param)
                        elif param.find("TS=") != -1:
                            ts_str = cau.CdmAnalyserUtils.ts_analyse(param)
                        elif param.find("SCOD=") != -1:
                            scod_str = cau.CdmAnalyserUtils.scod_analyse(param)
                    print(f"\n{list_line}* {shut_str}\n* {mon_str}\n* {ts_str}\n* {scod_str}")

                print("_____________________________________________________")
        else:
            controller.cv.close_menu("The choice of the path is not made")
