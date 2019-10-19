import pandas as pd
import re
import datetime as dt
import pytz


def clear_text(text):
    regex = re.compile('[ ,:()/-]')
    return re.sub(regex, '', text)


def add_to_group(group, vacancy):
    for gr in group["param"]:
        s = clear_text(vacancy.name)
        if s.upper().find(gr) != -1:
            group["values"].append(vacancy)
            return 1
    return 0


def add_column_days(data_frame):
    date = pd.to_datetime(df['published_at'], utc=True).dt.tz_convert('US/Eastern')
    data_frame["days"] = (dt.datetime.now(pytz.timezone('US/Eastern')) - date).astype('timedelta64[D]')


def fillna(data_frame, column, value):
    data_frame[column] = data_frame[column].fillna(value)


def count_salary(data_frame):
    categories = pd.unique(data_frame["city"])
    for category in categories:
        unique_cities = data_frame[data_frame["city"] == category]
        avg_min = unique_cities[unique_cities["min_salary"] != 0]["min_salary"].mean()
        avg_max = unique_cities[unique_cities["max_salary"] != 0]["max_salary"].mean()
        data_frame.update(data_frame[data_frame["city"] == category]["min_salary"].replace(0, round(avg_min, 2)))
        data_frame.update(data_frame[data_frame["city"] == category]["max_salary"].replace(0, round(avg_max, 2)))


def get_skills(data_frame):
    skills = dict()
    for vacancy in data_frame.itertuples():
        if str(vacancy.key_skills) != 'nan':
            for skill in vacancy.key_skills.split(';'):
                skills[skill] = skills.get(skill, 0) + 1
    str_skills = \
        ';'.join((sorted(skills, key=skills.get, reverse=True))[0:min(len(skills), 5)])
    data_frame.update(data_frame["key_skills"].fillna(str_skills))


df = pd.read_csv("Vacancies.csv", sep=';', low_memory=False, index_col=0)
fillna(df, "min_salary", 0)
fillna(df, "max_salary", 0)
fillna(df, "experience", "не требуется")
fillna(df, "schedule", "любой тип")
fillna(df, "employment", "любой тип")
add_column_days(df)
groups = [
    {"name": "tester", "param": ["ТЕСТ", "TEST"], "values": []},
    {"name": "net", "param": ["++", "#", ".NET"], "values": []},
    {"name": "fullstack", "param": ["FULLSTACK", "WEB", "ВЕБ", "САЙТ"], "values": []},
    {"name": "frontend", "param": ["FRONTEND", "JS", "JAVASCRIPT", "ФРОНТЕНД", "HTML", "GO", "front"], "values": []},
    {"name": "web_frameworks", "param": ["ANGULAR", "REACT", "RAILS", "RUBY"], "values": []},
    {"name": "backend", "param": ["BACKEND", "БЭКЕНД", "БЭК"], "values": []},
    {"name": "delphi", "param": ["DELPHI", "ДЕЛФИ"], "values": []},
    {"name": "java", "param": ["JAVA", "ДЖАВА", "ЯВА", "KOTLIN", "КОТЛИН"], "values": []},
    {"name": "ios", "param": ["IOS", "SWIFT", "МОБИЛЬ"], "values": []},
    {"name": "android", "param": ["ANDROID", "АНДРОИД"], "values": []},
    {"name": "erlang", "param": ["ERLANG"], "values": []},
    {"name": "perl", "param": ["PERL"], "values": []},
    {"name": "python", "param": ["PYTHON", "ПИТОН"], "values": []},
    {"name": "PHP", "param": ["PHP"], "values": []},
    {"name": "1C", "param": ["1C", "1С", "БИТРИКС", "BITRIX"], "values": []},
    {"name": "DB", "param": ["БАЗ", "БД", "SQL", "POSTGRES", "ORACLE", "FOXPRO", "OEBS"], "values": []},
    {"name": "engineer", "param": ["ИНЖЕНЕР", "COMPUTERVISION", "ПЛИС", "МИКРОКОНТР", "FPGA", "ДЕССИНАТОР"],
     "values": []},
    {"name": "developer", "param": ["ПРОГРАММИСТ", "РАЗРАБОТЧИК", "DEVELOPER"], "values": []},
    {"name": "manager", "param": ["МЕНЕДЖЕР"], "values": []}
]
for vacancy in df.itertuples():
    for group in groups:
        if add_to_group(group, vacancy) == 1:
            break

for group in groups:
    for value in group["values"]:
        df = df[df["id"] != value.id]

for group in groups:
    group["values"] = pd.DataFrame(group["values"])
    count_salary(group["values"])
    get_skills(group["values"])

df.to_csv("Vacancies1.csv", sep=';', encoding='UTF-8-sig')
for group in groups:
    pd.DataFrame(group["values"]).to_csv("L2. ProgrammerGroups/" + group["name"] + ".csv", sep=';', encoding='UTF-8-sig')
