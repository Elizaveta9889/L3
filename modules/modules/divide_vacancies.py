import pandas as pd

import modules.clear_text as ct

groups = [
    {"name": "tester", "param": ["ТЕСТ", "TEST"], "values": []},
    {"name": "web_programmer", "param": ["GO", "PHP", "JS", "JAVASCRIPT", "BACKEND", "БЭКЕНД", "БЭК"], "values": []},
    {"name": "web_front",
     "param": ["FRONTEND", "ФРОНТЕНД", "FRONT", "ANGULAR", "REACT", "RAILS", "RUBY", "FRONTEND", "ФРОНТЕНД", "FRONT",
               "HTML", "WEB", "ВЕБ", "САЙТ"], "values": []},
    {"name": "delphi", "param": ["DELPHI", "ДЕЛФИ"], "values": []},
    {"name": "java", "param": ["JAVA", "ДЖАВА", "ЯВА", "KOTLIN", "КОТЛИН"], "values": []},
    {"name": "ios", "param": ["IOS", "SWIFT", "МОБИЛЬ"], "values": []},
    {"name": "android", "param": ["ANDROID", "АНДРОИД"], "values": []},
    {"name": "erlang", "param": ["ERLANG"], "values": []},
    {"name": "perl", "param": ["PERL"], "values": []},
    {"name": "1C", "param": ["1C", "1С", "БИТРИКС", "BITRIX"], "values": []},
    {"name": "DB", "param": ["БАЗ", "БД", "SQL", "POSTGRES", "ORACLE", "FOXPRO", "OEBS"], "values": []},
    {"name": "manager", "param": ["МЕНЕДЖЕР"], "values": []},
    {"name": "developer_engineer",
     "param": ["PYTHON", "ПИТОН", "ИНЖЕНЕР", "COMPUTERVISION", "ПРОГРАММИСТ", "РАЗРАБОТЧИК", "DEVELOPER", "ПЛИС",
               "LINUX", "МИКРОКОНТР", "++", "#", ".NET", "QT"], "values": []},
]


# Разбить на группы по зарплате
def get_groups_salary(data_frame, group_by, num):
    step = (data_frame[group_by].max() - data_frame[group_by].min()) / num
    groups = []
    salary = data_frame[group_by].min()
    count = 0
    while data_frame[group_by].min() <= salary <= data_frame[group_by].max() - step:
        count += 1
        tmp = data_frame[(data_frame[group_by] > salary) & (data_frame[group_by] <= salary + step)]
        groups.append(tmp)
        salary += step
    return groups


# Разбить на группы по названию
def get_groups_name(data_frame, group_by):
    categories = pd.unique(data_frame[group_by])
    groups = []
    count = 0
    for category in categories:
        count += 1
        tmp = data_frame[data_frame[group_by] == category]
        groups.append(tmp)
    return groups


# Добавить вакансию, подходящую по параметру
def add_to_group_by_name(group, vacancy):
    for gr in group["param"]:
        s = ct.remove_unnecessary_symbols(vacancy.name)
        if s.upper().find(gr) != -1:
            group["values"].append(vacancy)
            return 1
    return 0


def get_groups_by_type(data_frame):
    for vacancy in data_frame.itertuples():
        for group in groups:
            if add_to_group_by_name(group, vacancy) == 1:
                break
    tmp = []
    for group in groups:
        if len(group["values"]) != 0:
            tmp.append(group)
    groups.clear()
    for group in tmp:
        groups.append(group)
    return groups


def add_group_name(group):
    group["values"]["group"] = group["name"]


# Обновление groups
def update_groups(data_frame, all_groups):
    for group in all_groups:
        new_gr = pd.DataFrame()
        for value in group["values"].itertuples():
            new_gr = new_gr.append(data_frame[data_frame["id"] == value.id])
        group["values"] = new_gr
    return all_groups
