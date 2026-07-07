from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('results/<int:pk>/', views.results_view, name='results'),
    path('api/', views.api_view, name='api'),
    path('current_models/', views.current_models_view, name='current_models'),
]
