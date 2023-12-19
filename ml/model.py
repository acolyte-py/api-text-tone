"""
    Модуль, в котором реализована основанная функция ML - части приложение.
    Модель подгружается из pipeline Hugging Face Transformers написанный в config.yaml файле.
    Модель использует CPU (из-за аргумента device=-1).
    После, на подгруженный pipeline идет запрос -> обрабатывается текст -> результирует в формате SentimentPrediction.
"""
from pathlib import Path
from yaml import load, FullLoader

from transformers import pipeline

from app.schemas import SentimentPrediction


config_path = Path(__file__).parent / "config.yaml"
with open(config_path, "r") as file:
    config = load(file, Loader=FullLoader)


def load_model():
    """
    Функция, которая создает вложенную функцию "model"
    Функция model - используя загруженную модель из Hugging Face Transformers, анализирует текст

    :return SentimentPrediction: schema - Схема из модуля "schemas.py":
    """
    model_hf = pipeline(config["task"], model=config["model"], device=-1)

    def model(text: str) -> SentimentPrediction:
        predict = model_hf(text)
        predict_best_class = predict[0]
        return SentimentPrediction(label=predict_best_class["label"], score=predict_best_class["score"],)

    return model
