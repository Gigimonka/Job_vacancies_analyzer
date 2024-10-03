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
    ax = sns.countplot(x="level", data=data, palette="viridis")
    plt.title("Количество вакансий по уровням квалификации")
    plt.xlabel("Уровень квалификации")
    plt.ylabel("Количество вакансий")
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5), 
                    textcoords='offset points')
    plt.show()


def plot_vacancies_per_region(data: pd.DataFrame):
    """
    Строит гистограмму количества вакансий по регионам.

    :param data: DataFrame с данными о вакансиях
    """
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x="region", data=data, palette="plasma")
    plt.title("Количество вакансий по регионам")
    plt.xlabel("Регион")
    plt.ylabel("Количество вакансий")
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5), 
                    textcoords='offset points')
    plt.show()


def plot_vacancies_per_level_region(data: pd.DataFrame):
    """
    Строит график количества вакансий по уровням квалификации в разрезе регионов.

    :param data: DataFrame с данными о вакансиях
    """
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x="region", hue="level", data=data, palette="viridis")
    plt.title("Количество вакансий по уровням квалификации в разрезе регионов")
    plt.xlabel("Регион")
    plt.ylabel("Количество вакансий")
    plt.legend(title="Уровень квалификации")
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5), 
                    textcoords='offset points')
    plt.show()

def plot_average_salary_by_region_and_level(data: pd.DataFrame):
    """
    Строит график средней зарплаты по регионам и уровням квалификации.
    Исключает вакансии, где зарплата не указана (salary_from и salary_to равны 0).

    :param data: DataFrame с данными о вакансиях
    """
    # Отфильтруем записи, где указана хотя бы одна зарплата (salary_from или salary_to больше 0)
    filtered_data = data[(data['salary_from'] > 0) | (data['salary_to'] > 0)]
    
    # Рассчитаем среднюю зарплату только для тех вакансий, где она указана
    filtered_data['average_salary'] = filtered_data[['salary_from', 'salary_to']].mean(axis=1)

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="region", y="average_salary", hue="level", data=filtered_data, palette="magma")
    plt.title("Средняя зарплата по регионам и уровням квалификации")
    plt.xlabel("Регион")
    plt.ylabel("Средняя зарплата")
    plt.legend(title="Уровень квалификации")
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5), 
                    textcoords='offset points')
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
    
    # Рассчитываем среднюю зарплату для каждого уровня и региона
    processed_data['average_salary'] = processed_data[['salary_from', 'salary_to']].mean(axis=1)
    
    # Отображение гистограммы количества вакансий по уровням
    plot_vacancies_per_level(processed_data)
    
    # Отображение графика количества вакансий по уровням в разрезе регионов
    plot_vacancies_per_level_region(processed_data)
    
    # Отображение гистограммы количества вакансий по регионам
    plot_vacancies_per_region(processed_data)
    
    # Отображение средней зарплаты по регионам и уровням
    plot_average_salary_by_region_and_level(processed_data)
    
    # Отображение сводных статистик
    stats = {
        "total_vacancies": len(processed_data),
        "vacancies_per_level": processed_data["level"].value_counts().to_dict(),
        "vacancies_per_region": processed_data["region"].value_counts().to_dict(),
        "average_salary_from": processed_data[processed_data["salary_from"] > 0]["salary_from"].mean(),
        "average_salary_to": processed_data[processed_data["salary_to"] > 0]["salary_to"].mean(),
    }
    display_summary_statistics(stats)
