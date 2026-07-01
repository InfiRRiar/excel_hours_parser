import pandas as pd
from os import listdir
from os.path import isfile, join
import os
import sys
import re


if getattr(sys, 'frozen', False):
    # Запущено как собранный .exe/.bin
    ROOT = os.path.dirname(sys.executable)
else:
    # Запущено как обычный Python-скрипт
    ROOT = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = ROOT + "/data"

res_dict = {
    "Фамилия": [],
    "Кол-во часов": []
}

splitters = r"[:-]"

def return_hours(time_gap: str):
    time_units = list(map(int, re.split(splitters, time_gap)))
    total_hours = (time_units[2] - time_units[0]) * 60 + (time_units[3] - time_units[1])
    return total_hours / 60

def main():
    excels_to_parse = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]
    for file in excels_to_parse:
        full_path_to_file = DATA_DIR + f"/{file}"
        try:
            excel_df = pd.read_excel(full_path_to_file, engine="openpyxl")
        except Exception as e:
            print(f"Не удалось прочитать файл {file}: {e}")
            continue
        
        total_hours = excel_df["Время"].apply(return_hours).sum()
        res_dict["Фамилия"].append(file.split(".")[0])
        res_dict["Кол-во часов"].append(str(total_hours / 4).replace(",", "."))
        
    pd.DataFrame.from_dict(res_dict).to_excel(f"{ROOT}/res.xlsx", engine="openpyxl")

if __name__ == "__main__":
    main()