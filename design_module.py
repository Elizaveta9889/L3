import pandas as pd

skills_signs = [
    {
        "name": "web_skill",
        "params": ["FRONTEND", "ФРОНТЕНД", "FRONT", "ANGULAR", "REACT", "RAILS", "RUBY", "ФРОНТЕНД",
                   "HTML", "WEB", "ВЕБ", "САЙТ", "GO", "PHP", "JS", "JAVASCRIPT", "BACKEND", "БЭКЕНД", "БЭК"],
        "columns": []
    },
    {
        "name": "1с_skill",
        "params": ["1C", "1С", "БИТРИКС", "BITRIX"],
        "columns": []
    },
    {
        "name": "mobile_skill",
        "params": ["IOS", "SWIFT", "МОБИЛЬН", "MOBILE", "ANDROID", "АНДРОИД"],
        "columns": []
    }
]


def get_columns(data_frame):
    for el in skills_signs:
        for i in range(0, len(data_frame.columns)):
            for skill in el["params"]:
                if str(data_frame.iloc[:, i].name).upper().find(skill) != -1:
                    el["columns"].append(data_frame.iloc[:, i].name)


def add_salary_column(data_frame):
    #data_frame["salary_scatter"] = data_frame.apply(lambda x: x["max_salary"] - x["min_salary"], axis=1)
    new_column = []
    for i in range(0, len(data_frame)):
        new_column.append(abs(data_frame.iloc[i]["max_salary"] - data_frame.iloc[i]["min_salary"]))
    data_frame["salary_scatter"] = pd.Series(new_column, index=data_frame.index)


def add_skill_signs(data_frame):
    get_columns(data_frame)
    for el in skills_signs:
        new_column = []
        for i in range(0, len(data_frame)):
            sum = 0
            for column in el["columns"]:
                sum += data_frame.iloc[i][column]
            new_column.append(sum)
        data_frame[el["name"]] = pd.Series(new_column, index=data_frame.index)
