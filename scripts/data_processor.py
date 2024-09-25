# scripts/data_processor.py

import pandas as pd
from typing import Dict, Any


def load_data(filename: str) -> pd.DataFrame:
    """
    Загружает данные из CSV файла в DataFrame.

    :param filename: Имя файла для загрузки данных
    :return: DataFrame с данными из файла
    """
    try:
        data = pd.read_csv(filename)
        print(f"Данные успешно загружены из {filename}")
        return data
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return pd.DataFrame()


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Выполняет предварительную обработку данных: удаление лишних столбцов и заполнение пропусков.

    :param data: Исходный DataFrame с данными
    :return: Обработанный DataFrame
    """
    # Удаляем строки с пустыми значениями для важных колонок
    data = data.dropna(subset=["name", "level", "region", "published_at"])
    
    # Заполняем пропуски в зарплатах значением 0
    data["salary_from"] = data["salary_from"].fillna(0)
    data["salary_to"] = data["salary_to"].fillna(0)
    
    # Преобразуем столбец с датой в формат datetime
    data["published_at"] = pd.to_datetime(data["published_at"])
    
    # Удаляем лишние столбцы, если они есть
    columns_to_drop = [col for col in data.columns if col not in ["id", "name", "level", "region", "employer", "salary_from", "salary_to", "currency", "published_at"]]
    data = data.drop(columns=columns_to_drop, axis=1)
    
    return data


def get_summary_statistics(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Вычисляет сводные статистики по вакансиям.

    :param data: DataFrame с данными о вакансиях
    :return: Словарь с ключевыми статистиками
    """
    stats = {
        "total_vacancies": len(data),
        "vacancies_per_level": data["level"].value_counts().to_dict(),
        "vacancies_per_region": data["region"].value_counts().to_dict(),
        "average_salary_from": data["salary_from"].mean(),
        "average_salary_to": data["salary_to"].mean(),
    }
    return stats


def filter_by_date(data: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Фильтрует вакансии по дате публикации.

    :param data: Исходный DataFrame
    :param start_date: Начальная дата (YYYY-MM-DD)
    :param end_date: Конечная дата (YYYY-MM-DD)
    :return: Отфильтрованный DataFrame
    """
    filtered_data = data[(data["published_at"] >= start_date) & (data["published_at"] <= end_date)]
    return filtered_data


if __name__ == "__main__":
    # Загружаем данные из CSV файла
    df = load_data("../data/vacancies_data.csv")
    
    # Предварительная обработка данных
    processed_data = preprocess_data(df)
    
    # Фильтрация данных по дате
    filtered_data = filter_by_date(processed_data, "2023-01-01", "2024-09-25")
    
    # Вычисление сводных статистик
    stats = get_summary_statistics(filtered_data)
    print("Сводные статистики по вакансиям:")
    print(stats)
    
    # Сохраняем обработанные данные в новый файл
    filtered_data.to_csv("../data/processed_vacancies_data.csv", index=False)
    print("Обработанные данные сохранены в файл processed_vacancies_data.csv")
