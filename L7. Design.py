from sklearn.feature_selection import VarianceThreshold
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.ensemble import RandomForestClassifier
from modules import files_work_data_frame as fw_df
from modules import design_module as dm
from modules import analize_vacancy as av
import pandas as pd
from modules import learning_model as lm


df = fw_df.read_files_to_df("L3. ProgrammerGroups")
df = df.fillna(0)
dm.add_salary_column(df)
dm.add_skill_signs(df)
#df.to_csv("L7. Design/Vacancies.csv", sep=';', encoding='UTF-8-sig')

av.transform_categories(df)
df = df.fillna(0)
av.all_numerical_to_int(df, ["days_from_publication", "id"])

#VarianceThreshold
"""
df = lm.clear_df_columns(df)
selector = VarianceThreshold(0.05)
selector.fit(df)
df = df[df.columns[selector.get_support(indices=True)]]
df.to_csv("L7. Design/VarianceThreshold.csv", sep=';', encoding='UTF-8-sig')
"""

new_df = fw_df.read_files_to_df("L4. ProgrammerGroups")
new_df = new_df.fillna(0)

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
dm.add_skill_signs(new_df)
#new_df.to_csv("L7. Design/NewVacancies.csv", sep=';', encoding='UTF-8-sig')
# Удалить ненужные признаки
tmp = new_df
tmp = tmp.drop(['group'], axis=1)
#df = lm.clear_df_columns(df)
#new_df = lm.clear_df_columns(new_df)
# Определить лучший классификатор
target = df.group
df = df.drop(['group'], axis=1)
# Предсказать группы
groups = new_df['group']
target_t = new_df.group
new_df = new_df.drop(['group'], axis=1)
"""
#SequentialFeatureSelector
df = lm.clear_df_columns(df)
new_df = lm.clear_df_columns(new_df)
selector = SFS(RandomForestClassifier(n_estimators=100), k_features=50, forward=False, verbose=2, scoring='accuracy')
sfs = selector.fit(df, target)
df = df[list(sfs.k_feature_names_)]
df.to_csv("L7. Design/SequentialFeatureSelector.csv", sep=';', encoding='UTF-8-sig')
"""
tmp['predicted_group'] = lm.predict(new_df, df, target, new_df, target_t)
tmp['factual_group'] = groups
tmp['gr'] = gr
#tmp.to_csv("L7. Design/PredictedGroups.csv", sep=';', encoding='UTF-8-sig')
#tmp.to_csv("L7. Design/VarianceThresholdGroups.csv", sep=';', encoding='UTF-8-sig')
