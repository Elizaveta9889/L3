from modules import clustering as cm
from modules import analize_vacancy as av
from modules import files_work_data_frame as fw_df
from modules import learning_model as lm
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import KMeans



# Считать все группы в dataframe
df = fw_df.read_files_to_df("L3. ProgrammerGroups")
# Записать названия групп
names_of_groups = df["group"].unique()
names = df["name"]
av.transform_categories(df)
# Записать индексы групп
indexes_of_groups = df["group"].unique()
# Получить словарь названий групп
names_of_groups = av.get_dict_groups(names_of_groups, indexes_of_groups)
df = df.fillna(0)
av.all_numerical_to_int(df, ["days_from_publication", "id"])
# Удалить ненужные признаки
df = lm.clear_df_columns(df)
num_of_clusters = 5
# KMeans
clustersKMeans = cm.get_clusters(
    KMeans(n_clusters=5), df, names_of_groups, names)
cm.write_all_clusters(clustersKMeans, "L6. Clusters/KMeansClusters.txt", "All clusters")
df = df.drop('name', 1)
# AffinityPropagation
clustersAffinityPropagation = cm.get_clusters(
    AffinityPropagation(), df, names_of_groups, names)
cm.write_all_clusters(clustersAffinityPropagation, "L6. Clusters/AffinityPropagationClusters.txt", "All clusters")
df = df.drop('name', 1)
# Top 3
num_of_values = 3
# KMeans
top_3_clustersKMeans = cm.get_top_clusters(clustersKMeans, num_of_values)
cm.write_all_clusters(top_3_clustersKMeans,
                      "L6. Clusters/KMeansClusters.txt", "Top " + str(num_of_values) + " clusters", "a")
# AffinityPropagation
top_3_clustersAffinityPropagation = cm.get_top_clusters(clustersAffinityPropagation, num_of_values)
cm.write_all_clusters(top_3_clustersAffinityPropagation,
                      "L6. Clusters/AffinityPropagationClusters.txt", "Top " + str(num_of_values) + " clusters", "a")
