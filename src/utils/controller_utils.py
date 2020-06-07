from pathlib import Path
from tkinter import Tk, filedialog
import controller as c
import model as m
from typing import List


class ControllerUtils:

    @staticmethod
    def create_MAIN_dir(controller: 'c.AppController'):
        print(f"Choose directory (in this directory will be created folder > {controller.MAIN_FOLDER_NAME} < for collecting data)")
        chosen_path: str = ControllerUtils.window_helper(path_obj=Path.home(), doc="dir")
        if chosen_path != '':
            base_dir: Path = Path(chosen_path)
            controller.data_lab.set_base_dir(base_dir)
            machinedata_dir: Path = base_dir.joinpath(controller.MAIN_FOLDER_NAME)
            controller.data_lab.set_machine_data_dir(machinedata_dir)
            if not controller.data_lab.get_machine_data_dir().is_dir():
                controller.data_lab.get_machine_data_dir().mkdir()
                if controller.data_lab.get_machine_data_dir().is_dir():
                    print(f"{controller.MAIN_FOLDER_NAME} created successfully! "
                          f"Full path >>> {str(controller.data_lab.get_machine_data_dir())}\n")
                else:
                    controller.cv.close_menu(f"Failed to create a folder {controller.MAIN_FOLDER_NAME}.")
            else:
                controller.cv.close_menu(f"{controller.MAIN_FOLDER_NAME} already EXISTS. Delete old {controller.MAIN_FOLDER_NAME} before start new attempt")
        else:
            controller.cv.close_menu("The choice of the path is NOT made.")

    @staticmethod
    def window_helper(path_obj: Path, doc: str):
        window = Tk()
        chosen_path: str = ""
        if doc == "dir":
            chosen_path = filedialog.askdirectory(title="Choose directory", initialdir=path_obj)
        elif doc == "file":
            chosen_path = filedialog.askopenfilename(title="Choose TRC.XML file", initialdir=path_obj, filetypes=[("cdm log files", "*.TRC.XML")])
        window.destroy()
        return chosen_path

    @staticmethod
    def create_REG_dir(data_lab: 'm.DataLab'):
        path_obj: Path = data_lab.get_machine_data_dir().joinpath('REG')
        path_obj.mkdir()
        data_lab.set_REG_dir(path_obj)

    @staticmethod
    def create_list_copying_folders(data_lab: 'm.DataLab'):
        available_machine_docs: List[Path] = []
        for dic_key in data_lab.get_all_machines_docs():
            if data_lab.get_all_machines_docs()[dic_key]:
                available_machine_docs.append(data_lab.get_all_machines_docs()[dic_key])
        data_lab.set_available_machine_docs(available_machine_docs)

    @staticmethod
    def create_TPCA_dir(data_lab: 'm.DataLab'):
        path_obj: Path = data_lab.get_machine_data_dir().joinpath('TPCA')
        path_obj.mkdir()
        data_lab.set_TPCA_dir(path_obj)
