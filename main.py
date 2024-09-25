# main.py

from scripts.data_collector import collect_data, save_data_to_csv
from scripts.data_processor import load_data, preprocess_data, filter_by_date, get_summary_statistics
from scripts.data_visualizer import (
    plot_vacancies_per_level,
    plot_vacancies_per_region,
    plot_salary_distribution,
    plot_vacancies_trend,
    display_summary_statistics,
)
import pandas as pd

def main():
    # Шаг 1: Сбор данных
    regions = ["1", "2"]  # Москва и Санкт-Петербург
    print("Сбор данных о вакансиях...")
    vacancies_data = collect_data(regions)
    save_data_to_csv(vacancies_data, "data/vacancies_data.csv")
    print("Данные собраны и сохранены в файл data/vacancies_data.csv.")

    # Шаг 2: Загрузка и предварительная обработка данных
    print("Загрузка и предварительная обработка данных...")
    data = load_data("data/vacancies_data.csv")
    processed_data = preprocess_data(data)
    
    # Шаг 3: Фильтрация данных по дате публикации (например, за 2023 год)
    print("Фильтрация данных по дате публикации...")
    filtered_data = filter_by_date(processed_data, "2023-01-01", "2024-09-25")
    print(f"Отфильтровано {len(filtered_data)} вакансий.")
    
    # Шаг 4: Вычисление сводных статистик
    print("Вычисление сводных статистик...")
    stats = get_summary_statistics(filtered_data)
    display_summary_statistics(stats)
    
    # Шаг 5: Визуализация данных
    print("Визуализация данных...")
    plot_vacancies_per_level(filtered_data)
    plot_vacancies_per_region(filtered_data)
    plot_salary_distribution(filtered_data)
    plot_vacancies_trend(filtered_data)
    
    # Шаг 6: Сохранение обработанных данных
    processed_data.to_csv("data/processed_vacancies_data.csv", index=False)
    print("Обработанные данные сохранены в файл data/processed_vacancies_data.csv.")

if __name__ == "__main__":
    main()
