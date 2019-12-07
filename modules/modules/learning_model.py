from datetime import datetime

from sklearn import model_selection, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


def find_the_best_classifier(train, target, test_size):
    kfold = 5
    itog_val = {}
    test = model_selection.train_test_split(train, target, test_size=test_size)
    model_rfc = RandomForestClassifier(n_estimators=100)
    model_rfc.fit(train, target)
    model_knc = KNeighborsClassifier(n_neighbors=100)
    model_knc.fit(train, target)
    model_dtc = DecisionTreeClassifier(max_depth=20, random_state=0)
    model_dtc.fit(train, target)
    model_lr = LogisticRegression(penalty='l1', tol=0.01, multi_class='ovr', solver='liblinear')
    model_lr.fit(train, target)
    model_svc = svm.SVC(gamma='scale')
    model_svc.fit(train, target)
    scores = model_selection.cross_val_score(model_rfc, train, target, cv=kfold)
    itog_val['RandomForestClassifier'] = scores.mean()
    scores = model_selection.cross_val_score(model_knc, train, target, cv=kfold)
    itog_val['KNeighborsClassifier'] = scores.mean()
    scores = model_selection.cross_val_score(model_dtc, train, target, cv=kfold)
    itog_val['DecisionTreeClassifier'] = scores.mean()
    scores = model_selection.cross_val_score(model_lr, train, target, cv=kfold)
    itog_val['LogisticRegression'] = scores.mean()
    scores = model_selection.cross_val_score(model_svc, train, target, cv=kfold)
    itog_val['SVC'] = scores.mean()
    print(itog_val)


def predict(new_df, train_l, target_l, train_t, target_t):
    model_rfc = RandomForestClassifier(n_estimators=100)
    model_rfc = model_rfc.fit(train_l, target_l)
    print(model_rfc.score(train_l, target_l))
    print(model_rfc.score(train_t, target_t))
    return model_rfc.predict(new_df)


def clear_df_columns(data_frame):
    data_frame = data_frame.drop('experience_Более 6 лет', 1)
    data_frame = data_frame.drop('experience_Нет опыта', 1)
    data_frame = data_frame.drop('experience_От 1 года до 3 лет', 1)
    data_frame = data_frame.drop('experience_От 3 до 6 лет', 1)
    data_frame = data_frame.drop('schedule_Гибкий график', 1)
    data_frame = data_frame.drop('schedule_Полный день', 1)
    data_frame = data_frame.drop('schedule_Сменный график', 1)
    data_frame = data_frame.drop('schedule_Удаленная работа', 1)
    data_frame = data_frame.drop('employment_Полная занятость', 1)
    data_frame = data_frame.drop('employment_Проектная работа', 1)
    data_frame = data_frame.drop('employment_Стажировка', 1)
    data_frame = data_frame.drop('employment_Частичная занятость', 1)
    data_frame = data_frame.drop('city_Екатеринбург', 1)
    data_frame = data_frame.drop('city_Москва', 1)
    data_frame = data_frame.drop('city_Новосибирск', 1)
    data_frame = data_frame.drop('city_Омск', 1)
    data_frame = data_frame.drop('city_Ростов-на-Дону', 1)
    data_frame = data_frame.drop('days_from_publication', 1)
    data_frame = data_frame.drop('name', 1)
    data_frame = data_frame.drop('company', 1)
    data_frame = data_frame.drop('description', 1)
    data_frame = data_frame.drop('conditions', 1)
    data_frame = data_frame.drop('requirement', 1)
    data_frame = data_frame.drop('responsibility', 1)
    data_frame = data_frame.drop('key_skills', 1)
    data_frame = data_frame.drop('Другие навыки', 1)
    return data_frame
