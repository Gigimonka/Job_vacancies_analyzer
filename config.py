# config.py

# Базовый URL для доступа к API HeadHunter
BASE_URL = "https://api.hh.ru/vacancies"

# Параметры для поиска вакансий
SEARCH_PARAMS = {
    "text": "Data Analyst OR Data Scientist OR Data Engineer",  # Ключевые слова для поиска
    "area": "1",  # Код региона (1 - Москва, 2 - Санкт-Петербург, и т.д.)
    "per_page": 100,  # Количество вакансий на одной странице
}

# Уровни квалификации для фильтрации
LEVELS = {
    "Junior": ["noExperience", "between1And3"],
    "Middle": ["between3And6"],
    "Senior": ["moreThan6"],
}

# Кодировка запроса для получения корректных данных
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
