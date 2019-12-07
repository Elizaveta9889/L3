import datetime as dt

import pandas as pd
import pytz
from sklearn.preprocessing import LabelEncoder


# Заполнить nan
def fillna(data_frame, column, value):
    data_frame[column] = data_frame[column].fillna(value)


# Посчитать количество каждого уникального
def get_unique_values(values):
    values_dict = {}
    for value in values:
        if str(value) != 'nan':
            values_dict[value] = values_dict.get(value, 0) + 1
    return values_dict


# Посчитать количество уникальных навыков
def get_unique_skills(all_skills):
    skills_dict = dict()
    for skills in all_skills:
        if str(skills) != 'nan':
            for skill in skills.split(';'):
                skills_dict[skill] = skills_dict.get(skill, 0) + 1
    return skills_dict


# Посчитать прошедшее количество дней
def get_days_count(dates):
    date = pd.to_datetime(dates, utc=True).dt.tz_convert('US/Eastern')
    return (dt.datetime.now(pytz.timezone('US/Eastern')) - date).astype('timedelta64[D]')


# Получить информацию по вакансии
def get_info(data_frame, unique):
    unique_dict = []
    vacancy = dict()
    vacancy[unique + 's'] = str(get_unique_values(data_frame[unique]))
    days = get_days_count(data_frame['published_at'])
    vacancy['minCountDays'] = days.min()
    vacancy['maxCountDays'] = days.max()
    vacancy['avgCountDays'] = days.mean()
    vacancy['experience'] = data_frame['experience'].value_counts().to_string().replace('\n', ';')
    vacancy['employment'] = data_frame['employment'].value_counts().to_string().replace('\n', ';')
    vacancy['schedule'] = data_frame['schedule'].value_counts().to_string().replace('\n', ';')
    vacancy['skills'] = str(get_unique_skills(data_frame['key_skills']))
    unique_dict.append(vacancy)
    return pd.DataFrame(unique_dict)


# Получить средние зарплаты по сгруппированным значениям
def count_salary(data_frame, group_by):
    categories = pd.unique(data_frame[group_by])
    for category in categories:
        unique_cities = data_frame[data_frame[group_by] == category]
        avg_min = unique_cities[unique_cities["min_salary"] != 0]["min_salary"].mean()
        avg_max = unique_cities[unique_cities["max_salary"] != 0]["max_salary"].mean()
        data_frame.update(data_frame[data_frame[group_by] == category]["min_salary"].replace(0, round(avg_min, 2)))
        data_frame.update(data_frame[data_frame[group_by] == category]["max_salary"].replace(0, round(avg_max, 2)))


# Получить несколько самых популярных навыков
def get_popular_skills(data_frame, params, num):
    skills = get_unique_skills(data_frame["key_skills"])
    for skill in params:
        if skill.lower() in skills:
            skills[skill.lower()] += 1000
    return ';'.join((sorted(skills, key=skills.get, reverse=True))[0:min(len(skills), num)])


# Получить несколько самых популярных навыков
def get_popular_values(data_frame, field, num):
    skills = get_unique_values(data_frame[field])
    return ';'.join((sorted(skills, key=skills.get, reverse=True))[0:min(len(skills), num)])


# Нормализация
def normalize_column(data_frame, column_name):
    data_days_from_publication = data_frame[column_name]
    min_values = data_days_from_publication.min()
    max_values = data_days_from_publication.max()
    data_frame[column_name] = ((data_frame[column_name] - min_values) / (max_values - min_values)).fillna(0)


# Дескритизация
def discretize_column(data_frame, column_name, num):
    step = (data_frame[column_name].max() - data_frame[column_name].min()) / num
    data_frame[column_name] = data_frame[column_name] // step


def dummy_skills(group, params, num):
    skills = get_popular_skills(group, params, num).split(';')
    skills.append("Другие навыки")
    for skill in skills:
        group[skill] = 0
    for vacancy in group.itertuples():
        for vacancy_skill in str(vacancy.key_skills).split(';'):
            for param in params:
                if param.lower() in skills:
                    if param.lower() in vacancy_skill:
                        group.update(
                            group[group["id"] == vacancy.id][param.lower()].replace(0, 1))
            if vacancy_skill in skills:
                group.update(
                    group[group["id"] == vacancy.id][vacancy_skill].replace(0, 1))
            else:
                group.update(
                    group[group["id"] == vacancy.id]["Другие навыки"].replace(0, 1))


def dummy(data_frame, field, num):
    values = get_popular_values(data_frame, field, num).split(';')
    values.append("Другие города")
    for value in values:
        data_frame[value] = 0
        data_frame.loc[data_frame[field] == value, value] = 1
    data_frame.loc[~data_frame[field].isin(values), "Другие города"] = 1


def all_numerical_to_int(data_frame, ignore=None):
    numerical_values = []
    if ignore is None:
        numerical_values = [col for col in data_frame.columns if
                        data_frame[col].dtype.name == 'float64' or
                            data_frame[col].dtype.name == 'int64']
    else:
        numerical_values = [col for col in data_frame.columns if
                            (data_frame[col].dtype.name == 'float64' or
                            data_frame[col].dtype.name == 'int64') and
                            not (data_frame[col].name in ignore)]
    data_frame[numerical_values] = data_frame[numerical_values].astype(int)


def divide_data_frame(data_frame, data_frame_1, data_frame_2, percent):
    percent = len(data_frame) * percent/100
    list1 = []
    list2 = []
    count = 0
    for vacancy in data_frame.itertuples():
        if count < percent:
            list1.append(vacancy)
        else:
            list2.append(vacancy)
        count += 1
    data_frame_1 = pd.DataFrame(list1)
    data_frame_2 = pd.DataFrame(list2)


def transform_categories(data_frame):
    le = LabelEncoder()
    le.fit(data_frame['group'])
    data_frame['group'] = le.transform(data_frame['group'])