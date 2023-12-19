"""
    Тестовый модуль, для проверки и отслеживания функционала, в ходе работы и его изменений.
"""
import pytest

from app.schemas import SentimentPrediction


@pytest.mark.parametrize(
    "text, expected_label",
    [
        ("очень плохо", "negative"),
        ("очень хорошо", "positive"),
        ("по-разному", "neutral"),
    ],
)
def test_sentiment(model, text: str, expected_label: str):
    """
    Базовый тест для проверки качества работы модели на оценку тональности текста.

    :param model: fixture - Фикстура для тестов, в ней сама модель:
    :param text: str - Текст, который оценивается на тональность:
    :param expected_label: str - Заранее прописанная оценка тексту:
    """
    model_pred = model(text)

    assert isinstance(model_pred, SentimentPrediction)
    assert model_pred.label == expected_label
