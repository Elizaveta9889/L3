import pandas as pd
from sklearn.metrics import pairwise_distances_argmin_min


# Получить несколько самых больших значений из словаря
def get_top_values_dict(dictionary, num=0):
    if num == 0:
        num = len(dictionary)
    sorted_dict = (sorted(dictionary, key=dictionary.get, reverse=True))[0:min(len(dictionary), num)]
    srt_dict = ''
    for el in sorted_dict:
        if dictionary[el] != 0:
            srt_dict += str(el) + ' (' + str(dictionary[el]) + '), '
    return srt_dict[:-2]


# Получить кластеры по модели
def get_clusters(model, df, names_of_groups, names):
    model_fit = model.fit_predict(df)
    closest, _ = pairwise_distances_argmin_min(model.cluster_centers_, df)
    clusters = []
    for i in range(0, max(model_fit) + 1):
        clusters.append(Cluster(i+1))
    # Добавление значений в кластеры
    df["name"] = names
    for i in range(0, len(model_fit)):
        clusters[model_fit[i]].values.append(df.iloc[i])
    i = 0
    for cluster in clusters:
        cluster.values = pd.DataFrame(cluster.values)
        cluster.center = df.iloc[closest[i]]
        i += 1
        for key, val in names_of_groups.items():
            cluster.values["group"] = cluster.values["group"].replace(key, val)
    return clusters


# Записать все крастеры в файл
def write_all_clusters(clusters, file_name, title="", modifier="w"):
    file = open(file_name, modifier)
    file.write(title + ':\n')
    file.close()
    for cluster in clusters:
        cluster.write(file_name, "a")


# Получить самые большие кластеры
def get_top_clusters(clusters, num):
    return (sorted(clusters, key=lambda cluster: cluster.count(), reverse=True))[0:min(len(clusters), num)]


class Cluster(object):

    def __init__(self, name):
        """Constructor"""
        self.name = name
        self.center = None
        self.values = []

    # Центер кластера
    def get_center(self):
        return ' '.join(self.center.to_string().replace("\n", "; ").split())

    # Количество элементов в кластере
    def count(self):
        return len(self.values)

    # Среднее значение столбца
    def get_mean(self, column, round_value=2):
        return round(self.values[column].mean(), round_value)

    # Получить самые популярные навыки
    def get_skills(self, num=0):
        values = dict()
        for i in range(22, len(self.values.columns)):
            name = self.values.iloc[:, i].name
            values[name] = self.values[self.values[name] == 1][name].sum()
        return get_top_values_dict(values, num)

    # Получить самые популярные требования опыта работы
    def get_experiences_count(self, num=0):
        values = dict()
        for i in range(5, 9):
            name = self.values.iloc[:, i].name
            values[name.split('_')[1]] = self.values[self.values[name] == 1][name].sum()
        return get_top_values_dict(values, num)

    # Получить самые популярные варианты графика работы
    def get_schedules_count(self, num=0):
        values = dict()
        for i in range(9, 13):
            name = self.values.iloc[:, i].name
            values[name.split('_')[1]] = self.values[self.values[name] == 1][name].sum()
        return get_top_values_dict(values, num)

    # Получить самые популярные варианты типа занятости
    def get_employments_count(self, num=0):
        values = dict()
        for i in range(13, 17):
            name = self.values.iloc[:, i].name
            values[name.split('_')[1]] = self.values[self.values[name] == 1][name].sum()
        return get_top_values_dict(values, num)

    # Получить самые популярные города
    def get_cities_count(self, num=0):
        values = dict()
        for i in range(17, 22):
            name = self.values.iloc[:, i].name
            values[name.split('_')[1]] = self.values[self.values[name] == 1][name].sum()
        return get_top_values_dict(values, num)

    # Получить самые популярные группы
    def get_groups_count(self, num=0):
        values = dict()
        categories = pd.unique(self.values["group"])
        for i in categories:
            values[i] = self.values[self.values["group"] == i]["group"].count()
        return get_top_values_dict(values, num)

    def __str__(self):
        return "\tCluster " + str(self.name) + "\n" + \
               "\tCenter: " + str(self.get_center()) + "\n" + \
               "\tCount of values: " + str(self.count()) + "\n" + \
               "\tTop 5 key skills: " + str(self.get_skills(5)) + "\n" + \
               "\tMean: " + \
               "min salary - " + str(self.get_mean("min_salary")) + ", " + \
               "max salary - " + str(self.get_mean("max_salary")) + "\n" + \
               "\tTop 3 experiences: " + str(self.get_experiences_count(3)) + "\n" + \
               "\tTop 3 schedules: " + str(self.get_schedules_count(3)) + "\n" + \
               "\tTop 3 employments: " + str(self.get_employments_count(3)) + "\n" + \
               "\tTop 3 cities: " + str(self.get_cities_count(3)) + "\n" + \
               "\tGroups: " + str(self.get_groups_count()) + "\n"

    # Записать в файл
    def write(self, file_name, modifier):
        file = open(file_name, modifier)
        file.write(str(self) + '\n')
        file.close()

