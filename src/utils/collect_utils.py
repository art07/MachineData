import shutil
import subprocess
import os
import winreg
import model as m
from pathlib import Path


class CollectUtils:
    @staticmethod
    def collection_journals(data_lab: 'm.DataLab'):
        print("Start to collect journals. Waiting time 1-4 minutes...")

        for machine_doc in data_lab.get_CHOSEN_machine_docs():
            src: str = str(machine_doc)
            if src.find("TPCA") == -1:
                dst = str(Path.joinpath(data_lab.get_machine_data_dir(), machine_doc.name))
            else:
                dst = str(Path.joinpath(data_lab.get_TPCA_dir(), machine_doc.name))

            if machine_doc.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copyfile(src, dst)

        print("Journals OK\n")

    @staticmethod
    def get_ip_data(data_lab: 'm.DataLab'):
        print("Start getting IP data...")

        path_obj: Path = data_lab.get_machine_data_dir().joinpath('ip.txt')
        my_subprocess = subprocess.check_output("ipconfig", encoding='oem')
        with open(str(path_obj), "w") as out_file:
            out_file.write(my_subprocess)

        print("IP OK\n")

    @staticmethod
    def save_REG_branches(data_lab: 'm.DataLab'):
        print("Start to collect reg branches...")

        reg_branch_list = data_lab.get_reg_branch_list()
        for i in range(4):
            CollectUtils.__get_reg_branches_helper(reg_branch_list[i].branch_path, str(data_lab.get_REG_dir().joinpath(reg_branch_list[i].full_branch_name)), reg_branch_list[i].branch_name)

        print("Reg branches OK\n")

    @staticmethod
    def __get_reg_branches_helper(regedit_branch: str, path_to_save_branch: str, branch_name: str):
        print(f"From registry getting: {branch_name}")
        os.system(f'cmd /c reg export {regedit_branch} {path_to_save_branch} /reg:64')

    @staticmethod
    def get_reg_values(data_lab: 'm.DataLab'):
        print("Start to collect main reg keys...")

        super_str_names_values = "Registry key = Registry value\n\n"
        reg_param_list = data_lab.get_reg_param_list()
        for reg_param_obj in reg_param_list:
            reg_param_obj.reg_value = CollectUtils.__get_reg_values_helper(reg_param_obj.param_name, reg_param_obj.param_path)
            if reg_param_obj.reg_value != 'None':
                name_value_str = f"{reg_param_obj.param_name} = {reg_param_obj.reg_value}"
                print(name_value_str)
                super_str_names_values += f"{name_value_str}\n"

        file: str = str(data_lab.get_REG_dir().joinpath("reg_values.txt"))
        with open(file, "w", encoding="utf-8") as out_file:
            out_file.write(super_str_names_values)

        print("Reg keys OK\n")

    @staticmethod
    def __get_reg_values_helper(key: str, path: str):
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            value, regtype = winreg.QueryValueEx(registry_key, key)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError:
            return "None"
