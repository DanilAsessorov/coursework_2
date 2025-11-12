import os

from src.kursovaya.json_saver import JSONSaver
from src.kursovaya.vacancy import Vacancy


def test_json_saver_add_and_get() -> None:
    """Тест добавления и получения вакансий."""
    saver = JSONSaver("data/test_vacancies.json")

    # Удаляем тестовый файл, если есть
    if os.path.exists(saver._filepath):
        os.remove(saver._filepath)

    vacancy = Vacancy("Test", "https://hh.ru", "100000", "Test desc")
    saver.add_vacancy(vacancy)

    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].title == "Test"

    # Удаление
    saver.delete_vacancy(vacancy)
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 0

    # Очистка
    if os.path.exists(saver._filepath):
        os.remove(saver._filepath)
