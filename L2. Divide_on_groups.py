import pandas as pd
from modules import analize_vacancy as av
from modules import divide_vacancies as dv
from modules import write_data_frame as w_df

# Считывание всех вакансий из файла
df = w_df.read_csv("Vacancies")
# Заполнение nan
av.fillna(df, "min_salary", 0)
av.fillna(df, "max_salary", 0)
av.fillna(df, "experience", "не требуется")
av.fillna(df, "schedule", "любой тип")
av.fillna(df, "employment", "любой тип")
# Добавление колонки days, равное количеству дней с даты публикации
df["days"] = av.get_days_count(df["published_at"])
# Получить группы по типу вакансии
groups = dv.get_groups_by_type(df)
# Удаляем добавленные в группы элементы из data_frame (для проверки)
for group in groups:
    for value in group["values"]:
        df = df[df["id"] != value.id]
w_df.save_data_frame(df, "Vacancies1")
# Заполняем пустые значения
for group in groups:
    group["values"] = pd.DataFrame(group["values"])
    # По средней зарплате по городу
    av.count_salary(group["values"], "city")
    # Самые популярные навыки
    group["values"].update(group["values"]["key_skills"].fillna(av.get_popular_skills(group["values"], 5)))
# Записываем группы в файл
for group in groups:
    pd.DataFrame(group["values"])\
        .to_csv("L2. ProgrammerGroups/" + group["name"] + ".csv", sep=';', encoding='UTF-8-sig')
