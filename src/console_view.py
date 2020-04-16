"""The module contains the ConsoleView class for working with the main menu of the program."""

from src.controller import AppController
import pathlib
import sys
from typing import List


class ConsoleView:
    def __init__(self):
        self.current_MACHINE: str = ""
        self.USER_CHOICE: int = 0

        self.controller: AppController = AppController(self)
        self.machines_list: List[str] = [
            "ATM",
            "TERMINAL"
        ]
        print("Program ver. 1.2")
        self.define_machine()
        self.main_menu()

    def define_machine(self):
        if pathlib.Path("C:/TPCA/Log").is_dir():
            self.current_MACHINE = self.machines_list[1]
        else:
            self.current_MACHINE = self.machines_list[0]

    def main_menu(self):
        if self.current_MACHINE == self.machines_list[0]:  # If ATM
            s = f"{self.current_MACHINE} detected\nGet {self.current_MACHINE} data - 1\nCDM SCOD Analyser - " \
                f"2\nExit - 3\nINPUT>>> "
        else:  # If TERMINAL
            s = f"{self.current_MACHINE} detected\nGet {self.current_MACHINE} data - 1\nExit - 2\nINPUT>>> "

        while True:
            try:
                loc_var_user_choice = int(input(s))
                if 0 < loc_var_user_choice < (4 if self.current_MACHINE == self.machines_list[0] else 3):
                    self.USER_CHOICE = loc_var_user_choice
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("\nInvalid input. Try again\n")

        self.controller.action()

    def close_menu(self, s: str):
        print(s)
        while True:
            try:
                str_answer = input("Close program y/n?\n>>> ")
                if str_answer == "y" or str_answer == "n":
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("\nInvalid input. Try again\n")

        if str_answer == "n":
            self.main_menu()
        else:
            sys.exit()
