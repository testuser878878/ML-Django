from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.forms.upload_analusics_form import UploadAnalysisForm
from ml_model.model_module import predict_glucose_level


@login_required
def upload_analysis(request):
    if request.method == 'POST':
        form = UploadAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user

            try:
                # Извлекаем данные из PDF
                patient_data = form.extract_patient_data(request.FILES['pdf_file'])

                # Проверяем, что glucose_level извлечен (первое значение)
                if patient_data[0] == 0:
                    raise ValueError("Не удалось извлечь уровень глюкозы из файла")

                # Делаем прогноз
                prediction = predict_glucose_level([patient_data])

                # Сохраняем результаты
                analysis.result = prediction
                analysis.save()

                return render(request, 'app/upload_analysis_result.html', {
                    'analysis': analysis,
                    'prediction': prediction,
                    'patient_data': patient_data
                })

            except Exception as e:
                form.add_error('pdf_file', f'Ошибка обработки файла: {str(e)}')
    else:
        form = UploadAnalysisForm()

    return render(request, 'app/upload_analysis.html', {'form': form})
