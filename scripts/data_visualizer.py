# scripts/data_visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict

# Устанавливаем стиль для графиков
sns.set(style="whitegrid")

def plot_vacancies_per_level(data: pd.DataFrame):
    """
    Строит гистограмму количества вакансий по уровням квалификации.

    :param data: DataFrame с данными о вакансиях
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(x="level", data=data, palette="viridis")
    plt.title("Количество вакансий по уровням квалификации")
    plt.xlabel("Уровень квалификации")
    plt.ylabel("Количество вакансий")
    plt.show()


def plot_vacancies_per_region(data: pd.DataFrame):
    """
    Строит гистограмму количества вакансий по регионам.

    :param data: DataFrame с данными о вакансиях
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(x="region", data=data, palette="plasma")
    plt.title("Количество вакансий по регионам")
    plt.xlabel("Регион")
    plt.ylabel("Количество вакансий")
    plt.show()


def plot_salary_distribution(data: pd.DataFrame):
    """
    Строит распределение зарплат по направлениям.

    :param data: DataFrame с данными о вакансиях
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data, x="salary_from", hue="level", element="step", stat="density", common_norm=False, palette="coolwarm")
    plt.title("Распределение зарплат по уровням квалификации")
    plt.xlabel("Зарплата (от)")
    plt.ylabel("Плотность")
    plt.xlim(0, data["salary_from"].max())
    plt.show()


def plot_vacancies_trend(data: pd.DataFrame):
    """
    Строит график изменения количества вакансий по месяцам.

    :param data: DataFrame с данными о вакансиях
    """
    # Добавляем столбец с месяцами для группировки
    data["month"] = data["published_at"].dt.to_period("M")
    
    # Группируем данные по месяцам и считаем количество вакансий
    vacancies_per_month = data.groupby("month").size().reset_index(name="vacancy_count")
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x="month", y="vacancy_count", data=vacancies_per_month, marker="o", color="b")
    plt.title("Тренд количества вакансий по месяцам")
    plt.xlabel("Месяц")
    plt.ylabel("Количество вакансий")
    plt.xticks(rotation=45)
    plt.show()


def display_summary_statistics(stats: Dict[str, any]):
    """
    Выводит сводные статистики по вакансиям в текстовом формате.

    :param stats: Словарь с ключевыми статистиками
    """
    print("Сводные статистики по вакансиям:")
    print(f"Общее количество вакансий: {stats['total_vacancies']}")
    print(f"Количество вакансий по уровням: {stats['vacancies_per_level']}")
    print(f"Количество вакансий по регионам: {stats['vacancies_per_region']}")
    print(f"Средняя зарплата (от): {stats['average_salary_from']:.2f}")
    print(f"Средняя зарплата (до): {stats['average_salary_to']:.2f}")


if __name__ == "__main__":
    # Загружаем обработанные данные
    processed_data = pd.read_csv("data/processed_vacancies_data.csv", parse_dates=["published_at"])
    
    # Отображение гистограммы количества вакансий по уровням
    plot_vacancies_per_level(processed_data)
    
    # Отображение гистограммы количества вакансий по регионам
    plot_vacancies_per_region(processed_data)
    
    # Отображение распределения зарплат по уровням
    plot_salary_distribution(processed_data)
    
    # Отображение тренда изменения количества вакансий по месяцам
    plot_vacancies_trend(processed_data)
    
    # Отображение сводных статистик
    stats = {
        "total_vacancies": len(processed_data),
        "vacancies_per_level": processed_data["level"].value_counts().to_dict(),
        "vacancies_per_region": processed_data["region"].value_counts().to_dict(),
        "average_salary_from": processed_data["salary_from"].mean(),
        "average_salary_to": processed_data["salary_to"].mean(),
    }
    display_summary_statistics(stats)
