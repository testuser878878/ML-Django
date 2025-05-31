import joblib

ml_model = joblib.load('ml_model/modelCB.pkl')

def predict_glucose_level(X):
    """
    Функция для предсказания наличия риска диабета на основе данных анализа.
    """

    result = ml_model.predict(X)

    if result == 1:
        return "Есть риск сахарного диабета."
    else:
        return "Риск сахарного диабета отсутствует."
