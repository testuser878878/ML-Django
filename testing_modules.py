import pdfplumber
import re

from ml_model.model_module import predict_glucose_level


def extract_patient_data(pdf_file):
    """Извлекает данные пациента из PDF файла на русском языке."""
    data_map = {
        'Glucose': 0,
        'Pregnancies': 0,
        'BMI': 0,
        'Age': 0,
        'Insulin': 0,
        'SkinThickness': 0
    }

    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Обновлённые шаблоны под русский текст
    patterns = {
        'Glucose': r'Уровень глюкозы.*?:\s*([\d\.]+)',
        'Pregnancies': r'Количество беременностей.*?:\s*([\d\.]+)',
        'BMI': r'Индекс массы тела.*?:\s*([\d\.]+)',
        'Age': r'Возраст.*?:\s*([\d\.]+)',
        'Insulin': r'Инсулин.*?:\s*([\d\.]+)',
        'SkinThickness': r'Толщина кожи.*?:\s*([\d\.]+)'
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data_map[key] = float(match.group(1))

    return [
        data_map['Glucose'],
        data_map['Pregnancies'],
        data_map['BMI'],
        data_map['Age'],
        data_map['Insulin'],
        data_map['SkinThickness']
    ]


if __name__ == "__main__":
    pdf_path = r"C:\Users\ilyak\OneDrive\Рабочий стол\Пример.pdf"
    patient_data = extract_patient_data(pdf_path)
    prediction = predict_glucose_level([patient_data])
    print(prediction)
