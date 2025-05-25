# app/views/news_views.py
from django.shortcuts import render, redirect
from app.models import News
from app.forms import NewsForm
from django.contrib.auth.decorators import login_required

def index(request):
    news_list = News.objects.order_by('-created_at')  # последние новости сверху
    return render(request, 'app/index.html', {'news_list': news_list})
@login_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.user = request.user  # Связываем новость с автором (пользователем)
            news.save()
            return redirect('app:index')  # После добавления новости перенаправляем на главную страницу
    else:
        form = NewsForm()

    return render(request, 'app/add_news.html', {'form': form})