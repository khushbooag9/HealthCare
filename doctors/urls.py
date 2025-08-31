from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.doctor_list_create, name='doctor-list-create'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor-detail'),
    path('doctors/specializations/', views.doctor_specializations, name='doctor-specializations'),
]
