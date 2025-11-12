from src.kursovaya.api import HeadHunterAPI
from src.kursovaya.json_saver import JSONSaver
from src.kursovaya.utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    print_vacancies,
    sort_vacancies,
)
from src.kursovaya.vacancy import Vacancy


def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат (например, 100000 - 150000): ")

    print("\nПолучаем вакансии с HH.ru...")
    hh_vacancies_json = hh_api.get_vacancies(search_query, per_page=top_n * 2)

    if not hh_vacancies_json:
        print("Не удалось получить вакансии. Проверьте подключение или запрос.")
        return

    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_json)

    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print(f"\nТоп {top_n} вакансий по зарплате:")
    print_vacancies(top_vacancies)


def main() -> None:
    """Точка входа в программу."""
    user_interaction()


if __name__ == "__main__":
    main()
