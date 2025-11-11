from abc import ABC, abstractmethod
import requests


class JobAPI(ABC):
    """
    Абстрактный класс для работы с API платформ с вакансиями.
    Определяет обязательный метод get_vacancies.
    """

    @abstractmethod
    def get_vacancies(self, query: str) -> list:
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
        self.base_url = base_url
        self.vacancies_url = f"{self.base_url}/vacancies"

    def get_vacancies(self, query: str, per_page: int = 20) -> list:
        """
        Получить вакансии с hh.ru по запросу.

        :param query: поисковый запрос
        :param per_page: количество вакансий на странице (макс. 100)
        :return: список вакансий в формате JSON
        """
        params = {
            "text": query,
            "area": 113,  # Россия
            "per_page": per_page
        }

        try:
            response = requests.get(self.vacancies_url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("items", [])
            else:
                print(f"Ошибка при запросе к HH.ru: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Ошибка подключения к HH.ru: {e}")
            return []