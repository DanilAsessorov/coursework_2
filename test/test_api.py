from unittest.mock import patch
from src.kursovaya.api import HeadHunterAPI


@patch("src.kursovaya.api.requests.get")
def test_headhunter_api_get_vacancies(mock_get):
    """Тест получения вакансий с моком."""
    # Подготовка
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [
            {
                "name": "Python Dev",
                "alternate_url": "https://hh.ru/123",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {"requirement": "Опыт от 3 лет"}
            }
        ]
    }

    # Выполнение
    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python", per_page=1)

    # Проверка
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Dev"