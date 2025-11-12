import re
from typing import Any


class Vacancy:
    __slots__ = ("title", "link", "salary", "description")

    """
    Класс для представления вакансии.
    Поддерживает сравнение по зарплате и валидацию данных.
    """

    def __init__(
        self, title: str, link: str, salary: str | None, description: str | None
    ):
        self.title = self._validate_title(title)
        self.link = self._validate_link(link)
        self.salary = self._validate_salary(salary)
        self.description = description or "Описание не указано"

    @staticmethod
    def _validate_title(title: str) -> str:
        """Проверяет, что название не пустое."""
        if not title or not title.strip():
            raise ValueError("Название вакансии не может быть пустым.")
        return title.strip()

    @staticmethod
    def _validate_link(link: str) -> str:
        """Проверяет, что ссылка корректна."""
        if not link.startswith("http://") and not link.startswith("https://"):
            raise ValueError("Ссылка должна начинаться с http:// или https://")
        return link

    @staticmethod
    def _validate_salary(salary: str | None) -> str:
        """Преобразует зарплату в читаемый формат, если не указана — ставит заглушку."""
        if not salary or salary.strip().lower() in ("не указано", "з/п не указана", ""):
            return "Зарплата не указана"
        return salary.strip()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary_in_rub() < other.get_salary_in_rub()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary_in_rub() > other.get_salary_in_rub()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary_in_rub() == other.get_salary_in_rub()

    def get_salary_in_rub(self) -> int:
        """
        Извлекает числовое значение зарплаты (в рублях) для сравнения.
        Если не указана — возвращает 0.
        """
        if self.salary == "Зарплата не указана":
            return 0
        numbers = re.findall(r"\d+", self.salary.replace(" ", ""))
        return int(numbers[0]) if numbers else 0

    def __str__(self) -> str:
        return f"Вакансия: {self.title}\nСсылка: {self.link}\nЗарплата: {self.salary}\nОписание: {self.description}\n"

    def to_dict(self) -> dict[str, str]:
        """Словарь для сохранения в JSON."""
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
        }

    @staticmethod
    def cast_to_object_list(data: list[dict[str, Any]]) -> list["Vacancy"]:
        """Преобразует список словарей из API в список объектов Vacancy."""
        vacancies: list["Vacancy"] = []
        for item in data:
            salary = None
            if item.get("salary"):
                salary_from = item["salary"].get("from")
                salary_to = item["salary"].get("to")
                currency = item["salary"].get("currency", "")
                if salary_from:
                    salary = (
                        f"{salary_from} - {salary_to} {currency}"
                        if salary_to
                        else f"{salary_from} {currency}"
                    )
            vacancies.append(
                Vacancy(
                    title=item["name"],
                    link=item.get("alternate_url", "https://hh.ru"),
                    salary=salary,
                    description=item.get("snippet", {}).get(
                        "requirement", "Нет описания"
                    ),
                )
            )
        return vacancies
