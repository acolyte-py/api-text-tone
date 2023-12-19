"""
    Тестовый модуль, для проверки и отслеживания функционала, в ходе работы и его изменений.
"""
import pytest
import requests

from config import APP_HOST, APP_PORT


@pytest.mark.parametrize(
    "input_text, expected_label",
    [
        ("очень плохо", "negative"),
        ("очень хорошо", "positive"),
        ("по-разному", "neutral"),
    ],
)
def test_sentiment(input_text: str, expected_label: str):
    """
    Базовый тест для проверки качества работы запроса приложения.

    :param input_text: str - Текст, который оценивается на тональность:
    :param expected_label: str - Заранее прописанная оценка тексту:
    """
    response = requests.get(f"http://{APP_HOST}:{APP_PORT}/predict", params={"text": input_text})

    assert response.json()["text"] == input_text
    assert response.json()["sentiment_label"] == expected_label
