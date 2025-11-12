import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

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
    def get_vacancies(self, criteria: Optional[Dict[str, str]] = None) -> List[Vacancy]:
        """Получить вакансии по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из хранилища."""
        pass


class JSONSaver(BaseSaver):
    def __init__(self, filepath: str = "data/vacancies.json"):
        self._filepath = filepath
        self._vacancies = self._load_vacancies()

    def _load_vacancies(self) -> List[Dict[str, str]]:
        if not os.path.exists(self._filepath):
            os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
            with open(self._filepath, "w", encoding="utf-8") as file:
                json.dump([], file)
            return []

        try:
            with open(self._filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_vacancies(self) -> None:
        """Приватный метод сохранения в файл."""
        with open(self._filepath, "w", encoding="utf-8") as file:
            json.dump(self._vacancies, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancy_dict = vacancy.to_dict()
        if vacancy_dict not in self._vacancies:
            self._vacancies.append(vacancy_dict)
            self._save_vacancies()

    def get_vacancies(self, criteria: Optional[Dict[str, str]] = None) -> List[Vacancy]:
        filtered = self._vacancies

        if criteria:
            keyword = criteria.get("keyword")
            if keyword:
                keyword_lower = keyword.lower()
                filtered = [
                    v
                    for v in filtered
                    if keyword_lower in v["title"].lower()
                    or keyword_lower in v["description"].lower()
                ]

        return [
            Vacancy(
                title=v["title"],
                link=v["link"],
                salary=v["salary"],
                description=v["description"],
            )
            for v in filtered
        ]

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancy_dict = vacancy.to_dict()
        self._vacancies = [v for v in self._vacancies if v != vacancy_dict]
        self._save_vacancies()
