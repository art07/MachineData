from typing import Dict


class CdmAnalyserUtils:
    is_scod_dic_made: bool = False

    shut_dic: Dict[str, str] = {
        "O": "Вiдкритий",
        "M": "Вiдсутнiй",
        "C": "Закритий",
        "U": "Невизначений (як правило це позицiя заслiнки при видачi готiвки)"
    }

    mon_dic: Dict[str, str] = {
        "P": "Presented = банкноти доступнi для клiєнта",
        "W": "Withdrawn = банкноти отриманi клiєнтом",
        "R": "Retracted = банкноти затримано",
        "N": "No = вихiд вiльний"
    }

    ts_dic: Dict[str, str] = {
        "0": "немає банкнот",
        "1": "касета",
        "2": "накопичувач",
        "3": "касета вiдбраковки",
        "4": "stop over (вихiдний тракт)",
        "5": "позицiя видачi",
        "8": "бокс для забуттiв",
        "9": "невизначене положення"
    }

    scod_dic: Dict[str, str] = {
        "01": "Помилка програмного забезпечення",
        "05": "Збiй передачi данних на ChipCard контролер",
        "06": "Збiй передачi данних на ChipCard чи невірний тип ChipCard",
        "08": "Вiдсутнiй чи пошкоджений EEPROM",
        "10": "Котроллер пошкоджений",
        "11": "Вiдсутнє фiрмове програмне забезпечення",
        "12": "Звiльнений перемикач розмiщення касового модуля",
        "13": "Касовий модуль блоковано",
        "17": "Пошкоджено ремiнну передачу клампа",
        "18": "Зажимання банкнот пiд час видачi",
        "19": "Кламп пошкоджено / блоковано",
        "20": "Перемикач одиночного вiдбракування пошкоджено / блоковано",
        "21": "Пошкодження вимiрювальної станцiї",
        "22": "Пошкоджений пiдсилювач фотодачика чи неуспiшна iнiцiалiзацiя фотодатчика",
        "23": "Диск позицiонування клампа (DCM2/SM3) пошкоджено / блоковано",
        "24": "Пошкоджений / блокований двигун МА6",
        "25": "Пошкоджений / блокований двигун DCM1",
        "26": "Пошкоджений / блокований двигун накопичувального колеса SM9",
        "28": "Пошкоджена заслiнка",
        "29": "Закритий фотодатчик, що контролює розмiщення банкнот для видачi",
        "70": "Вимiрювальна станцiя DDU не в робочому станi",
        "90": "Датчик PS1 брудний",
        "91": "Датчик PS18 брудний",
        "93": "Датчик PS2 брудний",
        "95": "Датчик PS27 брудний",
        "98": "Датчик PS28 брудний"
    }

    @staticmethod
    def make_scod_dic():
        CdmAnalyserUtils.is_scod_dic_made = True
        CdmAnalyserUtils.scod_dic.update(
            dict.fromkeys(["30", "31", "32", "33", "34", "35", "36", "37", "38", "39"],
                          "Забагато збоїв при витягуваннi банкнот з касети х"))
        CdmAnalyserUtils.scod_dic.update(
            dict.fromkeys(["40", "41", "42", "43", "44", "45", "46", "47", "48", "49"],
                          "В касетi блокованi банкноти чи недостатнiй тиск, що створює каретка"))
        CdmAnalyserUtils.scod_dic.update(
            dict.fromkeys(["50", "51", "52", "53", "54", "55", "56", "57", "58", "59"],
                          "Занадто багато поганих банкнот"))
        CdmAnalyserUtils.scod_dic.update(
            dict.fromkeys(["60", "61", "62", "63", "64", "65", "66", "67", "68", "69"], "Пошкодження касети"))
        CdmAnalyserUtils.scod_dic.update(dict.fromkeys(["71", "72", "73", "74", "75", "76", "77", "78", "79"],
                                                       "Датчик PSDx брудний чи пошкоджений"))
        CdmAnalyserUtils.scod_dic.update(
            dict.fromkeys(["80", "81", "82", "83", "84", "85", "86", "87", "88", "89"], "Датчик PSEx брудний"))

    @staticmethod
    def shut_analyse(param):
        value = param[-1]
        decryption = CdmAnalyserUtils.shut_dic[value]
        shut_str = f"Стан заслiнки касового модуля > {param} > {decryption}"
        return shut_str

    @staticmethod
    def mon_analyse(param):
        value = param[-1]
        decryption = CdmAnalyserUtils.mon_dic[value]
        mon_str = f"Стан вихiдного тракту > {param} > {decryption}"
        return mon_str

    @staticmethod
    def ts_analyse(param):
        value_from = param[-2]
        value_to = param[-1]
        decryption_from = CdmAnalyserUtils.ts_dic[value_from]
        decryption_to = CdmAnalyserUtils.ts_dic[value_to]
        ts_str = f"Останнє транспортування банкнот > {param}. Початкове положення = {decryption_from}, " \
                 f"кінцеве положення = {decryption_to}"
        return ts_str

    @staticmethod
    def scod_analyse(param):
        value = param[-2:]
        decryption = CdmAnalyserUtils.scod_dic[value]
        scod_str = f"Стан касового модуля згiдно коду на iндiкаторi > {param} > {decryption}"
        return scod_str
