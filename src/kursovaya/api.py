from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class JobAPI(ABC):
    """
    Абстрактный класс для работы с API платформ с вакансиями.
    Определяет обязательный метод get_vacancies.
    """

    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """
        Получить вакансии по поисковому запросу.

        :param query: поисковый запрос (например, 'Python')
        :return: список вакансий в формате JSON
        """
        pass


class HeadHunterAPI(JobAPI):
    """
    Реализация API для платформы HeadHunter (hh.ru).
    """

    def __init__(self, base_url: str = "https://api.hh.ru"):
        self._base_url = base_url
        self._vacancies_url = f"{self._base_url}/vacancies"

    def get_vacancies(self, query: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Получить вакансии с hh.ru по запросу.

        :param query: поисковый запрос
        :param per_page: количество вакансий на странице (макс. 100)
        :return: список вакансий в формате JSON
        """
        params: Dict[str, Any] = {
            "text": query,
            "area": 113,  # Россия
            "per_page": per_page,
        }

        try:
            response = self._request(self._vacancies_url, params)
            if response.status_code == 200:
                data = response.json()
                items: List[Dict[str, Any]] = data.get("items", [])
                return items
            else:
                print(f"Ошибка при запросе к HH.ru: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Ошибка подключения к HH.ru: {e}")
            return []

    @staticmethod
    def _request(url: str, params: Dict[str, Any]) -> requests.Response:
        """
        Приватный статический метод для отправки GET-запроса.
        """
        return requests.get(url, params=params, timeout=10)
