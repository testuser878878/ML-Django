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
            analysis.user = request.user  # Связываем анализ с пользователем
            analysis.save()

            # Получаем уровень глюкозы и делаем прогноз
            glucose_level = form.cleaned_data['glucose_level']
            prediction = predict_glucose_level(glucose_level)  # Получаем прогноз

            # Добавляем результат прогноза в объект анализа
            analysis.result = prediction
            analysis.save()

            return render(request, 'app/upload_analysis_result.html', {'analysis': analysis, 'prediction': prediction})

    else:
        form = UploadAnalysisForm()

    return render(request, 'app/upload_analysis.html', {'form': form})
