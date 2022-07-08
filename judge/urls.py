from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:problem_id>/', views.detail, name='detail'),
    path('<int:problem_id>/submit', views.submit, name='submit'),

]