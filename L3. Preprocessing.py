import pandas as pd

from modules import analize_vacancy as av
from modules import divide_vacancies as dv
from modules import write_data_frame as w_df

df = w_df.read_csv("Vacancies")
av.fillna(df, "min_salary", 0)
av.fillna(df, "max_salary", 0)
df["key_skills"] = df["key_skills"].replace(r'(?<=[;])\s+', '', regex=True)
# Изменение колонки published_at на days_from_publication (количество дней)
df["published_at"] = av.get_days_count(df["published_at"])
df.rename(columns={"published_at": "days_from_publication"}, inplace=True)
# Нормализация days_from_publication
av.normalize_column(df, "days_from_publication")
# Делим на группы
groups = dv.get_groups_by_type(df)
for group in groups:
    group["values"] = pd.DataFrame(group["values"])
    # По средней зарплате по городу
    av.count_salary(group["values"], "city")
    # Самые популярные навыки
    group["values"].update(group["values"]["key_skills"].fillna(av.get_popular_skills(group["values"], 5)))
df = pd.DataFrame()
for group in groups:
    df = df.append(pd.DataFrame(group["values"]))
# Дескритизация min_salary и max_salary
av.discretize_column(df, "min_salary", 10)
av.discretize_column(df, "max_salary", 10)
# Dummy кодирование
av.dummy(df, "city", 4)
df = pd.get_dummies(data=df, columns=['experience', 'schedule', 'employment'])
groups = dv.update_groups(df, groups)
for group in groups:
    # Dummy-кодирование навыков
    av.dummy_skills(group["values"], 10)
    av.all_numerical_to_int(group["values"], ["days_from_publication", "id"])
    pd.DataFrame(group["values"])\
       .to_csv("L3. ProgrammerGroups/" + group["name"] + ".csv", sep=';', encoding='UTF-8-sig')
