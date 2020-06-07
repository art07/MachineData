"""The module contains the ConsoleView class for working with the main menu of the program."""

import sys
from typing import List

from controller import AppController


class ConsoleView(object):
    def __new__(cls, *args, **kwargs):
        # hasattr возвращает флаг, указывающий на то, содержит ли объект указанный атрибут.
        if not hasattr(cls, 'single_object_of_consoleview'):  # Если нет ОБЪЕКТА класса, тогда его нужно создать.
            cls.single_object_of_consoleview = super(ConsoleView, cls).__new__(cls)
        return cls.single_object_of_consoleview

    def __init__(self):
        print("MachineData. Ver. 1.3")

        self.available_machines: List[str] = [
            "ATM",
            "Terminal"
        ]
        self.__MENU_TEXT = f"\nMAIN menu:\n0 - Exit\n1 - {self.available_machines[0]}\n2 - {self.available_machines[1]}\n3 - CDM SCOD Analyser\nINPUT>>> "

        # self.CURRENT_MACHINE: str = ""
        self.__USER_CHOICE: int = 0

        self.controller: AppController = AppController(self)
        self.main_menu()

    def main_menu(self):
        # Цикл основного меню.
        while True:
            try:
                loc_var_user_choice = int(input(self.__MENU_TEXT))
                if 0 <= loc_var_user_choice < 4:
                    self.__USER_CHOICE = loc_var_user_choice
                    break
                else:
                    print(f"Invalid input. Allowable range from 0 to {len(self.available_machines) + 1}.")
            except ValueError:
                print("Invalid input. Only integer type allowed.")

        self.controller.action(self.__USER_CHOICE)

    def close_menu(self, s: str):
        print(s)

        # Цикл меню закрытия программы.
        while True:
            str_answer = input("Close program y/n? >>> ")
            if str_answer == "y" or str_answer == "Y":
                sys.exit()
            elif str_answer == "n" or str_answer == "N":
                self.main_menu()
            else:
                print("Invalid input. Try again.")
