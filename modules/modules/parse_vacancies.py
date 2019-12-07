import requests

from modules import clear_text as ct


# Получить вакансии с hh по определённому городу
def get_vacancies(name_of_vacancy, area, per_page, page):
    url = 'https://api.hh.ru/vacancies'
    data = {'text': name_of_vacancy, 'area': area, 'per_page': per_page, 'page': page}
    return requests.get(url, params=data).json()


# Получить информацию по id вакансии
def get_vacancy_info(vacancy_id):
    return requests.get('https://api.hh.ru/vacancies/%s' % vacancy_id).json()


# Распарсить JSON-объект как вакансию
def parse_vacancies(json):
    return [parse_vacancy(elem) for elem in json['items']]


# Добавить параметр в вакансию
def add_param(vacancy, elem, vacancy_param, elem_params):
    current = elem
    for param in elem_params:
        current = current[param] if current is not None else None
        if current is None:
            break
    vacancy[vacancy_param] = ct.remove_tags(current) if type(current) is str else current


# Получить требования из описания
def get_conditions(description):
    description_mas_cond1 = description.split('Условия:')
    description_mas_cond2 = description.split('Вам потребуется:')
    description_mas_cond3 = description.split('Мы предлагаем:')

    if len(description_mas_cond1) > 1:
        return description_mas_cond1[1]
    if len(description_mas_cond2) > 1:
        return description_mas_cond2[1]
    if len(description_mas_cond3) > 1:
        return description_mas_cond3[1]


# Перевести массив навыков в строку
def get_skills(mas_skills):
    skills = ''
    for skill in mas_skills:
        skills += skill['name'] + '; '
    skills = skills[:-2]
    return skills


# Распарсить вакансию
def parse_vacancy(elem):
    info = get_vacancy_info(elem['id'])
    vacancy = dict()
    add_param(vacancy, elem, "id", ["id"])
    add_param(vacancy, elem, "name", ["name"])
    add_param(vacancy, elem, "city", ["area", "name"])
    add_param(vacancy, elem, "min_salary", ["salary", "from"])
    add_param(vacancy, elem, "max_salary", ["salary", "to"])
    add_param(vacancy, elem, "company", ["employer", "name"])
    add_param(vacancy, elem, "published_at", ["published_at"])
    add_param(vacancy, info, "experience", ["experience", "name"])
    add_param(vacancy, info, "schedule", ["schedule", "name"])
    add_param(vacancy, info, "employment", ["employment", "name"])
    add_param(vacancy, info, "description", ["description"])
    vacancy["conditions"] = get_conditions(vacancy["description"])
    add_param(vacancy, elem, "requirement", ["snippet", "requirement"])
    add_param(vacancy, elem, "responsibility", ["snippet", "responsibility"])
    vacancy["key_skills"] = get_skills(info['key_skills'])
    return vacancy
