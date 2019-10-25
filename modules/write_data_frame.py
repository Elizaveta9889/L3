import pandas as pd

from modules import analize_vacancy as av


# Считать csv в data_frame
def read_csv(file_name):
    return pd.read_csv(file_name + ".csv", sep=';', low_memory=False, index_col=0)


# Сохранить data_frame в csv файл
def save_data_frame(data_frame, file_name, count=None):
        data_frame.to_csv(file_name + (str(count) if count is not None else '') + ".csv", sep=';', encoding='UTF-8-sig')


# Запись нескольких data_frame в csv файл
def write_groups(all_groups, file_name):
    i = 1
    for gr in all_groups:
        save_data_frame(gr, file_name, i)
        i += 1


# Запись информации по каждой группе в csv файл
def write_groups_info(all_groups, param_group_by, file_name):
    i = 1
    for gr in all_groups:
        save_data_frame(av.get_info(gr, param_group_by), file_name, i)
        i += 1