import pytest

from src.kursovaya.vacancy import Vacancy


def test_vacancy_creation() -> None:
    """Тест создания вакансии."""
    vacancy = Vacancy(
        title="Python Developer",
        link="https://hh.ru/vacancy/123",
        salary="100 000 - 150 000 руб.",
        description="Требуется Python-разработчик",
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.link == "https://hh.ru/vacancy/123"
    assert vacancy.salary == "100 000 - 150 000 руб."
    assert vacancy.description == "Требуется Python-разработчик"


def test_vacancy_validation_empty_title() -> None:
    """Тест валидации: пустое название."""
    with pytest.raises(ValueError):
        Vacancy("", "https://hh.ru", "100000", "Описание")


def test_vacancy_validation_invalid_link() -> None:
    """Тест валидации: некорректная ссылка."""
    with pytest.raises(ValueError):
        Vacancy("Dev", "invalid-link", "100000", "Описание")


def test_vacancy_salary_not_specified() -> None:
    """Тест: зарплата не указана."""
    vacancy = Vacancy("Dev", "https://hh.ru", None, "Описание")
    assert vacancy.salary == "Зарплата не указана"


def test_vacancy_comparison() -> None:
    """Тест сравнения вакансий по зарплате."""
    v1 = Vacancy("A", "https://hh.ru/1", "150000 руб.", "desc")
    v2 = Vacancy("B", "https://hh.ru/2", "100000 руб.", "desc")
    v3 = Vacancy("C", "https://hh.ru/3", "Зарплата не указана", "desc")

    assert v1 > v2
    assert v2 > v3
    assert v1 > v3
