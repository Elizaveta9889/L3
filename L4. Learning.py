import pandas as pd
import glob, os

from modules import analize_vacancy as av
from modules import files_work_data_frame as fw_df
from modules import learning_model as lm


# Считать все группы в dataframe
df = fw_df.read_files_to_df("L3. ProgrammerGroups")
av.transform_categories(df)
df = df.fillna(0)
av.all_numerical_to_int(df, ["days_from_publication", "id"])
# Считать новые группы
new_df = fw_df.read_files_to_df("L4. ProgrammerGroups")
gr = new_df["group"]
av.transform_categories(new_df)
new_df = new_df.fillna(0)
# Добавить нужные признаки
tmp = pd.DataFrame()
for column in df:
    if column in new_df.columns.values:
        tmp[column] = new_df[column]
    else:
        tmp[column] = 0
for vacancy in new_df.itertuples():
    for skill in vacancy.key_skills.split(';'):
        if skill in tmp.columns.values:
            tmp.update(tmp[tmp["id"] == vacancy.id][skill].replace(0, 1))
av.all_numerical_to_int(tmp, ["days_from_publication", "id"])
new_df = tmp

# Удалить ненужные признаки
tmp = new_df
tmp = tmp.drop(['group'], axis=1)
df = lm.clear_df_columns(df)
new_df = lm.clear_df_columns(new_df)
# Определить лучший классификатор
target = df.group
df = df.drop(['group'], axis=1)
#lm.find_the_best_classifier(train, target, 0.3)
# Предсказать группы
groups = new_df['group']
target_t = new_df.group
new_df = new_df.drop(['group'], axis=1)
tmp['predicted_group'] = lm.predict(new_df, df, target, new_df, target_t)
tmp['factual_group'] = groups
tmp['gr'] = gr
tmp.to_csv("Groups_vacancies11.csv", sep=';', encoding='UTF-8-sig')