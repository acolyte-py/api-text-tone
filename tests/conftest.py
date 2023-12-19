"""
    Тестовый файл для базовой работы тестов.
"""
import pytest

from ml.model import load_model


@pytest.fixture(scope="function")
def model():
    """
    Фикстура тестов для вызова модели.
    Используется в качестве аргумента к тестовой функции.

    :return def: Возвращает вызов функции:
    """
    return load_model()
