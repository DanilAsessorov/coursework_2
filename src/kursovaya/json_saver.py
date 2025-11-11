from abc import ABC, abstractmethod
import json
import os
from typing import List

from .vacancy import Vacancy


class BaseSaver(ABC):
    """
    Абстрактный класс для работы с хранилищем вакансий.
    Определяет обязательные методы, которые должны быть реализованы.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict = None) -> List[Vacancy]:
        """Получить вакансии по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из хранилища."""
        pass


class JSONSaver(BaseSaver):
    """
    Реализация хранилища для сохранения вакансий в JSON-файл.
    """

    def __init__(self, filepath: str = "data/vacancies.json"):
        self.filepath = filepath
        self.vacancies = self.load_vacancies()

    def load_vacancies(self) -> List[dict]:
        """Загрузить вакансии из JSON-файла."""
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump([], file)
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_vacancies(self) -> None:
        """Сохранить текущие вакансии в файл."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в список и сохранить в файл."""
        vacancy_dict = vacancy.to_dict()
        if vacancy_dict not in self.vacancies:
            self.vacancies.append(vacancy_dict)
            self.save_vacancies()

    def get_vacancies(self, criteria: dict = None) -> List[Vacancy]:
        """
        Получить вакансии по критериям.
        Пока поддерживается только фильтрация по ключевым словам в описании или названии.
        """
        filtered = self.vacancies

        if criteria:
            keyword = criteria.get("keyword")
            if keyword:
                keyword_lower = keyword.lower()
                filtered = [
                    v for v in filtered
                    if keyword_lower in v["title"].lower() or keyword_lower in v["description"].lower()
                ]

        # Преобразуем обратно в объекты Vacancy
        return [
            Vacancy(
                title=v["title"],
                link=v["link"],
                salary=v["salary"],
                description=v["description"]
            )
            for v in filtered
        ]

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию по ссылке."""
        vacancy_dict = vacancy.to_dict()
        self.vacancies = [v for v in self.vacancies if v != vacancy_dict]
        self.save_vacancies()
