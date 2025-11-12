from typing import List

from .vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам в названии или описании.

    :param vacancies: список вакансий
    :param filter_words: список ключевых слов
    :return: отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    filter_words_lower = [word.lower() for word in filter_words]

    for vacancy in vacancies:
        text = f"{vacancy.title} {vacancy.description}".lower()
        if any(word in text for word in filter_words_lower):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат.

    :param vacancies: список вакансий
    :param salary_range: строка вида "100000 - 150000"
    :return: отфильтрованный список вакансий
    """
    try:
        if not salary_range or "Зарплата не указана" in salary_range:
            return vacancies

        parts = salary_range.replace(" ", "").split("-")
        if len(parts) == 1:
            min_salary = int(parts[0])
            max_salary = float("inf")
        else:
            min_salary = int(parts[0])
            max_salary = int(parts[1])

        result = []
        for vacancy in vacancies:
            salary_in_rub = vacancy.get_salary_in_rub()
            if min_salary <= salary_in_rub <= max_salary:
                result.append(vacancy)

        return result

    except (ValueError, IndexError):
        print(
            "Некорректный формат диапазона зарплат. Используйте формат: 100000 - 150000"
        )
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по убыванию зарплаты.

    :param vacancies: список вакансий
    :return: отсортированный список
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий.

    :param vacancies: отсортированный список вакансий
    :param top_n: количество вакансий
    :return: топ N вакансий
    """
    if top_n <= 0:
        return []
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Выводит вакансии в удобном формате.

    :param vacancies: список вакансий
    """
    if not vacancies:
        print("Вакансий не найдено.")
        return

    for i, vacancy in enumerate(vacancies, start=1):
        print(f"\n{i}. {vacancy}")
