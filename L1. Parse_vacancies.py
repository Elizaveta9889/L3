import pandas as pd
from modules import parse_vacancies as pv
from modules import write_data_frame as w_df
from modules import divide_vacancies as dv

# Получение вакансий по 10 городам
areas = [2, 3, 4, 68, 76, 78, 88, 95, 104]
df = pd.DataFrame(pv.parse_vacancies(pv.get_vacancies("Программист", 1, 10)))
for area in areas:
    df = df.append((pv.parse_vacancies(pv.get_vacancies("Программист", area, 100))))
# Сортировка вакасий
df = df.sort_values(['max_salary', 'min_salary'], ascending=[False, True])
# Запись всех вакансий в файл
w_df.save_data_frame(df, "Vacancies")
# Получение и запись групп по зарплате
groups = dv.get_groups_salary(df, 'max_salary', 10)
w_df.write_groups(groups, "L1. GroupsSalary/salary_gr")
w_df.write_groups_info(groups, "name", "L1. GroupsSalary/info_salary_gr")
# Получение и запись групп по названию
groups = dv.get_groups_name(df, 'name')
w_df.write_groups(groups, "L1. GroupsName/name_gr")
w_df.write_groups_info(groups, "min_salary", "L1. GroupsName/info_min_salary_name_gr")
w_df.write_groups_info(groups, "max_salary", "L1. GroupsName/info_max_salary_name_gr")