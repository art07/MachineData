import shutil
import subprocess
import os
import winreg
import pathlib
from src.model import DataLab
from pathlib import Path


class CollectUtils:

    @staticmethod
    def create_list_copying_folders(data_lab: DataLab):
        chosen_machine_docs = []
        for dic_key in data_lab.get_all_machines_docs():
            chosen_machine_docs.append(data_lab.get_all_machines_docs().get(dic_key)) if data_lab.get_all_machines_docs().get(dic_key) is not None \
                else CollectUtils.do_nothing()
        data_lab.set_CHOSEN_machine_docs(chosen_machine_docs)

    @staticmethod
    def do_nothing():
        pass

    @staticmethod
    def create_TPCA(data_lab: DataLab):
        path_obj = pathlib.Path.joinpath(data_lab.get_machine_data_dir(), "TPCA")
        path_obj.mkdir()
        data_lab.set_TPCA_dir(path_obj)

    @staticmethod
    def collection_journals(data_lab: DataLab):
        print("Start to collect journals. Waiting time 1-4 minutes...")
        for machine_doc in data_lab.get_CHOSEN_machine_docs():
            src = str(machine_doc)
            if src.find("TPCA") == -1:
                dst = str(pathlib.Path.joinpath(data_lab.get_machine_data_dir(), machine_doc.name))
            else:
                dst = str(pathlib.Path.joinpath(data_lab.get_TPCA_dir(), machine_doc.name))

            if machine_doc.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copyfile(src, dst)
        print("Journals OK")

    @staticmethod
    def get_ip_data(machine_data_dir: Path):
        print("Start getting IP data...")
        file_obj = pathlib.Path.joinpath(machine_data_dir, "ip.txt")
        my_subprocess = subprocess.check_output("ipconfig", encoding='oem')
        with open(str(file_obj), "w") as out_file:
            out_file.write(my_subprocess)
        print("IP OK")

    @staticmethod
    def create_REG(data_lab: DataLab):
        path_obj = pathlib.Path(data_lab.get_machine_data_dir(), "REG")
        path_obj.mkdir()
        data_lab.set_REG_dir(path_obj)

    @staticmethod
    def save_REG_branches(data_lab: DataLab):
        print("Start to collect reg branches...")
        for_x64 = "/reg:64"
        for i in range(4):
            if i == 0:
                str_path = str(pathlib.Path.joinpath(data_lab.get_REG_dir(), "WincorNixdorf.reg"))
                print(str_path)
                os.system(
                    f'cmd /c reg export "HKEY_LOCAL_MACHINE\\SOFTWARE\\Wincor Nixdorf" {str_path} {for_x64}')
            elif i == 1:
                str_path = str(pathlib.Path.joinpath(data_lab.get_REG_dir(), "XFS.reg"))
                print(str_path)
                os.system(f'cmd /c reg export HKEY_LOCAL_MACHINE\\SOFTWARE\\XFS {str_path} {for_x64}')
            elif i == 2:
                str_path = str(pathlib.Path.joinpath(data_lab.get_REG_dir(), "XFS_ROOT.reg"))
                print(str_path)
                os.system(f'cmd /c reg export HKEY_CLASSES_ROOT\\WOSA/XFS_ROOT {str_path} {for_x64}')
            elif i == 3:
                str_path = str(pathlib.Path.joinpath(data_lab.get_REG_dir(), "CSCCOMM.reg"))
                print(str_path)
                os.system(f'cmd /c reg export "HKEY_LOCAL_MACHINE\\SOFTWARE\\Wincor Nixdorf\\CSC-W32\\CurrentVersion\\CSCCOMM" {str_path} {for_x64}')
        print("Reg branches OK")

    @staticmethod
    def get_reg_values(cv, data_lab: DataLab):
        print("Start to collect main reg keys...")
        super_str_names_values = ""
        if cv.current_MACHINE == cv.machines_list[1]:
            reg_param_list = data_lab.get_reg_param_list()
        else:
            reg_param_list = data_lab.get_reg_param_list()[:5]
        for reg_param in reg_param_list:
            reg_param.reg_value = CollectUtils.get_reg_values_helper(reg_param.param_name, reg_param.param_path)
            super_str_names_values += f"{reg_param.param_name} = {reg_param.reg_value}\n"

        file_obj = pathlib.Path.joinpath(data_lab.get_REG_dir(), "reg_values.txt")
        with open(str(file_obj), "w", encoding="utf-8") as out_file:
            out_file.write(super_str_names_values)
        print("Reg keys OK")

    @staticmethod
    def get_reg_values_helper(key: str, path: str):
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0,
                                          winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            value, regtype = winreg.QueryValueEx(registry_key, key)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError:
            return "None"
