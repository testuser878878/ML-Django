import joblib
import numpy as np

# TODO: Изменить на относительный путь
modelKNN = joblib.load("ml_model/modelKNN.pkl")

modelLP = joblib.load("ml_model/modelLR.pkl")

final_model = joblib.load("ml_model/final_model.pkl")
def predict_glucose_level(glucose_level):
    """
    Функция для предсказания наличия риска диабета на основе уровня глюкозы.
    """
    # Получаем прогнозы от обеих моделей (KNN и LR)
    knn_pred = modelKNN.predict([[glucose_level]])[0]  # Прогноз от KNN
    lp_pred = modelLP.predict([[glucose_level]])[0]  # Прогноз от логистической регрессии

    # Комбинируем прогнозы в новый массив для обучения третьей модели
    predictions = np.array([[knn_pred, lp_pred]])

    result = final_model.predict(predictions)

    if result == 1:
        return "Есть риск сахарного диабета."
    else:
        return "Риск сахарного диабета отсутствует."