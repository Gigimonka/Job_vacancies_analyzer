# scripts/data_collector.py

import requests
import pandas as pd
from typing import List, Dict
import time
from config import BASE_URL, SEARCH_PARAMS, LEVELS, HEADERS

def get_vacancies_by_level(level: str, region: str) -> List[Dict]:
    """
    Функция для получения списка вакансий по заданному уровню и региону.

    :param level: Уровень квалификации (Junior, Middle, Senior)
    :param region: Код региона (например, '1' для Москвы)
    :return: Список словарей с данными о вакансиях
    """
    vacancies = []
    params = SEARCH_PARAMS.copy()
    params["area"] = region  # Устанавливаем нужный регион
    params["experience"] = LEVELS[level]  # Фильтр по опыту работы
    
    page = 0
    while True:
        params["page"] = page
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Ошибка {response.status_code} при запросе вакансий.")
            break
        
        data = response.json()
        vacancies.extend(data.get("items", []))
        
        if data.get("pages") - 1 == page:
            break
        page += 1
        time.sleep(0.5)  # Пауза между запросами, чтобы не блокировали IP
        
    return vacancies

def collect_data(regions: List[str]) -> pd.DataFrame:
    """
    Функция для сбора данных по всем уровням и регионам.

    :param regions: Список кодов регионов для анализа
    :return: DataFrame с собранными данными по вакансиям
    """
    all_vacancies = []
    for region in regions:
        for level in LEVELS.keys():
            print(f"Сбор данных для уровня {level} в регионе {region}...")
            vacancies = get_vacancies_by_level(level, region)
            for vacancy in vacancies:
                vacancy_data = {
                    "id": vacancy["id"],
                    "name": vacancy["name"],
                    "level": level,
                    "region": region,
                    "employer": vacancy["employer"]["name"] if vacancy.get("employer") else "Неизвестно",
                    "salary_from": vacancy["salary"]["from"] if vacancy.get("salary") else None,
                    "salary_to": vacancy["salary"]["to"] if vacancy.get("salary") else None,
                    "currency": vacancy["salary"]["currency"] if vacancy.get("salary") else None,
                    "published_at": vacancy["published_at"],
                }
                all_vacancies.append(vacancy_data)
    return pd.DataFrame(all_vacancies)

def save_data_to_csv(data: pd.DataFrame, filename: str):
    """
    Сохраняет DataFrame с вакансиями в CSV файл.

    :param data: DataFrame с данными о вакансиях
    :param filename: Имя файла для сохранения
    """
    data.to_csv(filename, index=False)
    print(f"Данные успешно сохранены в {filename}")

if __name__ == "__main__":
    regions = ["1", "2"]  # Москва и Санкт-Петербург
    vacancies_data = collect_data(regions)
    save_data_to_csv(vacancies_data, "../data/vacancies_data.csv")
