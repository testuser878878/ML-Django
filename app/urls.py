from django.urls import path
from app.migrations.views import news_views, auth_views, profile_views, analysis_views

app_name = 'app'

urlpatterns = [
    path('', news_views.index, name='index'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
    path('profile/', profile_views.profile_view, name='profile'),
    path('add_news/', news_views.add_news, name='add_news'),
    path('upload_analysis/', analysis_views.upload_analysis, name='upload_analysis')
]
